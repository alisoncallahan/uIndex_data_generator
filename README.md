## uIndex_data_generator

The uIndex_data_generator generates an SQL database from PubMed and PubMedCentral records to calculate the uIndex for informatics resources.

The code consists of scripts to 
  1. extract citations from PMC XML files ('scripts/PMCReferenceExtractor.py')
  2. query PubMed for informatics resource articles ('scripts/PubMedPapersQuery.py')
  3. extract information from the retrieved records ('scripts/PubMedPapersProcessor.py')
  4. extract resource names from these records ('scripts/ResourceNameExtractor.py')
  5. load the output of each of these scripts into a SQL database ('scripts/DBLoader.py'). 

'runner.py' runs each script in sequence from (1) - (5), using the options specified below.

To download PMC XML files for your citing universe, follow the instructions for using the NCBI's FTP service for the PubMed Central Open Access subset: https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/ .

### Usage:
    python runner.py [options]

### Options:
    --db_cnf              Configuration file where SQL username 
                          and password are stored (default: ~/.my.cnf)
    --db_host             SQL database host (default: localhost)
    --i [--indir]         Directory containing PMC XML files (required)
    --o [--outdir]        Directory where output will be written (required)
    --sql_port            Port where SQL server is running (default: 3306)
    
### Requirements:
    Python 2.7
    
    argparse, codecs, csv, imp, minidom, MySQLdb, re, urllib2
