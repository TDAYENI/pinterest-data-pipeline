# Read Me file
# Pinterest Data Pipeline

**Author**: Daniel Ayeni  
**Contact**: titilayoay@hotmail.com  
**Project Start Date**: 01/08/2024

---

## Table of Contents
1. [Project Description](#project-description)
2. [Prerequisites](#prerequisites)
3. [Installation Instructions](#installation-instructions)
4. [Usage Instructions](#usage-instructions)
5. [AWS Setup Instructions](#aws-setup-instructions)
6. [Kafka and MSK Setup](#kafka-and-msk-setup)
7. [S3 Setup and Connector Configuration](#s3-setup-and-connector-configuration)
8. [File Structure](#file-structure)
9. [License](#license)

---

## Project Description
This project simulates a data pipeline similar to what Pinterest might use to process and store user activity data. The goal is to utilize AWS cloud services to ingest, process, and store data. The pipeline will involve using Amazon MSK (Managed Streaming for Apache Kafka), S3 for storage, and IAM for secure authentication.

---

## Prerequisites
- GitHub account for version control.
- AWS account with access to necessary services (MSK, S3, IAM, EC2).
- Basic knowledge of Python, AWS, and Kafka.
- Installed tools: AWS CLI, Kafka, Python, and a code editor like VSCode.

---

## Installation Instructions

### 1. Setup AWS Account
- Navigate to [AWS](https://aws.amazon.com/) and log in using the credentials provided.
- Ensure that you are operating in the `us-east-1` region throughout the project.

### 2. Configure GitHub Repository
- Use GitHub to track changes. A repository should be created at the start of the project to save your code.

### 3. Create a Key Pair
- Navigate to AWS Parameter Store, locate the KeyPairId, and retrieve your key pair.
- Save the key pair value in a `.pem` file in VSCode.

---

## Usage Instructions
### Running the Python Script
- Download the `user_posting_emulation.py` script.
- Create a `db_creds.yaml` file to store database credentials securely.
- Run the script to print out `pin_result`, `geo_result`, and `user_result` to familiarize yourself with the data.

---

## AWS Setup Instructions

### 1. Connect to EC2 Instance
- Save the key pair with the format `<KeyPairName>.pem`.
- Use the SSH client to connect to your EC2 instance.

### 2. Set Up Kafka on EC2
- Install Kafka (version 2.12-2.8.1) on your EC2 instance.
- Ensure that the security rules for the EC2 instance allow communication with the MSK cluster.

### 3. IAM Configuration for MSK
- Navigate to the IAM console.
- Find the role with the format `<YOUR_UUID>-ec2-access-role`.
- Edit the trust policy to allow access and copy the role ARN for later use.

---

## Kafka and MSK Setup

### 1. Configure Kafka Client
- Modify the `client.properties` file in your Kafka folder to use AWS IAM authentication.

### 2. Create Kafka Topics
- Retrieve the Bootstrap servers string and the Plaintext Apache Zookeeper connection string from the MSK Management Console.
- Create the following Kafka topics using the retrieved information:
  - `<YOUR_UUID>.pin`
  - `<YOUR_UUID>.geo`
  - `<YOUR_UUID>.user`

---

## S3 Setup and Connector Configuration

### 1. Identify Your S3 Bucket
- Go to the S3 console and find the bucket named `user-<YOUR_UUID>-bucket`.
- Make a note of the bucket name.

### 2. Download and Upload Confluent S3 Connector
- Download the Confluent.io Amazon S3 Connector.
- Use the following command to upload the connector to your S3 bucket:
  ```bash
  aws s3 cp ./confluentinc-kafka-connect-s3-10.5.13.zip s3://user-<YOUR_UUID>-bucket/kafka-connect-s3/

### 3. Create and Configure Custom Plugin

1. **Navigate to MSK Connect Console**:
   - Open the AWS Management Console and navigate to the **MSK Connect** service.
   - In the **Plugins** section, choose to create a new custom plugin.

2. **Create a Plugin**:
   - Name the plugin `<YOUR_UUID>-plugin` (replace `<YOUR_UUID>` with your specific User ID).
   - Upload the connector file that you previously placed in the S3 bucket.
   - Follow the on-screen instructions to complete the plugin creation.

3. **Configure the Connector**:
   - In the MSK Connect console, after creating the plugin, proceed to create a connector.
   - Name the connector `<YOUR_UUID>-connector`.

4. **Set Connector Configurations**:
   - **Bucket Name**: Set the `s3.bucket.name` property to `user-<YOUR_UUID>-bucket`.
   - **Topics Regex**: Set the `topics.regex` field to `<YOUR_UUID>.*`. This configuration ensures that all data passing through the Kafka topics you created (e.g., `<YOUR_UUID>.pin`, `<YOUR_UUID>.geo`, `<YOUR_UUID>.user`) will be captured by the connector.
   - **IAM Role**: When configuring access permissions, select the IAM role `<YOUR_UUID>-ec2-access-role` that you set up earlier. This role must have the necessary permissions to authenticate with both MSK and S3.

5. **Deploy the Connector**:
   - Review the connector settings and deploy it.
   - Once deployed, the connector will start ingesting data from the Kafka topics and writing it to the S3 bucket in JSON format, using the configuration specified.
