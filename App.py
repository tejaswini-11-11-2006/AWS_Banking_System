from flask import Flask, render_template, request, redirect, url_for, session
import boto3
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# AWS DynamoDB Connection (Local credentials kiwa EC2 IAM role vaprel)
dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-2")
users_table = dynamodb.Table("users")
transactions_table = dynamodb.Table("transactions")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    hashed_password = generate_password_hash(password)
    user_id = str(uuid.uuid4())

    # Save user to DynamoDB Users table with 0 initial balance
    users_table.put_item(
        Item={
            "user_id": user_id,
            "name": name,
            "email": email,
            "password": hashed_password,
            "balance": Decimal("0.0"),
        }
    )
    return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    # Scan/Query user by email (For simplicity using scan here)
    response = users_table.scan()
    items = response.get("Items", [])

    user = next((item for item in items if item["email"] == email), None)

    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["user_id"]
        session["name"] = user["name"]
        return redirect(url_for("dashboard"))

    return "Invalid Credentials! Try Again."


from boto3.dynamodb.conditions import Attr


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("home"))

    user_id = session["user_id"]

    # Get user balance
    response = users_table.get_item(Key={"user_id": user_id})
    user = response.get("Item")

    # Get transaction history for this user
    tx_response = transactions_table.scan(
        FilterExpression=Attr("sender_id").eq(user_id) | Attr("receiver_id").eq(user_id)
    )
    transactions = tx_response.get("Items", [])

    return render_template("dashboard.html", user=user, transactions=transactions)


@app.route("/deposit", methods=["POST"])
def deposit():
    if "user_id" not in session:
        return redirect(url_for("home"))

    amount = Decimal(request.form["amount"])
    user_id = session["user_id"]

    # Update balance in DynamoDB
    response = users_table.get_item(Key={"user_id": user_id})
    current_balance = response["Item"]["balance"]
    new_balance = current_balance + amount

    users_table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET balance = :val",
        ExpressionAttributeValues={":val": new_balance},
    )

    # Log Transaction
    transactions_table.put_item(
        Item={
            "transaction_id": str(uuid.uuid4()),
            "timestamp": str(datetime.now()),
            "sender_id": user_id,
            "receiver_id": user_id,
            "amount": amount,
            "type": "Deposit",
        }
    )

    return redirect(url_for("dashboard"))

    @app.route("/withdraw", methods=["POST"])
    def withdraw():
        if "user_id" not in session:
            return redirect(url_for("home"))

    amount = Decimal(request.form["amount"])
    user_id = session["user_id"]

    # Get current balance from DynamoDB
    response = users_table.get_item(Key={"user_id": user_id})
    current_balance = response["Item"]["balance"]

    # Check if user has enough balance
    if current_balance < amount:
        return "Insufficient Balance! <a href='/dashboard'>Go Back</a>"

    new_balance = current_balance - amount

    # Update balance in DynamoDB
    users_table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET balance = :val",
        ExpressionAttributeValues={":val": new_balance},
    )

    # Log Transaction in Transactions table
    transactions_table.put_item(
        Item={
            "transaction_id": str(uuid.uuid4()),
            "timestamp": str(datetime.now()),
            "sender_id": user_id,
            "receiver_id": user_id,
            "amount": amount,
            "type": "Withdrawal",
        }
    )

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
