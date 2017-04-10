import MySQLdb
import csv
import sys

def escape(str):
    if str is None:
        return None
    if str is int:
        return str
    return MySQLdb.escape_string(str)

def create_tables(db_handler):

    sql1 = "DROP TABLE IF EXISTS `uindex_data`.`inf_resource_pubmed_title`;"
    sql2 = "CREATE TABLE `uindex_data`.`inf_resource_pubmed_title` (`pmid` varchar(50) NOT NULL,`title` text) CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql1)
    db_handler.execute(sql2)
    print "Finished creating uindex_data.inf_resource_pubmed_title table..."

    sql3 = "DROP TABLE IF EXISTS `uindex_data`.`inf_resource_pubmed_year`;"
    sql4 = "CREATE TABLE `uindex_data`.`inf_resource_pubmed_year` (`pmid` varchar(50) NOT NULL, `year` int(4)) CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql3)
    db_handler.execute(sql4)
    print "Finished creating uindex_data.inf_resource_pubmed_year table..."

    sql5 = "DROP TABLE IF EXISTS `uindex_data`.`inf_resource_pubmed_key`;"
    sql6 = "CREATE TABLE  `uindex_data`.`inf_resource_pubmed_key` (`pmid` varchar(50) NOT NULL, `key` varchar(250)) CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql5)
    db_handler.execute(sql6)
    print "Finished creating uindex_data.inf_resource_pubmed_key table..."

    sql7 = "DROP TABLE IF EXISTS `uindex_data`.`pmc_article_info`;"
    sql8 = "CREATE TABLE  `uindex_data`.`pmc_article_info` (" \
           "`pmcid` varchar(75) NOT NULL, " \
           "`pmid` varchar(75), " \
           "`doi` varchar(75), " \
           "`year` int(11), " \
           "`journal` varchar(150), " \
           "`heading` TEXT" \
           ") CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql7)
    db_handler.execute(sql8)
    print "Finished creating uindex_data.pmc_article_info table..."

    sql9 = "DROP TABLE IF EXISTS `uindex_data`.`pmc_article_citation`;"
    sql10 = "CREATE TABLE  `uindex_data`.`pmc_article_citation` (" \
           "`pmcid` varchar(75) NOT NULL, " \
           "`ref_id` varchar(75) NOT NULL, " \
           "`section` varchar(100) DEFAULT 'UNKNOWN', " \
           "`journal` varchar(150), " \
           "`year` int(11), " \
           "`id_type` varchar(10), " \
           "`id` varchar(75)" \
           ") CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql9)
    db_handler.execute(sql10)
    print "Finished creating uindex_data.pmc_article_citation table..."

    sql11 = "DROP TABLE IF EXISTS `uindex_data`.`pmc_article_section`;"
    sql12 = "CREATE TABLE  `uindex_data`.`pmc_article_section` (" \
           "`pmcid` varchar(75) NOT NULL, " \
           "`section` TEXT " \
           ") CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql11)
    db_handler.execute(sql12)
    print "Finished creating uindex_data.pmc_article_section table..."

    print "Finished creating tables."

def load_pubmed_titles(data_file, db_handler):
    print "Loading data into uindex_data.inf_resource_pubmed_title_test."
    with open(data_file, 'r') as infile:
        reader = csv.reader(infile, delimiter="\t", quoting=csv.QUOTE_NONE)
        next(reader, None)
        for row in reader:
            pmid = row[0].strip()
            title = row[1].strip()

            sql = "INSERT INTO `uindex_data`.`inf_resource_pubmed_title` VALUES(%s,%s);"
            try:
                db_handler.execute(sql, (pmid, escape(title)))
            except Exception as err:
                print "Problem PMID: "+pmid
                print("Error: {0}".format(err))
                sys.exit()
    print "Finished loading data into uindex_data.into inf_resource_pubmed_title_test ."


