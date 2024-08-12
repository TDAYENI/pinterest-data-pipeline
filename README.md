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