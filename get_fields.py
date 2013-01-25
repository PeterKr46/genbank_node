import sys, os, __main__
from pymongo import MongoClient
from yaml import load
import json

class fieldGrabber:
	
	def __init__(this, id, fields):
		this.fields		= fields
		if( len(fields) == 0 ):
			this.all_wanted	= True
		else:
			this.all_wanted	= False
		this.id			= id
		this.config_file	= open("config.yml","r")
		this.client		= None
		this.database		= None
		this.result		= {}
		if( this.id != "" ):
			this.loadConfig()
			this.establishConnection()
			this.getInformation()


	def loadConfig( this ):
		config			= load(this.config_file)
                db_defined              = False
		this.mongo_ip           = config["mongo_address"]
		this.mongo_port         = config["mongo_port"]
		this.mongo_db           = config["mongo_db"]
		this.mongo_user		= config["mongo_user"]
		this.mongo_pass		= config["mongo_pass"]

	def establishConnection( this ):
		this.client		= MongoClient(this.mongo_ip, this.mongo_port)
		this.database		= this.client[this.mongo_db]
		if not( this.database.authenticate(this.mongo_user, this.mongo_pass) ):
			#print "Database Authentication FAILED."
			return

	def getInformation( this ):
                this.collection         = list(this.database[this.id].find())
		if( len(this.collection) == 0 ):
			#print "ID '%s' not found." % this.id
			return
		this.collection = this.collection[0]
                for key in this.collection.keys():
                        if( ( key in this.fields ) or ( this.all_wanted == True ) ) and ( key != "_id" ):
                                this.result[str(key)] = this.collection[str(key)]
												
			
if( __name__ == '__main__'):
	# Check amount of arguments
	if( len(sys.argv) > 2 ):
		fg = fieldGrabber( sys.argv[1] ,sys.argv[2:])
		print json.dumps(fg.result)
	elif(len(sys.argv) == 2 ):
		fg = fieldGrabber( sys.argv[1], [] )
		print json.dumps(fg.result)
	else:
		print "{}"
