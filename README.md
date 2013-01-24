A Node.js Server Script for GenBank files that runs MongoDB as information source.

Requirements:
	Python 2.X:
		- pymongo module
	Node.js:
		- js-yaml module
	MongoDB

To set the server up, open the "config.yml".
It should look like this:
```yaml
port: 8001
mongo_address: localhost
mongo_port: 27017
mongo_db: mongo_database
mongo_user: mongo_username
mongo_pass: mongo_password
# This part is optional, leave it commented out to copy all information to the database
# or set the field names you want to store.
database_ignore:
    - SQ
    - KW
```

 
