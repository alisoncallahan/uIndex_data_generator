## uIndex_data_generator

The uIndex_data_generator generates an SQL database from PubMed and PubMedCentral records to calculate the uIndex for informatics resources.

All you need to get started is a directory containing the set of PubMed Central (PMC) XML files that represent the citing universe of interest, and a MySQL instance running. 

To download PMC XML files for your citing universe, follow the instructions to use the NCBI's FTP service for the PubMed Central Open Access subset: https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/.

The methods to extract citations from the PMC XML files, retrieve PubMed records for informatics resources, and count the number of usage and awareness citations in order to calcuate the u-Index are ready to use out-of-the-box, as detailed below. 

The code consists of scripts to: 
  1. extract references and citations from PMC XML files ('scripts/PMCReferenceExtractor.py')
  2. query PubMed for informatics resource articles ('scripts/PubMedPapersQuery.py')
  3. extract information (PMID, title, authors, publication date, MeSH terms) from the retrieved records ('scripts/PubMedPapersProcessor.py')
  4. extract resource names from these records ('scripts/ResourceNameExtractor.py')
  5. load the output of each of these scripts into a SQL database ('scripts/DBLoader.py'). 

'runner.py' runs each script in sequence from (1) - (5), using the options specified below.

### Usage:
    python runner.py [options]

### Options:
    -db_cnf              Configuration file where SQL username 
                          and password are stored (default: ~/.my.cnf)
    -db_host             SQL database host (default: localhost)
    -i [--indir]         Directory containing PMC XML files (required)
    -o [--outdir]        Directory where output will be written (required)
    -sql_port            Port where SQL server is running (default: 3306)
    
### Example:
    python runner.py -db_cnf ~/.my.cnf -db_host localhost -i /path/to/pmc/xml/ -o /path/to/output/dir/ -sql_port 3306

### Requirements:
    Python 2.7
    
    argparse, codecs, csv, imp, minidom, MySQLdb, re, urllib2
