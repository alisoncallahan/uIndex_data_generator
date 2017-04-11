## uIndex_data_generator

Generate a SQL database from PubMed and PubMedCentral records to calculate the uIndex for informatics resources.

### Usage:
    python runner.py [options]

### Options:
    --i [--indir]         Directory containing PMC XML files (required)
    --o [--outdir]        Directory where output will be written
    --db_cnf              Configuration file where SQL username 
                          and password are stored (default: ~/.my.cnf)
    --db_host             SQL database host (default: localhost)
    --debug               Print debug information
    --sql_port            Port where SQL server is running (default: 3306)
    
### Requirements:
    Python 2.7
    
    argparse, codecs, csv, imp, minidom, MySQLdb, re, urllib2
