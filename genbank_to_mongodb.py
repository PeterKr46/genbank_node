#! /usr/bin/python
# Required external modules:
# - pymongo
# - pyyaml
from pymongo import Connection
from yaml import load, dump
import sys,os
import __main__

class Struct:
    def __init__(self, d):
            for a, b in d.items():
	    	if isinstance(b, (list, tuple)):
			setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
		else:
			setattr(self, a, obj(b) if isinstance(b, dict) else b)


class GBParser:
	
	# Prepare the parser
	def __init__( this, path ):
		this.file_handler	= open(path, "r")
		this.config_file	= open("config.yml","r")
		this.filepath		= path
		this.information	= {"SQ":""}
		this.unwanted_fields	= [] 
		this.all_wanted		= False
		this.documents		= []
		this.total		= 0

	def load_config( this ):
		config			= load(this.config_file)
		db_defined		= False

		this.mongo_ip		= config["mongo_address"]
		this.mongo_port		= config["mongo_port"]
		this.mongo_db		= config["mongo_db"]

		for c in config:
			if( str(c) == "database_ignore"): db_defined = True
		if ( db_defined == False ):
			this.all_wanted	= True
			return
		this.unwanted_fields	= config["database_ignore"]

	def parse( this ):
		blockname	= None
		total_parsed	= 0
		for line in this.file_handler:
			# If current line is the end of a document, move to archive
			if(line.startswith("//")):
				this.documents.append(this.information)
				this.information = { "SQ":"" }
				total_parsed += 1
				print "\r %s documents parsed in total." % total_parsed,
				# COMMENT FOLLOWING LINE OUT TO PARSE ALL FILES
				# OR SET NUMBER FOR AMOUNT OF FILES
				if( total_parsed >= 2000 ): break
			# If current line is a comment, ignore it
			if(line.startswith("CC")): continue
			# If current line is indented, add to Sequence
			if( line.startswith(" ") ):
				this.information["SQ"] += line

			last_blockname	= blockname
			if not( line.startswith(" ") ): blockname = line.split(" ")[0]

			if(last_blockname == blockname):
				this.information[blockname] += " ".join(line.split(" ")[1:])
			elif( blockname != "ID" ):
				this.information[blockname] = " ".join(line.split(" ")[1:])
			else:
				for c in line.split(" "):
					if( c == "ID" or c == "" ): continue
					else:
						this.information[blockname] = c
						break
		print "\nDone Reading."
	

if( len(sys.argv) == 1 ):
	print __main__.__file__ + " <GenBank File>"
else:
	if not ( os.path.exists(sys.argv[1]) ):
		print "File '%s' not found." % sys.argv[1];
	else:
		parser = GBParser(sys.argv[1])
		parser.load_config()
		parser.parse()
		res = ""
		tosave = {}
		total = 0
		conn = Connection(parser.mongo_ip,parser.mongo_port)
		db = getattr(conn,parser.mongo_db)

		for document in parser.documents:
			#print document
			for i in document.keys():
				if (not( i in parser.unwanted_fields )) or ( parser.all_wanted == True ): 
					tosave[i] = document[i]
			# Debug output
			#print tosave
			collection = db[tosave["ID"]]
			collection.insert(tosave)
			total += 1
			print "\r " + str(total) + " Documents written to the database.",
