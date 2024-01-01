
MySQL with AWS Deployment.
Overview:
This repository contains a Python script for deploying a distributed MySQL system on AWS using the Boto3 library. The system includes the creation of a security group, launching multiple EC2 instances of different types, and deploying a Flask application for distributed MySQL query routing.

Prerequisites
Before running the script, ensure that you have the following:

AWS credentials (access key, secret key, and session token) stored in a config.py file.
Boto3 library installed: pip install boto3
AWS Deployment Script
The script (deploy_aws.py) performs the following actions:

AWS Credentials: Loads AWS credentials from the config.py file.

EC2 Client Initialization: Initializes an EC2 client with the specified credentials and region.

Security Group Creation: Creates a security group with rules allowing SSH (port 22), HTTP (port 80), and custom port 5000-5002 traffic.

EC2 Instance Launching: Launches 5 EC2 instances of type t2.micro and 2 EC2 instances of type t2.large in the us-east-1a availability zone.

Wait for Instance Initialization: Waits for all instances to be in the 'running' state before displaying a success message.

Flask Application for Distributed MySQL Query Routing
The app.py file contains a Flask application demonstrating a simple implementation of proxy and gatekeeper design patterns for a distributed MySQL system. It includes the following modules, classes, and functions:

Modules
Flask: Web framework for handling HTTP requests
mysql.connector: Connector for MySQL database
Classes
MySQLCluster: Represents a MySQL node (either master or slave) with configuration details.
Proxy: Routes queries to different nodes based on a specified routing strategy.
DirectHitStrategy, RandomStrategy, CustomizedStrategy: Strategies for query routing.
Gatekeeper: Processes requests and directs them through the proxy.
App: Main Flask application.
Functions
proxy_pattern: Creates a proxy instance based on the specified routing strategy.
Usage
Run the app.py script to start the Flask application.
Send POST requests to the /process_request endpoint with a JSON payload specifying the query type ('read' or 'write').
MySQL Stand-alone Server Setup
The mysql_setup.py script automates the setup of a MySQL stand-alone server, including installation, secure configuration, and initialization.

MySQL Cluster Installation and Configuration
The mysql_cluster_setup.py script automates the installation and configuration of a MySQL Cluster on AWS instances. It includes the download and extraction of MySQL Cluster, creation of necessary directories, and initialization of the cluster.

Stand-alone MySQL Server Setup
The standalone_mysql_setup.py script automates the setup of a stand-alone MySQL server on an AWS instance. It includes the installation of MySQL Server, running the secure installation script, and completing the setup.

Notes
Ensure that you have the necessary AWS credentials and permissions before running the deployment script.
Review and modify the configuration parameters in the scripts to match your specific requirements.
