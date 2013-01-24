A Node.js Server Script for GenBank files that runs MongoDB as information source.

Example query/Reply:

http://localhost:8001/?id=001R_FRG3G&DR&RL
```json
{
    "RL": "  Virology 323:70-84(2004).\n",
    "DR": "  EMBL; AY548484; AAT09660.1; -; Genomic_DNA.\n  RefSeq; YP_031579.1; NC_005946.1.\n  ProteinModelPortal; Q6GZX4; -.\n  GeneID; 2947773; -.\n  ProtClustDB; CLSP2511514; -.\n  GO; GO:0006355; P:regulation of transcription, DNA-dependent; IEA:UniProtKB-KW.\n  GO; GO:0046782; P:regulation of viral transcription; IEA:InterPro.\n  GO; GO:0006351; P:transcription, DNA-dependent; IEA:UniProtKB-KW.\n  InterPro; IPR007031; Poxvirus_VLTF3.\n  Pfam; PF04947; Pox_VLTF3; 1.\n",
    "ID": "001R_FRG3G"
}
```


Requirements:
	Python 2.X:
		- pymongo module
	Node.js:
		- js-yaml module
	MongoDB

To set the server up, open the "config.yml".
It should look like this:
```yaml
port: 8001				# This is the port the Node.js Server will be running on
mongo_address: localhost		# IP for mongodb server
mongo_port: 27017			# Port for mongodb server
mongo_db: mongo_database		# Database containing the information
mongo_user: mongo_username		# Username to authenticate with
mongo_pass: mongo_password		# Password to authenticate with
# This part is optional, leave it commented out to copy all information to the database
# or set the field names you want to ignore when storing information.
database_ignore:
    - SQ
    - KW
```
Follow the instructions inside the file to set things up.
Once you're done, run this from the command line:
```terminal
./genbank_to_mongodb.py <Path to a GenBank Format file>
```
The file is limited to 20k files by default. You can remove the limit by commenting a marked line in the file out:
```python
				# COMMENT FOLLOWING LINE OUT TO PARSE ALL FILES
				# OR SET NUMBER FOR AMOUNT OF FILES
				if( total_parsed == 20000 ): break
```
Once the script has finished, run this command to start the server up:
```terminal
node server.js
```
