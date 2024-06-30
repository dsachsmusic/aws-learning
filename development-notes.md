# Local Dev Environment set up
General guide to stumble through https://code.tutsplus.com/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972t

Install flask (already done)

Install mysql https://www.geeksforgeeks.org/how-to-install-mysql-in-windows/
- Note: saw no "Developer Default" setup type option, so ran "Full" ... then ran installer with all defaults 
- Note: to run mySQL from cmd, run "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p

Set stuff up in mySQL...
CREATE DATABASE db_helloec2rdsipaddress_misc

CREATE TABLE db_helloec2rdsipaddress_misc.tbl_visitor_ip (
	id INT AUTO_INCREMENT PRIMARY KEY,
	ip_address VARCHAR(50) UNIQUE
);

CREATE USER 'helloec2rds_user'@'localhost' IDENTIFIED BY 'mypassword';
GRANT SELECT, INSERT, UPDATE, DELETE ON db_helloec2rdsipaddress_misc.tbl_visitor_ip TO 'helloec2rds_user'@'localhost';

Install SQLAlchemy 
- pip install -U Flask-SQLAlchemy

Install mysql 
In Flask app, we'll want 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://helloec2rds_user:rmypassword@localhost.db_helloec2rdsipaddress_misc'
db = SQLAlchemy(app)
# Cloud formations 
Starting with setting up Cloud Formations...which I am figuring out with help from ChatGPT

Create an IAM account, grant it AWSCloudFormationFullAccess (this might be be granular enough to be considered best practice)
Link Git repo to AWS
- In AWS...go to Cloud Formations > Create Stack, and select
  - Choose an existing template
  - Sync from Git
    - Follow steps to set up a connection
- In AWS, go to go to Cloud Formations > Create Stack, and select
  - Choose an existing template
  - Sync from Git
    - follow the steps prompts...
    - outcome: in Git, under Integrations > Github Apps, see AWS Connector
  - Link a git repository
    - select the connection set up previously
    - select the repository and branch
    - Deployment file path: cfstackhelloec2rdsipaddress-deploy.yaml
    - For IAM Role, select "New IAM role"
      - Name: cf-update-stack-git-repo-aws-learning
    - Template file path: cf-template-  .yaml
    - Complete the rest of the  Note: For "Configure stack options", choose defaults  
  - Job will fail, saying that cf-update-stack-git-repo-aws-learning doesn't trust the connection 
  - Complete the above steps one more time, except, for IAM Role, select "Existing IAM role"
  - Completes successfully. Notice Pull Requst in Git repo "Add AWS Cloudformation Deployment file for cfstackhelloec2rdsipaddress stack #1".  Merge it.
  - In Git, git fetch, git merge (or whatever), then add template file cf-template-helloec2rdsipaddress.yaml to the repo, and commit

Next: set up the template - based on this guide (stumble through it) https://medium.com/@amarakulin/aws-practical-guide-ec2-rds-with-cloudformation-93ff2cbcb8e

# Side track: Doing it manually
Note: I had the thought that I should configure this manually, to fully understand it, before doing it via Cloud Formations
...steps I'm taking:

## Create the VPC and components

VPC
- AWS > VPC Dashboard > Create VPC
- Name: helloec2rdsipaddress-vpc-manual
- IPv4 CIDR block: 10.0.0.0/24
- Click Create.

Internet Gateway (IGW)
- AWS > VPC Dashboard > Internet Gateways > Create internet gateway
- Name:  helloec2rdsipaddress-internet-gateway-manual

Attach Internet Gateway to VPC...
- Actions > Attach to VPC (select helloec2rdsipaddress-vpc-manual)
- Select the newly created IGW.
- Click on Actions > Attach to VPC.
- Select your VPC (VPC resource).

Subnets
- AWS > VPC Dashboard > Subnets > Create Subnet
- Name: helloec2rdsipaddress-subnet-public-manual
- CIDR block: 10.0.0.0/28
- Choose the VPC (select helloec2rdsipaddress-vpc-manual)
- Enable Auto-assign public IPv4 address (note: for some reason need to override/disable this when creating EC2 instance...looking into that with AWS tech support)
- Repeat the same for helloec2rdsipaddress-subnet-db1-manual/10.0.0.16/28 and helloec2rdsipaddress-subnet-db2-manual/10.0.0.32/28 don't enable auto-assing public ip for these)

Route Tables
- helloec2rdsipaddress-public-route-table-manual, helloec2rdsipaddress-db-route-table-manual...
...subnet associations

Routes for route public table
- ...Edit routes > 
- Add a route to  helloec2rdsipaddress-public-route-table-manual 0.0.0.0/0 for target helloec2rdsipaddress-internet-gateway-manual

security groups
- helloec2rdsipaddress-securitygroup-internal-traffic-manual, helloec2rdsipaddress-securitygroup-public-traffic-manual
- For helloec2rdsipaddress-securitygroup-public-traffic-manual, add inbound rule: TCP traffic from 0.0.0.0/0 on port 8080.
- Add an inbound rule allowing TCP traffic from ...whats my ip.... on port 8080, another rule for SSH
- For helloec2rdsipaddress-securitygroup-internal-traffic-manual, add inbound rule allowing all traffic from source helloec2rdsipaddress-securitygroup-public-traffic-manual (all traffic from anything within the security group is allowed to all components that are members of the security group)

## Create the instance
EC2
- EC2 > Launch instance 
- Name: helloec2rdsipaddress-webserver-manual
- OS Image: Amazon Linux (free tier eligible)
- Network settings > Edit ...set auto-assign public ip to disabled (because, throws an error, otherwise...talking to customer support)
- Keypair: Create new keypair (rsa, .pem, name: keypair-helloec2rdsipaddress)
- Security group: helloec2rdsipaddress-securitygroup-public-traffic-manual
- Launch instance

