'''
@author: Rainer Winnenburg
@author: Alison Callahan
'''
import urllib2
from xml.dom import minidom

def returnIDs(q):    
    response = urllib2.urlopen(q)
    xmldoc = minidom.parse(response)
    
    ret = set()
    for id in xmldoc.getElementsByTagName('Id'):
        ret.add(id.firstChild.nodeValue)
    return ret

def write(medlines,out):
    for m in medlines:
        out.write(m+"\n")
    out.close()

def run(output_directory,limit=100000):
    master = set()

    #
    # Software[major] OR Database[major]
    #
    q = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=(Software%5BMAJOR%5D%20OR%20databases,%20factual[MAJR:NOEXP]%20OR%20databases,%20protein[MAJR:NOEXP]%20OR%20databases,%20nucleic%20acid[MAJR:NOEXP]%20OR%20databases,%20pharmaceutical[MAJR:NOEXP]%20OR%20databases,%20chemical[MAJR:NOEXP]%20OR%20databases,%20genetic[MAJR:NOEXP])&RETMAX=" + str(limit) + "&retmode=XML"
    for pmid in returnIDs(q):
        master.add(pmid)

    #
    # RESCUE queries: any combination of two MH (does not need to be major)
    #
    q = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=(Software%5BMH%5D%20AND%20(databases,%20factual[MH:NOEXP]%20OR%20databases,%20protein[MH:NOEXP]%20OR%20databases,%20nucleic%20acid[MH:NOEXP]%20OR%20databases,%20pharmaceutical[MH:NOEXP]%20OR%20databases,%20chemical[MH:NOEXP]%20OR%20databases,%20genetic[MH:NOEXP]))&RETMAX=" + str(limit) + "&retmode=XML"
    for pmid in returnIDs(q):
        master.add(pmid)


    q = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=(Algorithms%5BMH%5D%20AND%20(databases,%20factual[MH:NOEXP]%20OR%20databases,%20protein[MH:NOEXP]%20OR%20databases,%20nucleic%20acid[MH:NOEXP]%20OR%20databases,%20pharmaceutical[MH:NOEXP]%20OR%20databases,%20chemical[MH:NOEXP]%20OR%20databases,%20genetic[MH:NOEXP]))&RETMAX=" + str(limit) + "&retmode=XML"
    for pmid in returnIDs(q):
        master.add(pmid)


    q = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=(Algorithms%5BMH%5D%20AND%20Software%5BMH%5D)&RETMAX=" + str(limit) + "&retmode=XML"
    for pmid in returnIDs(q):
        master.add(pmid)

    q = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=(Computer%20Communication%20Networks%5BMH%5D%20AND%20(databases,%20factual[MH:NOEXP]%20OR%20databases,%20protein[MH:NOEXP]%20OR%20databases,%20nucleic%20acid[MH:NOEXP]%20OR%20databases,%20pharmaceutical[MH:NOEXP]%20OR%20databases,%20chemical[MH:NOEXP]%20OR%20databases,%20genetic[MH:NOEXP]))&RETMAX=" + str(limit) + "&retmode=XML"
    for pmid in returnIDs(q):
        master.add(pmid)

    print "Downloaded "+str(len(master))+" PubMed IDs."
    #
    # Write Pubmed IDs
    #
    out = open(output_directory+"informatics_resource_pmids.txt","w")

    write(master, out)

    return output_directory+"informatics_resource_pmids.txt"