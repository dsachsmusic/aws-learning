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