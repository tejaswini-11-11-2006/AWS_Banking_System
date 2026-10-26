# AWS_Banking_System
A cloud-hosted banking data analytics and reporting system built using Python, Flask, AWS EC2, Amazon DynamoDB, IAM, and CloudWatch. Features user authentication, transaction management, financial analytics, and reporting through a web-based dashboard.
# AWS Banking Data Analytics and Reporting System

## Project Overview

The **AWS Banking Data Analytics and Reporting System** is a cloud-based web application developed using Python, Flask, and Amazon Web Services (AWS). It aims to provide a web interface for user authentication, banking transaction data management, financial analytics, and report generation.

The application uses Amazon EC2 for hosting and Amazon DynamoDB for storing user and transaction data. AWS IAM helps manage access permissions, while Amazon CloudWatch supports monitoring and troubleshooting.

## Features

- User registration and login
- Banking dashboard with financial summaries
- Transaction data storage and retrieval
- Deposit and withdrawal analytics
- Transaction history and filtering
- Financial reports and CSV export
- AWS cloud deployment using EC2
- Database integration using Amazon DynamoDB
- Access management using AWS IAM
- Application monitoring using Amazon CloudWatch
- Responsive web interface using HTML and CSS

## Technologies Used

- **Programming Language:** Python
- **Web Framework:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Cloud Hosting:** Amazon EC2
- **Database:** Amazon DynamoDB
- **AWS Security:** IAM Roles and Policies
- **Monitoring:** Amazon CloudWatch
- **AWS SDK:** Boto3
- **Development Environment:** Visual Studio Code

## System Architecture

1. Users access the banking application through a web browser.
2. The Flask application processes requests and validates user input.
3. Amazon DynamoDB stores and retrieves application records.
4. Python processes transaction data to generate financial summaries.
5. The dashboard presents analytics and reports.
6. IAM controls application access to AWS resources.
7. CloudWatch supports application and server monitoring.

## Project Structure

```text
AWS-banking-project/
├── App.py
├── templates/
│   ├── index.html
│   ├── dashboard.html
└── static/
    ├── style.css
```

*The structure may vary depending on the features implemented.*

## Installation and Setup

1. Navigate to the project directory:

   ```bash
   cd AWS-banking-project
   ```

2. Create and activate a Python virtual environment.
3. Configure AWS authentication securely and ensure the required DynamoDB tables exist in the configured AWS region.

4. Run the Flask application:

   ```bash
   python App.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.

## Learning Outcomes

- Understanding cloud computing and AWS services
- Developing web applications using Python and Flask
- Integrating applications with Amazon DynamoDB
- Managing AWS permissions using IAM
- Deploying applications on Amazon EC2
- Understanding cloud monitoring using CloudWatch
- Performing basic financial data analytics

## Disclaimer

This project is intended for educational and demonstration purposes. Use fictional banking data only. It is not a production-ready banking or financial transaction platform.

## Author

Developed as a cloud computing and banking data analytics project.
