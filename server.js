var yaml	= require("js-yaml");
var http	= require("http");
var fs		= require("fs");
var spawn	= require("child_process").spawn;

// Add String.startsWith function
if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.indexOf(str) == 0;
  };
}


function GenBankServer()
{
	// Load configuration file
	try{
		this.config	= require("./config.yml");
		config		= this.config;
	}
	catch (Error)
	{
		console.log("Config file missing!!!");
		return;
	}

	
	// Gets fields from an entry in the Mongo database.
	this.getFieldsFromId = function (id, fields,res)
	{
		var args = new Array();
		args.push("get_fields.py");
		args.push(id);
		for( var i = 0; i < fields.length; i++ )
		{
			args.push(fields[i]);
		}
		var cmd = spawn("python",args);
		cmd.stdout.on('data',
			function(data)
			{
				res.end( JSON.stringify(JSON.parse( data ),null,4) );
			}	);
		cmd.stderr.on('data',function(data){ res.end(data); } );
	}
	
	// Make getFieldsFromId public/accessible
	getFieldsFromId = this.getFieldsFromId;

	// Handles HTTP Requests
	this.requestHandler = function (req, res)
	{
		if( req.method != "GET" || req.url == "/" || req.url == "/favicon.ico")
		{
			res.end("{ }\n");
			return;
		}
		var res = res;
		//console.log("Received request for: " + req.url);
		var GETData	= req.url.split("?")[1];
		if(GETData == undefined || GETData == "")
		{
			res.end("{ }\n");
		}
		var keys	= GETData.split("&");
		var fields	= [];
		var id;
		for( var k = 0; k < keys.length; k++ )
		{
			if( keys[k].indexOf("=") == -1 )
			{
				fields.push(keys[k]);
			}else{
				if( keys[k].split("=")[0] != "id") continue;
				id = keys[k].split("=")[1];
			}
		}
		// Debug output
		console.log("Received request for fields: \n" + fields + "\nID: " + id);
		getFieldsFromId(id,fields,res);
		setTimeout(function(){ res.end(); }, 2000);
		
	}

	// Launch HTTP Server
        this.srv = http.createServer(this.requestHandler);
        this.srv.listen(this.config["port"]);
	console.log("GBS started.");
}

gbs = new GenBankServer();
