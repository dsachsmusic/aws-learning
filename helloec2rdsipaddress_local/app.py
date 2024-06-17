from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://helloec2rds_user:mypassword@localhost/db_helloec2rdsipaddress_misc'
db = SQLAlchemy(app)

# Route for handling requests
@app.route('/')
def hello_world():
    visitor_ip = request.remote_addr  # Get visitor's IP address

    # Check if the IP address exists in the database
    sql_query = text("SELECT * FROM tbl_visitor_ip WHERE ip_address = :addr")
    ip_entry = db.session.execute(sql_query, {"addr": visitor_ip}).fetchone()

    if ip_entry:
        return f"Hello again {visitor_ip}!"
    else:
        # If IP address doesn't exist, add it to the database
        sql_insert = text("INSERT INTO tbl_visitor_ip (ip_address) VALUES (:addr)")
        db.session.execute(sql_insert, {"addr": visitor_ip})
        db.session.commit()
        return f"Hello {visitor_ip}! Welcome for the first time."

if __name__ == '__main__':
    app.run(debug=True)