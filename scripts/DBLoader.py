import MySQLdb
import string
import os
import csv
import sys

def create_tables(db_handler):

    sql1 = "DROP TABLE IF EXISTS `uindex_data`.`inf_resource_pubmed_title_test`;"
    sql2 = "CREATE TABLE `uindex_data`.`inf_resource_pubmed_title_test` (`pmid` varchar(50) NOT NULL,`title` text) CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql1)
    db_handler.execute(sql2)
    print "Finished creating uindex_data.inf_resource_pubmed_title table..."

    sql3 = "DROP TABLE IF EXISTS `uindex_data`.`inf_resource_pubmed_year_test`;"
    sql4 = "CREATE TABLE `uindex_data`.`inf_resource_pubmed_year_test` (`pmid` varchar(50) NOT NULL, `year` int(4)) CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql3)
    db_handler.execute(sql4)
    print "Finished creating uindex_data.inf_resource_pubmed_year table..."

    sql5 = "DROP TABLE IF EXISTS `uindex_data`.`inf_resource_pubmed_key`;"
    sql6 = "CREATE TABLE  `uindex_data`.`inf_resource_pubmed_key_test` (`pmid` varchar(50) NOT NULL, `key` varchar(250)) CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql5)
    db_handler.execute(sql6)
    print "Finished creating uindex_data.inf_resource_pubmed_key table..."
    print "Finished creating tables!"

    '''
    CREATE TABLE uindex_data.inf_resource_citation_counts_upto2015 (`key` varchar(250), `total` int(11), `used` int(11), `aware` int(11)) ENGINE=MyISAM;
    '''

def load_pubmed_titles(data_file, db_handler):
     with open(data_file, 'r') as infile:
        reader = csv.reader(infile, delimiter="\t", quoting=csv.QUOTE_NONE)
        next(reader, None)
        for row in reader:
            pmid = row[0].strip()
            title = row[1].strip()

            sql = "INSERT INTO `uindex_data`.`inf_resource_pubmed_title_test` VALUES('"\
                  +MySQLdb.escape_string(pmid)+"','"\
                  +MySQLdb.escape_string(title)+"');"
            try:
                db_handler.execute(sql)
            except Exception as err:
                print "Problem PMID: "+pmid
                print("Error: {0}".format(err))
                sys.exit()

def load_pubmed_years(data_file, db_handler):
    with open(data_file, 'r') as infile:
        reader = csv.reader(infile, delimiter="\t", quoting=csv.QUOTE_NONE)
        next(reader, None)
        for row in reader:
            pmid = row[0].strip()
            year = row[1].strip()

            sql = "INSERT INTO `uindex_data`.`inf_resource_pubmed_year_test` VALUES('"\
                  +MySQLdb.escape_string(pmid)+"','"\
                  +MySQLdb.escape_string(year)+"');"
            try:
                db_handler.execute(sql)
            except Exception as err:
                print "Problem PMID: "+pmid
                print("Error: {0}".format(err))
                sys.exit()

def load_pubmed_keys(data_file, db_handler):
    with open(data_file, 'r') as infile:
        reader = csv.reader(infile, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in reader:
            pmid = row[0].strip()
            key = row[2].lower().strip()

            if key is '' or key is None:
                key = pmid

            sql = "INSERT INTO `uindex_data`.`inf_resource_pubmed_key_test` VALUES('"\
              +MySQLdb.escape_string(pmid)+"','"\
              +MySQLdb.escape_string(key)+"');"
            try:
                db_handler.execute(sql)
            except Exception as err:
                print "Problem PMID: "+pmid
                print("Error: {0}".format(err))
                sys.exit()

def index_tables(db_handler):
    sql = "ALTER TABLE `uindex_data`.`inf_resource_pubmed_title_test` ADD INDEX `pmid_idx`(`pmid`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    sql = "ALTER TABLE `uindex_data`.`inf_resource_pubmed_year_test` ADD INDEX `pmid_idx`(`pmid`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    sql = "ALTER TABLE `uindex_data`.`inf_resource_pubmed_key_test` ADD INDEX `pmid_idx`(`pmid`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    sql = "ALTER TABLE `uindex_data`.`inf_resource_pubmed_key_test` ADD INDEX `key_idx`(`key`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

if __name__ == '__main__':

    myDB = MySQLdb.connect(host="shahlab-db1.stanford.edu",port=3306,db="user_acallaha",read_default_file="~/.my.cnf")
    cHandler = myDB.cursor()

    pmid_titles_file = 'out/PubMed100k_titles.txt'
    pmid_years_file = 'out/PubMed100K_dates.txt'
    pmid_keys_file = 'out/PubMed100k_keys.txt'
    create_tables(cHandler)
    load_pubmed_titles(pmid_titles_file,cHandler)
    load_pubmed_years(pmid_years_file,cHandler)
    load_pubmed_keys(pmid_keys_file, cHandler)
    index_tables(cHandler)