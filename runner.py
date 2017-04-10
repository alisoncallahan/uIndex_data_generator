'''
@author: alisoncallahan
'''

import argparse
from scripts.PMCReferenceExtractor import run as run_pmc_extractor
from scripts.PubmedPapersQuery import run as run_pubmed_query
from scripts.PubMedPapersProcessor import  run as run_pubmed_processor
from scripts.ResourceNameExtractor import run as run_toolname_extractor
from scripts.DBLoader import run as run_db_loader
if __name__ == '__main__':
    #host="shahlab-db1.stanford.edu",port=3306,db="user_acallaha"
    parser = argparse.ArgumentParser(description = "Run uIndex data generator.")

    parser.add_argument('-i',
                        '--indir',
                        dest='input_directory',
                        help='Directory where citing universe PMC XML files are located.',
                        required=True
                        )
    parser.add_argument('-o',
                        '--outdir',
                        dest='output_directory',
                        help='Directory where output will be written.',
                        required=True)

    parser.add_argument('-db_host',
                        dest='db_host',
                        help='SQL database host (e.g. localhost)',
                        default='localhost',
                        required=False
                        )

    parser.add_argument('-sql_port',
                        dest='sql_port',
                        help='Port where SQL  server is running (default: 3306)',
                        default=3306,
                        required=False
                        )

    parser.add_argument('-db_cnf',
                        dest='db_cnf',
                        help='Configuration file where SQL username and password are stored.',
                        default='~/.my.cnf',
                        required=False
                        )

    args = parser.parse_args()


    print "########################################################"
    print "### Processing PMC records to build citing universe. ###"
    print "########################################################"
    pmc_article_fp, pmc_reference_fp, pmc_sections_fp = run_pmc_extractor(args.input_directory, args.output_directory)

    print "########################################################"
    print "###   Downloading informatics resource PubMed IDs.   ###"
    print "########################################################"
    pmids_fp = run_pubmed_query(args.output_directory, limit=1)

    print "########################################################"
    print "###  Processing informatics resource PubMed records. ###"
    print "########################################################"
    titles_fp, dates_fp = run_pubmed_processor(args.output_directory, pmids_fp)

    print "########################################################"
    print "###      Extracting informatics resource names.      ###"
    print "########################################################"
    resource_names_fp = run_toolname_extractor(args.output_directory, titles_fp)

    print "########################################################"
    print "###      Creating and loading u-Index database.      ###"
    print "########################################################"
    run_db_loader(args.db_host,
                  args.sql_port,
                  args.db_cnf,
                  titles_fp,
                  dates_fp,
                  resource_names_fp,
                  pmc_article_fp,
                  pmc_reference_fp,
                  pmc_sections_fp
                  )


    ## TODO write the rest