"""
Flask Application for Distributed MySQL Query Routing

This Flask application demonstrates a simple implementation of proxy and Gatekeeper design patterns for a distributed MySQL system
where queries are routed to different MySQL nodes based on a specified routing strategy.

Modules:
- Flask: Web framework for handling HTTP requests
- mysql.connector: Connector for MySQL database

Classes:
- MySQLCluster: Represents a MySQL node (either master or slave) with configuration details.
- Proxy: Routes queries to different nodes based on a specified routing strategy.
- DirectHitStrategy, RandomStrategy, CustomizedStrategy: Strategies for query routing.
- Gatekeeper: Processes requests and directs them through the proxy.
- App: Main Flask application.

Functions:
- proxy_pattern: Creates a proxy instance based on the specified routing strategy.

Usage:
1. Run the script to start the Flask application.
2. Send POST requests to the '/process_request' endpoint with a JSON payload specifying the query type.
   Supported query types: 'read' and 'write'.

"""
from flask import Flask, request, jsonify
import random
import mysql.connector
import sys

app = Flask(__name__)

# Define AWS configuration

MASTER_NODE_IP = "50.17.104.45"
SLAVE_NODES_IPS = ["54.226.235.123", "34.228.70.150", "52.55.169.12"]
PROXY_SERVER_IP = "54.83.121.193"
PROXY_SERVER_INSTANCE_TYPE = "t2.large"  # Add the proxy server instance type here

# Define MySQL configuration for master, slaves, and proxy
MASTER_DB_HOST = MASTER_NODE_IP
MASTER_DB_USER = "sabadb"
MASTER_DB_PASSWORD = "SK$@2023"
MASTER_DB_DATABASE = "finalTP"

SLAVE_DB_USER = "sabadb"
SLAVE_DB_PASSWORD = "SK$@2023"
SLAVE_DB_DATABASE = "finalTP"

PROXY_DB_USER = "sabadb"  # Adjust as needed
PROXY_DB_PASSWORD = "SK$@2023"  # Adjust as needed
PROXY_DB_DATABASE = "finalTP"  # Adjust as needed

 #MySQLCluster
 
class MySQLCluster:
    def __init__(self, is_master):
        self.is_master = is_master
        self.db_endpoint = MASTER_DB_HOST
        self.db_user = MASTER_DB_USER if is_master else PROXY_DB_USER
        self.db_password = MASTER_DB_PASSWORD if is_master else PROXY_DB_PASSWORD
        self.db_database = MASTER_DB_DATABASE if is_master else PROXY_DB_DATABASE

    def get_connection(self):
        return mysql.connector.connect(
            host=self.db_endpoint,
            user=self.db_user,
            password=self.db_password,
            database=self.db_database,
            autocommit=True  # Add this line to enable autocommit
        )
# Proxy
class Proxy:
    def __init__(self, cluster, strategy, proxy_ip, instance_type):
        self.cluster = cluster
        self.strategy = strategy
        self.proxy_ip = proxy_ip
        self.instance_type = instance_type

    def route_query(self, query):
        node = self.strategy.select_node()
        print(f"Routing query to {node}")
        with node.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)

class DirectHitStrategy:
    def __init__(self, cluster):
        self.cluster = cluster

    def select_node(self):
        return self.cluster

class RandomStrategy:
    def __init__(self, nodes):
        self.nodes = nodes

    def select_node(self):
        return random.choice(self.nodes)

class CustomizedStrategy:
    def __init__(self, cluster, all_nodes):
        self.cluster = cluster
        self.all_nodes = all_nodes

    def select_node(self):
        ping_times = {node: self.measure_ping_time(node) for node in self.all_nodes}
        min_ping_node = min(ping_times, key=ping_times.get)
        return min_ping_node

    def measure_ping_time(self, node):
        # Simulate measuring ping time (replace with actual ping logic)
        return random.uniform(0.1, 1.0)

# Gatekeeper

class Gatekeeper:
    def __init__(self, proxy):
        self.proxy = proxy

    def process_request(self, query_type):
        if query_type == "read":
            query = "SELECT * FROM test_requests;"
        elif query_type == "write":
            query = "INSERT INTO test_requests (id, name) VALUES (1, 'John'), (2, 'Alice'), (3, 'Bob');"
        else:
            raise ValueError("Invalid query type")

        self.proxy.route_query(query)

def proxy_pattern(strategy, master_node, nodes):
    if strategy == "direct":
        return Proxy(master_node, DirectHitStrategy(master_node), PROXY_SERVER_IP, PROXY_SERVER_INSTANCE_TYPE)
    elif strategy == "random":
        return Proxy(master_node, RandomStrategy(nodes), PROXY_SERVER_IP, PROXY_SERVER_INSTANCE_TYPE)
    elif strategy == "customized":
        return Proxy(master_node, CustomizedStrategy(master_node, nodes), PROXY_SERVER_IP, PROXY_SERVER_INSTANCE_TYPE)
    else:
        raise ValueError("Invalid strategy")


# Create instances for master and slave

master_node = MySQLCluster(is_master=True)
slave_nodes = [MySQLCluster(is_master=False) for _ in range(len(SLAVE_NODES_IPS))]

strategy = sys.argv[1] if len(sys.argv) > 1 else "direct"
proxy_instance = proxy_pattern(strategy, master_node, slave_nodes)
gatekeeper = Gatekeeper(proxy_instance)

@app.route('/process_request', methods=['POST'])
def process_request():
    data = request.get_json()
    query_type = data.get('query_type', '')

    if query_type not in ['read', 'write']:
        return jsonify({'error': 'Invalid query type'}), 400

    gatekeeper.process_request(query_type)

    return jsonify({'message': 'Request processed successfully'})

if __name__ == "__main__":
    # Create database and table on startup for master
    with master_node.get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS finalTP;")
        cursor.execute("USE finalTP;")
        cursor.execute("CREATE TABLE IF NOT EXISTS test_requests (id INT, name VARCHAR(255));")
    app.run(host='0.0.0.0', port=5000)