def load_pubmed_years(data_file, db_handler):
    print "Loading data into uindex_data.inf_resource_pubmed_year_test."

    with open(data_file, 'r') as infile:
        reader = csv.reader(infile, delimiter="\t", quoting=csv.QUOTE_NONE)
        next(reader, None)
        for row in reader:
            pmid = row[0].strip()
            year = row[1].strip()

            sql = "INSERT INTO `uindex_data`.`inf_resource_pubmed_year` VALUES(%s,%s);"
            try:
                db_handler.execute(sql, (pmid, year))
            except Exception as err:
                print "Problem PMID: "+pmid
                print("Error: {0}".format(err))
                sys.exit()
    print "Finished loading data into uindex_data.inf_resource_pubmed_year_test."


def load_pubmed_keys(data_file, db_handler):
    print "Loading data into uindex_data.inf_resource_pubmed_key_test."

    with open(data_file, 'r') as infile:
        reader = csv.reader(infile, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in reader:
            pmid = row[0].strip()
            key = row[2].lower().strip()

            if key is '' or key is None:
                key = pmid

            sql = "INSERT INTO `uindex_data`.`inf_resource_pubmed_key` VALUES(%s,%s);"
            try:
                db_handler.execute(sql, (pmid, escape(key)))
            except Exception as err:
                print "Problem PMID: "+pmid
                print("Error: {0}".format(err))
                sys.exit()
    print "Finished loading data into uindex_data.inf_resource_pubmed_key_test."

def load_pmc_article_info(data_file, db_handler):
    print "Loading data into uindex_data.pmc_article_info."

    with open(data_file, 'r') as infile:
        reader = csv.reader(infile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in reader:
            pmcid = row[0].strip()
            pmid = row[1].strip()
            doi = row[2].strip()
            year = row[3].strip()
            journal = row[4].strip()
            heading = row[5].strip()

            sql = "INSERT INTO `uindex_data`.`pmc_article_info` VALUES(%s,%s,%s,%s,%s,%s);"
            try:
                db_handler.execute(sql, (escape(pmcid), escape(pmid),escape(doi), escape(year), escape(journal),escape(heading)))
            except Exception as err:
                print "Problem PMCID: "+pmcid
                print("Error: {0}".format(err))
                sys.exit()
    print "Finished loading data into uindex_data.pmc_article_info."

def load_pmc_article_citations(data_file, db_handler):
    print "Loading data into uindex_data.pmc_article_citation."

    with open(data_file, 'r') as infile:
        reader = csv.reader(infile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in reader:
            pmcid = row[0].strip()
            ref_id = row[1].strip()
            section = row[2].strip()
            journal = row[3].strip()
            year = row[4].strip()
            id_type = row[5].strip()
            id = row[6].strip()

            if ref_id == 'NULL':
                ref_id = None

            if section == 'NULL':
                section = None

            if journal == 'NULL':
                journal = None

            if year == 'NULL':
                year = None

            if id_type == 'NULL':
                id_type = None

            if id == 'NULL':
                id = None

            sql = "INSERT INTO `uindex_data`.`pmc_article_citation` VALUES(%s,%s,%s,%s,%s,%s,%s);"
            try:
                db_handler.execute(sql, (escape(pmcid), escape(ref_id), escape(section), escape(journal), escape(year), escape(id_type), escape(id)))
            except Exception as err:
                print "Problem PMCID: "+pmcid
                print("Error: {0}".format(err))
                sys.exit()
    print "Finished loading data into uindex_data.pmc_article_citation."


def load_pmc_article_sections(data_file, db_handler):
    print "Loading data into uindex_data.pmc_article_section."

    with open(data_file, 'r') as infile:
        reader = csv.reader(infile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in reader:
            pmcid = row[0].strip()
            section = row[1].strip()

            if section == 'NULL':
                section = None
            sql = "INSERT INTO `uindex_data`.`pmc_article_section` VALUES(%s,%s);"
            try:
                db_handler.execute(sql, (escape(pmcid), escape(section)))
            except Exception as err:
                print "Problem PMCID: "+pmcid
                print("Error: {0}".format(err))
                sys.exit()
    print "Finished loading data into uindex_data.pmc_article_section."

def index_tables(db_handler):
    sql = "ALTER TABLE `uindex_data`.`inf_resource_pubmed_title` ADD INDEX `pmid_idx`(`pmid`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    sql = "ALTER TABLE `uindex_data`.`inf_resource_pubmed_year` ADD INDEX `pmid_idx`(`pmid`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    sql = "ALTER TABLE `uindex_data`.`inf_resource_pubmed_key` ADD INDEX `pmid_idx`(`pmid`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    sql = "ALTER TABLE `uindex_data`.`inf_resource_pubmed_key` ADD INDEX `key_idx`(`key`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    sql = "ALTER TABLE `uindex_data`.`pmc_article_info` ADD INDEX `pmcid_idx`(`pmcid`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    sql = "ALTER TABLE `uindex_data`.`pmc_article_citation` ADD INDEX `pmcid_idx`(`pmcid`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    sql = "ALTER TABLE `uindex_data`.`pmc_article_citation` ADD INDEX `id_idx`(`id`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    sql = "ALTER TABLE `uindex_data`.`pmc_article_section` ADD INDEX `pmcid_idx`(`pmcid`);"
    try:
        db_handler.execute(sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    print "Finished indexing tables."

def generate_uindex_data(db_handler):

    sql = "DROP TABLE IF EXISTS `uindex_data`.`pmc_research_articles`;"
    db_handler.execute(sql)
    sql = "CREATE TABLE `uindex_data`.`pmc_research_articles` (`pmcid` varchar(75) NOT NULL) CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql)

    print "Extracting research articles from uindex_data.pmc_article_info."
    pmc_research_articles_sql = "INSERT INTO `uindex_data`.`pmc_research_articles` SELECT DISTINCT a.pmcid AS pmcid FROM `uindex_data`.`pmc_article_info` a, `uindex_data`.`pmc_article_section` b " \
                                "WHERE a.pmcid=b.pmcid " \
                                "AND a.heading NOT LIKE '%addend%' " \
                                "AND a.heading NOT LIKE '%brief communication%' " \
                                "AND a.heading NOT LIKE '%clinical overview%' " \
                                "AND a.heading NOT LIKE '%column%' " \
                                "AND a.heading NOT LIKE '%comment%' " \
                                "AND a.heading NOT LIKE '%communication%' " \
                                "AND a.heading NOT LIKE '%correction%' " \
                                "AND a.heading NOT LIKE '%editor%' " \
                                "AND a.heading NOT LIKE '%errata%' " \
                                "AND a.heading NOT LIKE '%erratum%' " \
                                "AND a.heading NOT LIKE '%interview%' " \
                                "AND a.heading NOT LIKE '%opinion%' " \
                                "AND a.heading NOT LIKE '%perspective%' " \
                                "AND a.heading NOT LIKE '%reply%' " \
                                "AND a.heading NOT LIKE '%report%' " \
                                "AND a.heading NOT LIKE '%review%' " \
                                "AND (b.section LIKE '%ethod%' OR (b.section LIKE '%material%' AND b.section NOT LIKE '%supplement%'));"
    try:
        db_handler.execute(pmc_research_articles_sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    print "Finished extracting research articles from uindex_data.pmc_article_info."

    sql = "DROP TABLE IF EXISTS `uindex_data`.`citation_counts_2015`;"
    db_handler.execute(sql)
    sql = "CREATE TABLE `uindex_data`.`citation_counts_2015` (`key` varchar(75) NOT NULL, `total` int(20), `used` int(20), `aware` int(20)) CHARACTER SET utf8 ENGINE=MyISAM;"
    db_handler.execute(sql)

    insert_uindex_citation_counts_sql = "INSERT INTO `uindex_data`.`citation_counts_2015` SELECT DISTINCT inte0.key, inte3.total AS total, inte3.used AS used, inte3.total-inte3.used AS aware FROM " \
                                        "(SELECT `pmid`,`key` FROM `uindex_data`.`inf_resource_pubmed_key`) " \
                                        "AS inte0 " \
                                        "LEFT JOIN " \
                                        "( " \
                                        "SELECT inte1.key, inte1.total, inte2.used FROM " \
                                        "( " \
                                        "SELECT `uindex_data`.`inf_resource_pubmed_key`.`key`, COUNT(DISTINCT  `uindex_data`.`pmc_article_citation`.`pmcid`) as total " \
                                        "FROM `uindex_data`.`inf_resource_pubmed_title`, `uindex_data`.`inf_resource_pubmed_key`, `uindex_data`.`pmc_article_citation`, `uindex_data`.`pmc_research_articles`,  `uindex_data`.`pmc_article_info` " \
                                        "WHERE `uindex_data`.`inf_resource_pubmed_titles`.pmid = `uindex_data`.`inf_resource_pubmed_key`.pmid " \
                                        "AND `uindex_data`.`pmc_article_citation`.id = `uindex_data`.`inf_resource_pubmed_title`.pmid " \
                                        "AND `uindex_data`.`pmc_article_citation`.`id_type` = 'pmid' " \
                                        "AND `uindex_data`.`pmc_article_citation`.`pmcid` = `uindex_data`.`pmc_research_articles`.pmcid " \
                                        "AND `uindex_data`.`pmc_article_citation`.`pmcid` = `uindex_data`.`pmc_article_info`.pmcid " \
                                        "AND `uindex_data`.`pmc_article_info`.`year` < 2016 " \
                                        "GROUP BY `uindex_data`.`inf_resource_pubmed_key`.key " \
                                        "ORDER BY count(distinct `uindex_data`.`pmc_article_citation`.`pmcid`) DESC " \
                                        ") AS inte1 " \
                                        "LEFT JOIN " \
                                        "( " \
                                        "SELECT `uindex_data`.`inf_resource_pubmed_key`.`key`, COUNT(DISTINCT  `uindex_data`.`pmc_article_citation`.`pmcid`) as used " \
                                        "FROM `uindex_data`.`inf_resource_pubmed_title`, `uindex_data`.`inf_resource_pubmed_key`, `uindex_data`.`pmc_article_citation`, `uindex_data`.`pmc_research_articles`,  `uindex_data`.`pmc_article_info` " \
                                        "WHERE `uindex_data`.`inf_resource_pubmed_title`.pmid = `uindex_data`.`inf_resource_pubmed_key`.pmid " \
                                        "AND `uindex_data`.`pmc_article_citation`.id = `uindex_data`.`inf_resource_pubmed_title`.pmid " \
                                        "AND `uindex_data`.`pmc_article_citation`.`id_type` = 'pmid'" \
                                        "AND `uindex_data`.`pmc_article_citation`.`pmcid` = `uindex_data`.`pmc_research_articles`.pmcid " \
                                        "AND `uindex_data`.`pmc_article_citation`.`pmcid` = `uindex_data`.`pmc_article_info`.pmcid " \
                                        "AND `uindex_data`.`pmc_article_info`.`year` < 2016 " \
                                        "AND (`uindex_data`.`pmc_article_citation`.`section` LIKE '%ethod%'  OR (`uindex_data`.`pmc_article_citation`.`section` LIKE '%material%' AND `uindex_data`.`pmc_article_citation`.`section` NOT LIKE '%supplement%')) " \
                                        "GROUP BY `uindex_data`.`inf_resource_pubmed_key`.key " \
                                        ") AS inte2 " \
                                        "ON (inte1.key  = inte2.key) " \
                                        ") AS inte3 " \
                                        "ON (inte0.key=inte3.key);"

    try:
        db_handler.execute(insert_uindex_citation_counts_sql)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit()

    print "Finished generating uIndex citation data for 2015."
    print "Finished generating uIndex data."
    return None

def run(db_host, sql_port, db_schema, cnf_file, pmid_titles_fp, pmid_dates_fp, pmid_keys_fp, pmc_article_fp, pmc_ref_fp, pmc_section_fp):
    myDB = MySQLdb.connect(host=db_host,port=sql_port,db=db_schema,read_default_file=cnf_file)
    cHandler = myDB.cursor()

    create_tables(cHandler)
    load_pubmed_titles(pmid_titles_fp,cHandler)
    load_pubmed_years(pmid_dates_fp,cHandler)
    load_pubmed_keys(pmid_keys_fp, cHandler)
    load_pmc_article_info(pmc_article_fp, cHandler)
    load_pmc_article_citations(pmc_ref_fp, cHandler)
    load_pmc_article_sections(pmc_section_fp, cHandler)
    index_tables(cHandler)
    generate_uindex_data(cHandler)