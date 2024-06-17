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
General guide to stumble through https://medium.com/@amarakulin/aws-practical-guide-ec2-rds-with-cloudformation-93ff2cbcb8e
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
    - Template file path: cf-template-helloec2rdsipaddress.yaml
    - Complete the rest of the  Note: For "Configure stack options", choose defaults  
  - Job will fail, saying that cf-update-stack-git-repo-aws-learning doesn't trust the connection 
  - Complete the above steps one more time, except, for IAM Role, select "Existing IAM role"
  - Completes successfully. Notice Pull Requst in Git repo "Add AWS Cloudformation Deployment file for cfstackhelloec2rdsipaddress stack #1"
