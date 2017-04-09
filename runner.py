import sys
import os
import argparse
from scripts.PubmedPapersQuery import run as run_pubmed_query
from scripts.PubMedPapersProcessor import   run as run_pubmed_processor

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "Run uIndex data generator.")

    parser.add_argument('-o', '--outdir',
                        dest='output_directory',
                        help='Provide a directory to write output to.',
                        required=True)



    results = parser.parse_args()
    pmids_fp = run_pubmed_query(results.output_directory, limit=1)
    run_pubmed_processor(results.output_directory, pmids_fp)
    #run 3
    # run 4

    #load database


    ## TODO write the rest