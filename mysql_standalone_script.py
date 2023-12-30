import subprocess

import subprocess

# Update package information and install MySQL Server
subprocess.run(["sudo", "apt-get", "update"])
subprocess.run(["sudo", "apt-get", "install", "-y", "mysql-server"])

# Run the MySQL secure installation script
subprocess.run(["sudo", "mysql_secure_installation"])

print("MySQL Stand-alone Server setup complete.")
