import sys
import os
import argparse
from scripts.PubmedPapersQuery import run as run_pubmed_query
from scripts.PubMedPapersProcessor import  run as run_pubmed_processor
from scripts.ResourceNameExtractor import run as run_toolname_extractor
if __name__ == '__main__':

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
                        dest="db_host",
                        help="SQL database host (e.g. localhost)",
                        default="localhost",
                        required=False
                        )

    parser.add_argument('-sql_port',
                        dest="sql_port",
                        help="Port where SQL  server is running (default: 3306)",
                        default=3306,
                        required=False
                        )

    parser.add_argument('-db_schema',
                        dest="db_schema",
                        help="DB schema to load data into",
                        default="uindex_data",
                        required=False)

    args = parser.parse_args()

    pmids_fp = run_pubmed_query(args.output_directory, limit=1)
    titles_fp = run_pubmed_processor(args.output_directory, pmids_fp)
    resource_names = run_toolname_extractor(args.output_directory, titles_fp)

    # run 4

    #load database


    ## TODO write the rest