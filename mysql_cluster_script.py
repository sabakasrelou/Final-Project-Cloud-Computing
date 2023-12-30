import subprocess
import os

# MySQL Stand-alone Server Setup
subprocess.run(["sudo", "apt-get", "update"])
subprocess.run(["sudo", "apt-get", "install", "-y", "mysql-server"])
subprocess.run(["sudo", "mysql_secure_installation"])

# MySQL Cluster Installation and Configuration
MYSQL_CLUSTER_VERSION = "7.2.1"
MYSQL_CLUSTER_URL = f"http://dev.mysql.com/get/Downloads/MySQL-Cluster-{MYSQL_CLUSTER_VERSION}/mysql-cluster-gpl-{MYSQL_CLUSTER_VERSION}-linux2.6-x86_64.tar.gz"

# Download and extract MySQL Cluster
subprocess.run(["sudo", "wget", MYSQL_CLUSTER_URL])
subprocess.run(["sudo", "tar", "xvf", f"mysql-cluster-gpl-{MYSQL_CLUSTER_VERSION}-linux2.6-x86_64.tar.gz"])
subprocess.run(["sudo", "ln", "-s", f"mysql-cluster-gpl-{MYSQL_CLUSTER_VERSION}-linux2.6-x86_64", "mysqlc"])

# Create necessary directories
subprocess.run(["sudo", "mkdir", "-p", "/opt/mysqlcluster/deploy/{conf,mysqld_data,ndb_data}"])
subprocess.run(["sudo", "mkdir", "-p", "/opt/mysqlcluster/home"])

# Create MySQL Cluster configuration file
mysql_cnf_content = """
[mysqld]
ndbcluster
datadir=/opt/mysqlcluster/deploy/mysqld_data
basedir=/home/ubuntu/mysql-cluster-gpl-{MYSQL_CLUSTER_VERSION}-linux2.6-x86_64/bin/mysqlc
socket=/var/run/mysqld/mysqld.sock
port=3306
"""
with open("/opt/mysqlcluster/home/my.cnf", "w") as cnf_file:
    cnf_file.write(mysql_cnf_content)


# Initialize MySQL Cluster
subprocess.run(["sudo", "scripts/mysql_install_db", "--no-defaults", "datadir=/opt/mysqlcluster/deploy/mysqld_data"])

# Install required library
subprocess.run(["sudo", "apt-get", "update"])
subprocess.run(["sudo", "apt-get", "-y", "install", "libncurses5"])

# Start MySQL Cluster Management Server
subprocess.run(["sudo", f"/home/ubuntu/mysql-cluster-gpl-{MYSQL_CLUSTER_VERSION}-linux2.6-x86_64/bin/ndb_mgmd",
                "-f", "/opt/mysqlcluster/deploy/conf/config.ini", "--initial", "--configdir=/opt/mysqlcluster/deploy/conf/",
                "--ndb-nodeid=1"])

# Display cluster configuration and status
subprocess.run([f"/home/ubuntu/mysql-cluster-gpl-{MYSQL_CLUSTER_VERSION}-linux2.6-x86_64/bin/ndb_mgm", "-e", "show"])

print("MySQL Cluster setup complete.")
