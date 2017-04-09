import sys
import os
import argparse
from scripts.PubmedPapersQuery import run as run_pubmed_query

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "Run uIndex data generator.")

    parser.add_argument('-o', '--outdir',
                        dest='output_directory',
                        help='Provide a directory to write output to.',
                        required=True)

    results = parser.parse_args()
    print results.output_directory
    run_pubmed_query(results.output_directory)
    ## TODO write the rest