from pymongo import MongoClient
from yaml import load

class Debug:
	def __init__( this ):
		this.config_file        = open("config.yml","r")
                this.client             = None
                this.database           = None
                this.result             = {}
                this.loadConfig()
                this.establishConnection()
                this.getInformation()


        def loadConfig( this ):
                config                  = load(this.config_file)
                db_defined              = False
                this.mongo_ip           = config["mongo_address"]
                this.mongo_port         = config["mongo_port"]
                this.mongo_db           = config["mongo_db"]
                this.mongo_user         = config["mongo_user"]
                this.mongo_pass         = config["mongo_pass"]

        def establishConnection( this ):
                this.client             = MongoClient(this.mongo_ip, this.mongo_port)
                this.database           = this.client[this.mongo_db]
                if not( this.database.authenticate(this.mongo_user, this.mongo_pass) ):
                        print "Database Authentication FAILED."
                        return

	def getInformation( this ):
		for name in this.database.collection_names():
			print name

d = Debug()
