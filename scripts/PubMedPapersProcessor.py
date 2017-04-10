'''
@author: winnenbr
@author: alisoncallahan
'''
import urllib2
from xml.dom import minidom

def returnTitles(pmid_list):

    retts = []
    retsa = []
    retsd = []
    retsh = []
    retjs = []
    
    ids = ""
    for i in pmid_list:
        ids = ids+str(i)+","

    url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="+ids+"&retmode=xml"
    response = urllib2.urlopen(url)
    xmldoc = minidom.parse(response)
    
 
    medlines = xmldoc.getElementsByTagName('MedlineCitation')

    # For all articles in this batch extract the following:
    # * pmid
    # * title
    # * journal name
    # * list of authors' last names
    # * publication date(s)
    # * MeSH terms from index
    
    for m in medlines:
        
        try:
            rett = "" # title
            retd = "" # date
            reta = "" # author
            reth = "" # mesh headings
            retj = "" # journal
            
            
            # Get PMID
            article_id = m.getElementsByTagName('PMID')[0].firstChild.nodeValue
            rett=rett+article_id+"\t"
            reta=reta+article_id 
            retd=retd+article_id +"\t"
            retj=retj+article_id +"\t"
            reth=reth+article_id 
           
           
            # Get TITLE    
            article_title = m.getElementsByTagName('ArticleTitle')[0].firstChild.nodeValue.replace("\t"," ").replace("\n"," ").strip()
            rett = rett+(article_title)
            retts.append(rett)
              
                
            # Get Journal Name (MedlineTA)
            journal = m.getElementsByTagName('MedlineTA')[0].firstChild.nodeValue.replace("\t"," ").replace("\n"," ").strip()
            #for a in journals:
            retj = retj+journal
            retjs.append(retj)
            
            
            # Get ALL AUTHOR LAST NAMES
            author_lns = m.getElementsByTagName('LastName')
            for ln in author_lns:
                reta = reta+"\t"+(ln.firstChild.nodeValue.replace("\t"," ")).strip()
            retsa.append(reta)
    
    
            # Get publication date(s)
            article_dates = m.getElementsByTagName('PubDate')
            for a in article_dates:
                for b in a.getElementsByTagName('Year'):
                    retd = retd+(b.firstChild.nodeValue.replace("\t"," ").replace("\n"," ")).strip()
                    
                for b in a.getElementsByTagName('MedlineDate'):
                    retd = retd+(b.firstChild.nodeValue.replace("\t"," ").replace("\n"," ")).strip()[0:4]

                retsd.append(retd)
    
    
            # Get MeSH headings
            mesh_h = m.getElementsByTagName('MeshHeading')

            for a in mesh_h:
                dname = ""
                for b in a.getElementsByTagName('DescriptorName'):
                    fc = b.firstChild
                    dname = (fc.nodeValue.replace("\t"," ").replace("\n"," ")).strip()
                    major = (b.attributes["MajorTopicYN"].value.strip())
                    reth = reth+"\t"+dname+"/"+major+"/"
                    
                for c in a.getElementsByTagName('QualifierName'):
                    fc = c.firstChild
                    qname = (fc.nodeValue.replace("\t"," ").replace("\n"," ")).strip()
                    major = (c.attributes["MajorTopicYN"].value.strip())
                    reth = reth+"\t"+dname+"/"+major+"/"+qname
            retsh.append(reth.strip())
        except:
            print "Error with extracting from XML file for "
            print article_id
            
    return retts, retsa, retsd, retsh, retjs

def run(output_fp, pmids_fp, CHUNK_SIZE=200):
    ##############################################################################
    ##
    ## Create tab delimited files that can be loaded into SQL tables
    ## (XML files (each for a batch of PubMed Articles) -> tab-files )
    ##
    ##############################################################################

    CHUNK_SIZE = 200
    COLUMN_SEPARATOR = "," #= "\t"

    ids = []

    out_titles   = open(output_fp+"informatics_resource_titles.txt","w" )
    out_authors  = open(output_fp+"informatics_resource_authors.txt","w" )
    out_dates    = open(output_fp+"informatics_resource_dates.txt","w" )
    out_meshs    = open(output_fp+"informatics_resource_meshs.txt","w" )
    out_journals = open(output_fp+"informatics_resource_journals.txt","w" )

    for l in open (pmids_fp,"r"):

        pid = l.strip().split(COLUMN_SEPARATOR)[0]

        #skip header
        if pid!="PMID":
            ids.append(pid)

    for i in range(0,(len(ids)/CHUNK_SIZE)+1):

        start = CHUNK_SIZE*i
        end = ((i+1)*CHUNK_SIZE)

        if len(ids)<end:
            end = len(ids)

        data = []
        for j in range(start, end):
            data.append(ids[j])
        print "Processing records "+str(start)+" - "+str(end)+"."

        titles, authors, dates, meshs, journals = returnTitles(data)

        try:
            for l in titles:
                out_titles.write(l.encode('utf8').strip()+"\n")
            for a in authors:
                out_authors.write(a.encode('utf8').strip()+"\n")
            for d in dates:
                out_dates.write(d.encode('utf8').strip()+"\n")
            for j in journals:
                out_journals.write(j.encode('utf8').strip()+"\n")
            for h in meshs:
                mes  = h.split("\t")
                for i in mes[1:]:
                    out_meshs.write(mes[0]+"|"+i.encode('utf8').strip()+"\n")
        except:
            print "Error with:"
            print mes[0]

    print "Processed "+str(len(ids)) +" PubMed records."
    out_titles.close()
    out_authors.close()
    out_dates.close()
    out_meshs.close()
    out_journals.close()
    return output_fp+"informatics_resource_titles.txt", output_fp+"informatics_resource_dates.txt"