Elastic IP
- Elastic IPs > Allocate Elastic IP Addresses...select all defaults and click "Allocate"
- Elastic IPs > Select newly allocated Elastic IP > Actions > Associate...

Connect
- EC2 > Instances > select instance that was created > Connect > SSH client...use the command provided (ssh -i "keypair-helloec2rdsipaddress.pem" ec2-user@52.86.14.235)

## Configure Python and Flask and create hello world app

Dependencies
- Confirm python is installed by running the command python3 --version
- Install pip: sudo yum install python3-pip -y
- Install virutalenv: sudo pip3 install virtualenv

Create a user: sudo adduser flaskapp
- Create a group (to manage resources that the new user, as well the regular user, should have access to) sudo groupadd flaskapp
- Grant the group (and the user) ownership over the user home folder sudo chown -R flaskapp:flaskapp /home/flaskapp
- Add regular user account to the the group (created for "managing resources that the new user, as well as the regular user...")sudo usermod -aG flaskapp ec2-user
- Tip: If desired, confirm, user added to group, if Confirm with: groups ec2-user
- Make user folder accessible (grant read and write) to group that was granted ownership over the folder the sudo chmod -R 775 /home/flaskapp
- Confirm permissions applied ls -ld /home/flaskapp
  - (should be drwxrwxr-x)
- Make a directory to hold the application mkdir /home/flaskapp/helloec2rdsipaddress
- Chmod that directory: sudo chmod -R 775 /home/flaskapp/helloec2rdsipaddress/
- change the owner group of that directory...to flaskapp:flaskapp: sudo chown -R flaskapp:flaskapp /home/flaskapp
- Change directory, to /home/flaskapp/helloec2rdsipaddress
- Create a virtual environment: python -m venv venv
- Activate the virtual environment: source venv/bin/activate
- Install flask: pip install flask
- create an app.py file...with a simple hello world.  For app.run...use app.run(host='IP Address of the host', port=8080, debug=True) 
- Run python app.py
- Connect http://publicipaddress:8080 to see "Hello, World"

...Next step will be to set up gunicorn and nginx


# Create RDS instance

Create the DB Subnet Group
AWS > RDS > Create DB Subnet Group
- Select the subnets created for this purpose, etc. 
Create the RDS instance 

AWS > RDS >  Create database.
- Choose Standard Create.
- Select Engine (PostgreSQL in this case).
- etc. 
- For security group, select the "internal" one
- For machine size, etc. Single-AZ db.t2.micro or db.t3.micro instance.
- Storage...go minimum: 20 GB of storage (SSD)
- create a first DB called db_hello_misc
Note: Turn this off regularly...because it is expensive...and, be aware that it automatically turns back on every 7 days
- RDS > Databases > select the RDS instance > Actions > Stop
- Should set up a script to stop every 7 days, or just use Aurora

# Configure EC2 instance to talk to Postgress

Install postgres sql client...
- This is so, later, in case we want to test querying against table from bash (after we create the table with python)
- run yum list | grep postgres
  -...find the name of the currently available postgresql and postgresql_libs package (for example, postgresql15.x86_64 and postgresql15-private-libs.x86_64)
  - sudo yum install said packages


Install dependencies within virtual environment...run:
- pip install psycopg2-binary
- pip install sqlalchemy
- note: We use psycopg2-binary to query postgres with sqlalchemy

Build a connection string, create a query to create the table 
- Note: To find the hostname and port, AWS >  RDS > "Connectivity & security" tab >  "Endpoint" and "Port"
  - Btw...This endpoint is reachable using AWS' VPC's built in DNS resolution

create a file named create_table.py, and add the following contents
```
from sqlalchemy import create_engine, text
engine = (create_engine("postgresql+psycopg2://postgres:mypassword@db-helloec2rdsipaddress.ctcsm8kwqy85.us-east-1.rds.amazonaws.com:5432/db_hello_misc"))
create_table_query = '''
CREATE TABLE tbl_contact_me (
    contact_me_id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(100),
    email VARCHAR(100),
    message VARCHAR(1500)
)
'''
with engine.begin() as connection:
    connection.execute(text(create_table_query))
```
Test connecting to the database from bash:
- psql -h db-helloec2rdsipaddress.ctcsm8kwqy85.us-east-1.rds.amazonaws.com -U postgres -d db_hello_misc
- describe the tables:
  - \dt 

Create and run file called insert_test.py
```
from sqlalchemy import create_engine, text
engine = (create_engine("postgresql+psycopg2://postgres:mypassword@db-helloec2rdsipaddress.ctcsm8kwqy85.us-east-1.rds.amazonaws.com:5432/db_hello_misc"))
insert_statement = '''
    INSERT INTO tbl_contact_me (name, email, message)
    VALUES ('John Doe', 'john@example.com', 'This is a test message.');
'''
with engine.begin() as connection:
    connection.execute(text(insert_statement))
```
Create and run a file called select_statement.py

```
from sqlalchemy import create_engine, text
engine = (create_engine("postgresql+psycopg2://postgres:mypassword@db-helloec2rdsipaddress.ctcsm8kwqy85.us-east-1.rds.amazonaws.com:5432/db_hello_misc"))
select_statement = '''
SELECT * FROM tbl_contact_me
'''
with engine.begin() as connection:
    connection.execute(text(select_statement))
```	

A lesson learned during this work: don't create a file called select.py when using sqlalchemy (it conflicts with a module in sqlalchemy called select.py)