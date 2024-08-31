# Pinterest Data Pipeline

## Table of Contents
- [Description](#description)
- [Project Dependencies](#project-dependencies)
- [The Dataset](#the-dataset)
- [Utilized Tools](#utilized-tools)
  - [Apache Kafka](#apache-kafka)
  - [AWS MSK (Amazon Managed Streaming for Apache Kafka)](#aws-msk-amazon-managed-streaming-for-apache-kafka)
  - [AWS MSK Connect](#aws-msk-connect)
  - [Kafka REST Proxy](#kafka-rest-proxy)
  - [AWS API Gateway](#aws-api-gateway)
  - [Apache Spark](#apache-spark)
  - [PySpark](#pyspark)
  - [Databricks](#databricks)
- [Setup](#setup)
  - [Setting up the EC2 Instance & Apache Kafka](#setting-up-the-ec2-instance--apache-kafka)
  - [Connecting MSK Cluster to an S3 Bucket](#connecting-msk-cluster-to-an-s3-bucket)
  - [Configuring API in AWS API Gateway](#configuring-api-in-aws-api-gateway)
  - [Setting up Kafka REST Proxy on the EC2 Client](#setting-up-kafka-rest-proxy-on-the-ec2-client)
- [Batch Processing](#batch-processing)
  - [Data Cleaning](#data-cleaning)
  - [Data Analysis](#data-analysis)
- [Stream Processing](#stream-processing)
  - [Creating Data Streams with Kinesis](#creating-data-streams-with-kinesis)
  - [Configure an API with Kinesis Proxy Integration](#configure-an-api-with-kinesis-proxy-integration)
  - [Create `user_posting_emulation_streaming.py`](#create-user_posting_emulation_streampy)
  - [Read Data from Kinesis Streams in Databricks](#read-data-from-kinesis-streams-in-databricks)
  - [Data Cleaning](#data-cleaning-1)
  - [Write the Data to Delta Tables](#write-the-data-to-delta-tables)
- [File Structure](#file-structure)
- [License](#license)

## Description

Pinterest crunches billions of data points every day to provide more value to its users. In this project, I created a similar system using AWS Cloud. The project was planned for a month and involved setting up a comprehensive data pipeline that mirrors Pinterest's data processing operations.

The project is divided into three main parts:
- **Setup**
- **Batch Processing**
- **Stream Processing**

## Project Dependencies

To execute this project, the following Python packages are required:

- `python-dotenv`
- `sqlalchemy`
- `requests`

## The Dataset

The project includes a script (`user_posting_emulation.py`) that simulates the flow of data points similar to those received by Pinterest's API during user data uploads. This data is stored in an AWS RDS database with the following tables:

- **pinterest_data**: Data about posts being uploaded to Pinterest.
- **geolocation_data**: Geolocation data related to each Pinterest post.
- **user_data**: Information about the users uploading the posts.

The script continuously cycles through random intervals, selecting rows from each table and compiling them into dictionaries for further processing.

## Utilized Tools

### Apache Kafka
Apache Kafka is an event streaming platform used to process streaming data in real time.

### AWS MSK (Amazon Managed Streaming for Apache Kafka)
Amazon MSK is a fully managed service for Apache Kafka, enabling the easy setup and management of Kafka clusters.

### AWS MSK Connect
MSK Connect simplifies the process of streaming data to and from Apache Kafka clusters.

### Kafka REST Proxy
The Confluent REST Proxy provides a RESTful interface to interact with Kafka clusters, allowing message production, consumption, and cluster administration via HTTP requests.

### AWS API Gateway
Amazon API Gateway is a managed service that facilitates the creation, publication, maintenance, and security of APIs.

### Apache Spark
Apache Spark is a powerful engine for data processing, enabling large-scale data engineering and machine learning.

### PySpark
PySpark is the Python API for Apache Spark, used for real-time, distributed data processing.

### Databricks
Databricks is a platform that provides tools for running Apache Spark applications, used in this project for batch and stream data processing.

## Setup

### Setting up the EC2 Instance & Apache Kafka

To set up the foundational components of this project:

1. **Create a Key Pair File:**
   - In the AWS console, generate a key-pair file for authentication.
  
2. **Configure Security Groups:**
   - Create a security group with rules allowing HTTP, HTTPS, and SSH access.
  
3. **Launch an EC2 Instance:**
   - Use the Amazon Linux 2 AMI to create an EC2 instance and install Kafka and IAM MSK authentication packages on the client EC2 machine.

4. **Configure Kafka Client Properties:**
   - Modify the Kafka client properties to enable AWS IAM authentication.

5. **Create MSK Clusters and Kafka Topics:**
   - Set up Amazon MSK clusters and create Kafka topics for the three data tables.

### Connecting MSK Cluster to an S3 Bucket

1. **Create an S3 Bucket:**
   - Create an S3 bucket to store the data extracted from the MSK cluster.
  
2. **Create an IAM Role:**
   - Set up an IAM role with permissions to write to the S3 bucket.

3. **Create a VPC Endpoint:**
   - Establish a VPC endpoint to connect the MSK cluster directly to the S3 bucket.

4. **Set up MSK Connect:**
   - Create a connector using a custom plug-in associated with the IAM role to stream data from MSK to the S3 bucket.

### Configuring API in AWS API Gateway

1. **Create and Configure an API:**
   - Set up a REST API in AWS API Gateway, create child resources, and configure methods to interact with the Kinesis streams.

2. **Deploy the API:**
   - Deploy the API to obtain an invoke URL, which is used to send data to the Kafka topics via the API.

### Setting up Kafka REST Proxy on the EC2 Client

1. **Install Confluent Package:**
   - Install the Confluent package for Kafka REST Proxy on the EC2 client machine.

2. **Configure the `kafka-rest.properties`:**
   - Modify the properties file to specify the bootstrap server and IAM role.

3. **Deploy the REST Proxy API:**
   - Deploy the API and use it to send data to Kafka topics.

## Batch Processing

### Data Cleaning

To perform batch processing:

1. **Mount the S3 Bucket in Databricks:**
   - Mount the S3 bucket to Databricks and load the data into DataFrames.

2. **Clean the Data:**
   - Use PySpark to clean the data by removing duplicates, renaming columns, handling null values, and converting data types.

3. **Automate Processing with MWAA:**
   - Set up MWAA to trigger Databricks notebooks automatically, using a DAG file for scheduling.

### Data Analysis

The `batch_queries.ipynb` notebook contains queries to analyze the cleaned data, providing insights such as popular Pinterest categories, follower counts, and user activity over time.

## Stream Processing

### Creating Data Streams with Kinesis

1. **Create Kinesis Streams:**
   - Create three streams in Kinesis for the `pin`, `geo`, and `user` data.

### Configure an API with Kinesis Proxy Integration

1. **Set up API Resources:**
   - Create resources and methods in AWS API Gateway to interact with Kinesis streams via HTTP requests.

2. **Deploy the API:**
   - Deploy the API to enable real-time data streaming.

### Create `user_posting_emulation_streaming.py`

1. **Send Data to Kinesis Streams:**
   - Modify the provided script to send data to the Kinesis streams using the configured API.

### Read Data from Kinesis Streams in Databricks

1. **Ingest and Clean Streaming Data:**
   - In Databricks, read data from the Kinesis streams, clean it, and prepare it for storage.

### Write the Data to Delta Tables

1. **Save Cleaned Data:**
   - Save the cleaned streaming data into Delta Tables in Databricks.

## File Structure

Your main project folder should have the following structure:

```plaintext
pinterest-data-pipeline/
├── images/                             # Images used in the documentation
├── .gitignore                          # Specifies files and directories to ignore in Git
├── 0abb070c336b_dag.py                 # DAG file for Apache Airflow
├── 0abb070c336-key-pair.pem            # Key pair file for authentication
├── batch_data_cleaning.ipynb           # Jupyter Notebook for batch data cleaning
├── batch_queries.ipynb                 # Jupyter Notebook for batch data analysis
├── README.md                           # Main documentation file
├── streaming_data.ipynb                # Jupyter Notebook for streaming data processing
├── user_posting_emulation.py           # Script for emulating user posting data
└── user_posting_emulation_streaming.py # Script for emulating user posting data with streaming
