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

## Create the VPC 

AWS > VPC Dashboard > Create VPC
Name: helloec2rdsipaddress-vpc-manual
IPv4 CIDR block: 10.0.0.0/24
Click Create.

Internet Gateway (IGW):

AWS > VPC Dashboard > Internet Gateways > Create internet gateway
Name:  helloec2rdsipaddress-internet-gateway-manual
Attach Internet Gateway to VPC...
- Actions > Attach to VPC (select helloec2rdsipaddress-vpc-manual)

Select the newly created IGW.
Click on Actions > Attach to VPC.
Select your VPC (VPC resource).
Subnets:

AWS > VPC Dashboard > Subnets > Create Subnet
Name: helloec2rdsipaddress-subnet-public-manual
CIDR block: 10.0.0.0/28
Choose the VPC (select helloec2rdsipaddress-vpc-manual)
Enable Auto-assign public IPv4 address (note: for some reason need to override/disable this when creating EC2 instance...looking into that with AWS tech support)
Repeat the same for helloec2rdsipaddress-subnet-db1-manual/10.0.0.16/28 and helloec2rdsipaddress-subnet-db2-manual/10.0.0.32/28 don't enable auto-assing public ip for these)

Route Tables: helloec2rdsipaddress-public-route-table-manual, helloec2rdsipaddress-db-route-table-manual...
...subnet associations

Routes for route public table
...Edit routes > 
Add a route to  helloec2rdsipaddress-public-route-table-manual 0.0.0.0/0 for target helloec2rdsipaddress-internet-gateway-manual

Create security groups: helloec2rdsipaddress-securitygroup-internal-traffic-manual, helloec2rdsipaddress-securitygroup-public-traffic-manual
For helloec2rdsipaddress-securitygroup-public-traffic-manual, add inbound rule: TCP traffic from 0.0.0.0/0 on port 8080.
Assign it to your VPC (VPC resource).
Add an inbound rule allowing TCP traffic from ...whats my ip.... on port 8080, another rule for SSH
For helloec2rdsipaddress-securitygroup-internal-traffic-manual, add inbound rule allowing all traffic from source helloec2rdsipaddress-securitygroup-internal-traffic-manual (all traffic from anything within the security group is allowed to all components that are members of the security group)

## Create the instance
EC2 > Launch instance 
Name: helloec2rdsipaddress-webserver-manual
OS Image: Amazon Linux (free tier eligible)
Network settings > Edit ...set auto-assign public ip to disabled (because, throws an error, otherwise...talking to customer support)
Keypair: Create new keypair (rsa, .pem, name: keypair-helloec2rdsipaddress)
Security group: helloec2rdsipaddress-securitygroup-public-traffic-manual
Launch instance

Elastic IPs > Allocate Elastic IP Addresses...select all defaults and click "Allocate"
Elastic IPs > Select newly allocated Elastic IP > Actions > Associate...

EC2 > Instances > select instance that was created > Connect > SSH client...use the command provided (ssh -i "keypair-helloec2rdsipaddress.pem" ec2-user@52.86.14.235)
