# -*- coding: utf-8 -*-
from xml.dom import minidom
import os  
import codecs
import re

######################################################
# 
######################################################
def convertWholeReference(r):
    base = re.findall(r'\d+', r)[0]
    n= convertSuffix(r)
    if r != n:
        suf = str(n[n.rfind(".")+1:])
        nr = str(base)+"."+suf
        return float(nr)
    else:
        return float(base)

######################################################
# 
######################################################
def convertSuffix(enum):
    if enum.endswith("a"):
        enum=enum[:-1].strip()+".01"
    if enum.endswith("b"):
        enum=enum[:-1].strip()+".02"
    if enum.endswith("c"):
        enum=enum[:-1].strip()+".03"
    if enum.endswith("d"):
        enum=enum[:-1].strip()+".04"
    if enum.endswith("e"):
        enum=enum[:-1].strip()+".05"
    if enum.endswith("f"):
        enum=enum[:-1].strip()+".06"
    if enum.endswith("g"):
        enum=enum[:-1].strip()+".07"
    if enum.endswith("h"):
        enum=enum[:-1].strip()+".08"
    if enum.endswith("i"):
        enum=enum[:-1].strip()+".09"
    if enum.endswith("j"):
        enum=enum[:-1].strip()+".10"
    if enum.endswith("k"):
        enum=enum[:-1].strip()+".11"
    if enum.endswith("l"):
        enum=enum[:-1].strip()+".12"
    if enum.endswith("m"):
        enum=enum[:-1].strip()+".13"
    if enum.endswith("n"):
        enum=enum[:-1].strip()+".14"
    if enum.endswith("o"):
        enum=enum[:-1].strip()+".15"
    if enum.endswith("p"):
        enum=enum[:-1].strip()+".16"
    if enum.endswith("q"):
        enum=enum[:-1].strip()+".17"
    if enum.endswith("r"):
        enum=enum[:-1].strip()+".18"
    if enum.endswith("s"):
        enum=enum[:-1].strip()+".19"
    if enum.endswith("t"):
        enum=enum[:-1].strip()+".20"
        
    return enum

def read(file):
    
    
    ####################################################################
    #
    # Parses a given PMC article in XML format and extracts article information and references
    #
    ########################################################################################
    
    # Define NULL value 
    NULL = "NULL"
    
    # Lines for output files
    lines_error = []
    lines_output = []
    lines_article = []
    lines_section = []

    #
    reference_hash = {}

    #parse XML file (=ONE article)
    xmldoc = minidom.parse(file)
    file.close()
    
    
    #--------------------------------------------------    
    
    ###############################################    
    ###############################################
    ##
    ## ARTICLE DATA
    ## (Article Meta Data (IDs, Journal Name, Publication Date, etc)
    ##
    ###############################################  
    ###############################################

    pmc_id = NULL
    pubmed_id = NULL
    doi = NULL

    # Parse all article IDs for this XML file
    article_ids = xmldoc.getElementsByTagName('article-id')
    
    for aid in article_ids:
        
        try:
            
            if aid.attributes['pub-id-type'].value == "pmc":
                pmc_id = aid.firstChild.nodeValue
            if aid.attributes['pub-id-type'].value == "pmid":
                pubmed_id = aid.firstChild.nodeValue
            if aid.attributes['pub-id-type'].value == "doi":
                doi = aid.firstChild.nodeValue.replace("\\","")
        except:
            None

    
    #--------------------------------------------------
    
    # Parse name of journal for this article

    journal_ids = xmldoc.getElementsByTagName('journal-id')
    journal_id = ""
    
    # There might be several journal IDs for this article; If available, use the nlm-ta ID
    for jid in journal_ids:
       
        if jid.attributes['journal-id-type'].value == "nlm-ta":
            
            journal_id = jid.firstChild.nodeValue
        else:
            #only wirite alternative jornal name, if nlm-ta not available
            if journal_id == "":
                journal_id = jid.firstChild.nodeValue
    
    #--------------------------------------------------
    
    # Parse (any) publication date for this article
    pub_dates = xmldoc.getElementsByTagName('article-meta')[0].getElementsByTagName('pub-date')
    
    for pdate in pub_dates:
        pub_date = pdate.getElementsByTagName('year')[0].firstChild.nodeValue

    #--------------------------------------------------
    
    # Parse article categories for this article
    art_types = xmldoc.getElementsByTagName('article-categories')
    art_type_str = ""

    if len(art_types)>0:
        
        art_types_sub = art_types[0].getElementsByTagName('subj-group')
        
        if len(art_types_sub)>0:
            
            for art in art_types_sub:
                
                # Normally the article category can be parsed from here
                tmp = art.getElementsByTagName('subject')[0].firstChild.nodeValue
                
                # Sometimes, article category is further nested
                if tmp == None:
                    try:
                        tmp = art.getElementsByTagName('subject')[0].getElementsByTagName('italic')[0].firstChild.nodeValue
                    except:
                        tmp = NULL

                art_type_str = art_type_str + tmp +"; "

    if len(art_type_str)>1:
        art_type_str = art_type_str[:-2].strip()
    
    #--------------------------------------------------
    
    # Clean extracted IDs and names
    
    pmc_id = pmc_id.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
    pubmed_id = pubmed_id.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
    doi = doi.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
    pub_date = pub_date.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
    journal_id = journal_id.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
    art_type_str = art_type_str.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()

    # Write collected information for this article to array
    article_info = pmc_id+"\t"+pubmed_id+"\t"+doi+"\t"+pub_date+"\t"+journal_id+"\t"+art_type_str
    lines_article.append(article_info.replace("\n"," ").strip())


    #--------------------------------------------------
    
    ###############################################    
    ##
    ##  REFERENCES
    ##
    ###############################################


    ###############################################
    # Parse Section and Reference information (position) from FULLTEXT
    ################################################
    #print "Check for body"
    
    body = xmldoc.getElementsByTagName('body')
    
    oldref = ""
    oldsection_cat = ""
    candidate_blocks = {}
    
    if len(body) == 0:
        lines_error.append("warning: "+pmc_id+" does not contain a BODY")
        lines_error.append(str(file))
    
    else:
        #############
        # Go through references at the end of XML document (not inline)
        #############
        try:
            ref_list = xmldoc.getElementsByTagName('ref-list')[0]
        except:
            ref_list = None

        if ref_list != None:
            refs = ref_list.getElementsByTagName('ref')

        else:
            refs = []
            lines_error.append("warning\t"+pmc_id+"\tdoes not contain any references")
            lines_error.append(str(file))
        
        oldref= ""
        
        # There are different ways how to establish reference labels
        # Try them all and decide wihch of them is the preferred one
        candidate_num_label = [] 
        candidate_num_label.append([])
        candidate_num_label.append([])
        candidate_num_label.append([])
        candidate_num_label.append([])
        
        
        # Store the references that can be established for this document
        ESTABLISHED_REFS = []
        LABEL = {}
        
        for ref in refs:
            
            ref_id = ref.attributes['id'].value
            lab = "NOLABEL" 
            
            try:
                for cn in ref.childNodes:
                    if cn.tagName == "label":
                        lab = cn.childNodes[0].data.strip()
            except:
                None

            
            # Iterate over Citation information
            
            iteration = []
            
            if len(ref.getElementsByTagName('citation'))> 0:
                iteration = ref.getElementsByTagName('citation')
                
            if len(ref.getElementsByTagName('mixed-citation'))> 0:
                iteration = ref.getElementsByTagName('mixed-citation')
                
            if len(ref.getElementsByTagName('element-citation'))> 0:
                iteration = ref.getElementsByTagName('element-citation')
            
            old_id = ""
            old_lab = ""
            old_alt_id = ""
            old_alt_lab = ""
            old_pub_s = ""
            old_pub_y = ""
            
            for it in iteration:
                
                alt_id = ref_id
                try:
                    alt_id = it.attributes['id'].value
                except:
                    None
                    
                alt_lab = lab
                try:
                    alt_lab = it.getElementsByTagName('label')[0].firstChild.nodeValue.strip()
                except:
                    None
                
                pubs = []
                try:
                    pubs = it.getElementsByTagName('pub-id')
                except:
                    pubs = []
                if pubs == None:
                    pubs = []     
                    
                pub_y = NULL
                try:
                    pub_y = it.getElementsByTagName('year')[0].firstChild.nodeValue
                except:
                    pub_y = NULL
                if pub_y == None:
                    pub_y = NULL    
                
                pub_s = NULL    
                try:
                    pub_s = it.getElementsByTagName('source')[0].firstChild.nodeValue
                except:
                    pub_s = NULL
                if pub_s == None:
                    pub_s = NULL
   
                num_label = NULL
                if old_id == ref_id and  old_lab == lab and  old_alt_id == alt_id and  old_alt_lab == alt_lab:
                    # DUPLICATE 
                    
                    if pub_y == NULL:
                        pub_y = old_pub_y
                    if pub_s == NULL:
                        pub_s = old_pub_s
                
                else:
                    try:
                        num_label = convertWholeReference(ref_id)    
                    except:
                        num_label = NULL
                    
                    candidate_num_label[0].append(num_label)
                    
                    num_label = NULL
                    try:
                        num_label = convertWholeReference(alt_id)
                    except:
                        # NO CONVERSION OF NUM LABEL 
                        num_label = NULL
                    candidate_num_label[1].append(num_label)
                       
                    num_label = NULL
                    try:
                        num_label = convertWholeReference(lab)
                    except:
                        # NO CONVERSION OF NUM LABEL 
                        num_label = NULL
                    candidate_num_label[2].append(num_label)
                        
                    num_label = NULL
                    try:
                        num_label = convertWholeReference(alt_lab)
                    except:
                        num_label = NULL
                        # NO CONVERSION OF NUM LABEL 
                    candidate_num_label[3].append(num_label)
                

                old_id = ref_id
                old_lab =lab
                old_alt_id = alt_id
                old_alt_lab =alt_lab  
                old_pub_s = pub_s
                old_pub_y = pub_y           
    
    
                pmc_id = pmc_id.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
                ref_id = ref_id.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
                pub_s = pub_s.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
                pub_y = pub_y.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
               
               
               
                if len(pubs)>0:
                    for p in pubs:
                        pub_t = NULL
                        try:
                            pub_t = p.attributes["pub-id-type"].value
                            pub_t = pub_t.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
                        except:
                            None
                            
                        pub_id = NULL
                        try:
                            pub_id = p.firstChild.nodeValue
                            pub_id = pub_id.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
                        except:
                            None
                        
                        ESTABLISHED_REFS.append(pmc_id+"\t"+ref_id+"\t"+alt_id+"\t"+lab+"\t"+alt_lab+"\t"+pub_s+"\t"+pub_y+"\t"+pub_id+"\t"+pub_t )
                
                else:
                    ESTABLISHED_REFS.append(pmc_id+"\t"+ref_id+"\t"+alt_id+"\t"+lab+"\t"+alt_lab+"\t"+pub_s+"\t"+pub_y+"\t"+NULL+"\t"+NULL)
                
        
        
                
        master = -1
        masters = set()
        
        i = 0
        for c in candidate_num_label:
            consider = True
            if NULL in c:
                consider = False
            else:
                old = -1
                for ci in c:
                    if ci==old:
                        consider = False
                        break
                    old = ci
                    
            if consider==True:
                masters.add(i)
            i=i+1   
        
        
        #USE labels if there are labels
        if 1 in masters:
            master = 1
        if 0 in masters:
            master = 0
        if 2 in masters:
            master = 2
        if 3 in masters:
            master = 3


        ESTABLISHED_REFS2 = []
        
        for l in ESTABLISHED_REFS:
            if master > -1:
                l = l + "\t"+ str(convertWholeReference(l.split("\t")[master+1]))
                LABEL[l.split("\t")[1]] =str(convertWholeReference(l.split("\t")[master+1]))
            else:
                l = l + "\t"+NULL
            ESTABLISHED_REFS2.append(l)
        
        ESTABLISHED_REFS = ESTABLISHED_REFS2
        
        
        
        
        
        
        
        
        sections2 = body[0].childNodes
        section_cat = NULL
 
        if len(sections2)>0:

            for s in sections2:

                #check whether element is section 
                try:
                    s.tagName
                    try:
                        section_cat = s.attributes['sec-type'].value.replace("\t"," ").replace("\n"," ").replace("  "," ")
                    except:
                        section_cat = NULL

                    if section_cat == NULL:
                        try:
                            title = s.getElementsByTagName('title')
                            section_cat = "RESC_"+str(title[0].firstChild.nodeValue).value.replace("\t"," ").replace("\n"," ").replace("  "," ")
                           
                            lines_error.append("warning\t"+pmc_id+"\tsection type inferred for "+str(s.tagName))
                            lines_error.append(str(file))
                        except:
                            None   
            
                    try:
                        lines_section.append(pmc_id+"\t"+section_cat)
                    except:
                        lines_section.append(pmc_id+"\tERROR" )
                    
                    #GO through the xrefs in the given section
                    xrefs = s.getElementsByTagName('xref')
                    
                    for xr in xrefs:
                        if xr.attributes['ref-type'].value == "bibr" or xr.attributes['ref-type'].value == "bib":
                            xref_id = xr.attributes['rid'].value
                           
                            if " " in xref_id:
                                xref_ids = xref_id.split(" ")
                                
                                for xref_id in xref_ids:
                                    lines_error.append("warning\t"+pmc_id+"\tresolution of inline enumeration for "+xref_id)
                                    lines_error.append(str(file))
                                    
                                    if xref_id not in reference_hash:
                                        reference_hash[xref_id] = set()
                                        
                                    reference_hash[xref_id].add(section_cat)
                                    oldref = xref_id
                                    oldsection_cat = section_cat
                            else:
                                if xref_id not in reference_hash:
                                    reference_hash[xref_id] = set()
                                reference_hash[xref_id].add(section_cat)
                             
                                if len(LABEL) > 0:
                                
                                    if oldref != "":
                                        # TRY BLOCK BUSINESS
                                        try:
                                            candidate2 = float(LABEL[xref_id])
                                            candidate  = float(LABEL[oldref])   
                                            
                                            if candidate2-candidate>.01 :
                                                cand = str(oldref)+"|"+str(xref_id)
                                                
                                                if cand not in candidate_blocks:
                                                    candidate_blocks[cand]=set()
                                                if section_cat==oldsection_cat:
                                                    candidate_blocks[cand].add(section_cat)
                                        except:
                                            None
                                        
                                oldref = xref_id
                                oldsection_cat = section_cat
                            
                except:
                    lines_error.append("warning\t"+pmc_id+"\tcomment elements")
                    lines_error.append(str(file))


        ############################################################
        #
        # Those references directly under body       
        #     
        ############################################################
        
        xrefs = body[0].getElementsByTagName('xref')
        
        section_cat = NULL

        for xr in xrefs:

            if 'ref-type' in xr.attributes.keys() and (xr.attributes['ref-type'].value == "bibr" or xr.attributes['ref-type'].value == "bib"):
                
                try:
                    xref_id = xr.attributes['rid'].value
                    
                    if " " in xref_id:
                        xref_ids = xref_id.split(" ")
                        
                        for xref_id in xref_ids:
                            if xref_id not in reference_hash:
                                lines_error.append("warning\t"+pmc_id+"\tresolution of inline enumeration for "+xref_id)
                                lines_error.append(str(file))
                                reference_hash[xref_id] = set()
                                reference_hash[xref_id].add(section_cat)
                                         
                    else:
                        if xref_id not in reference_hash:
                            reference_hash[xref_id] = set()
                            reference_hash[xref_id].add(section_cat)
                except:
                    lines_error.append("warning\t"+pmc_id+"\thas one reference without rid")
                    lines_error.append(str(file))

        if len(reference_hash)==0:
            lines_error.append("warning\t"+pmc_id+"\tdoes not contain any references with bibr / bib tag")
            lines_error.append(str(file))
            
            
        #-------------------------------------------------------------------      
        
        #############
        # Go through refrences at the end of XML document (not inline)
        #############
        
        try:
            ref_list = xmldoc.getElementsByTagName('ref-list')[0]
        except:
            ref_list = None

        if ref_list != None:
            refs = ref_list.getElementsByTagName('ref')
        else:
            refs = []
            lines_error.append("warning\t"+pmc_id+"\tdoes not contain any references")
            lines_error.append(str(file))


        #-------------------------------------------------------------------  


        #print "Go through blocks "
        blocksRAW = open(str(file.name),"r").read().replace("\n","").replace(" ","") 
        blocks1 = blocksRAW.split(">-<")
        blocks2 = blocksRAW.split(">&#x02013;<")
        blocks3 = blocksRAW.split(">&#x02212;<")

        blocks = []
        
        if len(blocks1)>1:
            for b in blocks1:
                blocks.append(b.strip())
 
        if len(blocks2)>1:
            for b in blocks2:
                blocks.append(b.strip())
  
        if len(blocks3)>1:
            for b in blocks3:
                blocks.append(b.strip())

        
        #######################
        # Precalculate blocks
        ###########################
        
        precalculated_blocks  = []

        if len(blocks)>1:
            
            for i in range(1,len(blocks)):
 
                try:
                    blocke1 = blocks[i-1][blocks[i-1].rfind("<xref"):]
                    blocke2 = blocks[i][0:blocks[i].find("</xref")+7]        
                    blocke1 = blocke1.replace("&#x0005b;","[").replace("&#x0005d;","]")
                    blocke2 = blocke2.replace("&#x0005d;","]").replace("&#x0005b;","[")

                    if ((blocks[i-1].endswith("/xref") and blocks[i].startswith("xref")) or (blocks[i-1].endswith("/xref><sup") and blocks[i].startswith("/sup><xref"))) and   ("\"bibr\"" in blocke1 or "\"bib\"" in blocke1) and ("\"bibr\"" in blocke2 or "\"bib\"" in blocke2):
                    
                        l = re.findall(r'\>\[?\d+[a-z]?\]?\<',blocke1)
                        
                        if len(l)>0 :
                            
                            l_extract = re.findall(r'\d+[a-z]?', l[0])
                            if len(l_extract)>0 :

                                lower = convertWholeReference(l_extract[0])
                                l = re.findall(r'\>\[?\d+[a-z]?\]?\<',blocke2)
                                
                                if len(l)>0 :
                                    
                                    l_extract = re.findall(r'\d+[a-z]?', l[0])
                                    if len(l_extract)>0 :
                                        
                                        upper =  convertWholeReference(l_extract[0])
                                           
                                        lowerref = blocks[i-1][blocks[i-1].rfind("rid=")+5:]
                                        lowerref = lowerref[0:lowerref.find("\"")]   
                                        upperref = blocks[i][blocks[i].find("rid=")+5:]
                                        upperref = upperref[0:upperref.find("\"")]
                        
                                        if str(lowerref)+"|"+str(upperref) in candidate_blocks:
                                            
                                            ses = candidate_blocks[str(lowerref)+"|"+str(upperref)]
                                            
                                            tmp = {}
                                            tmp["lower"]=lower
                                            tmp["upper"]=upper
                                            tmp["lowerref"]=lowerref
                                            tmp["upperref"]=upperref
                                            tmp["candidate_blocks"]=set()
                                            for se in ses:
                                                tmp["candidate_blocks"].add(se)
                                            precalculated_blocks.append(tmp)
                
                except:
                    lines_error.append("error\t"+pmc_id+"\t"+ref_id+" WITH PRECALCULATED BLOCKS")                
                    print "ERROR WITH PRECALCULATED BLOCKS "  +pmc_id+"\t"+ref_id
        
        #######################
        # Loop through refs and blocks
        ###########################
        
        for ref in ESTABLISHED_REFS:
        
            ref_id = ref.split("\t")[1]
            pmc_id = ref.split("\t")[0]
            num_id = None
            try:
            
                num_id = float(ref.split("\t")[9])
            except:
                None

            if len(precalculated_blocks)>0:
            
                for i in range(0,len(precalculated_blocks)):

                    if num_id != None:
                        try:
                            
                            blocke1 = blocks[i-1][blocks[i-1].rfind("<xref"):]
                            blocke2 = blocks[i][0:blocks[i].find("</xref")+7]
                            candidate =  num_id 
                            
                            if candidate > precalculated_blocks[i]["lower"] and candidate < precalculated_blocks[i]["upper"]:

                                if ref_id not in reference_hash:
                                    reference_hash[ref_id] = set()
                                    
                                for se in precalculated_blocks[i]["candidate_blocks"]:
                                        
                                    if (len(reference_hash[ref_id])==0):
                                        lines_error.append("warning\t"+pmc_id+"\t"+ref_id+" not referenced in text but inferred from enumeration")
                                    else:
                                        lines_error.append("warning\t"+pmc_id+"\t"+ref_id+" inferred from enumeration")
                                    
                                    reference_hash[ref_id].add(se)
                                    lines_error.append(str(file))
                                
                        except:
                            print "ERROR\t"+str(ref_id)+"\t"+pmc_id
                            lines_error.append("error\t"+pmc_id+"\t aborted")
                            lines_error.append(str(file))
                            #sys.exit()
    
    
            if ref_id not in reference_hash:
            
                lines_error.append("warning\t"+pmc_id+"\t"+ref_id+" in reference set but not referenced in text")
                lines_error.append(str(file))
                
                reference_hash[ref_id] = set()
                reference_hash[ref_id].add("NOT_FOUND_IN_TEXT")
            
            
            #### return lines by categories
            
            for cat in reference_hash[ref_id]:
                
                cat    = cat.replace("\n"," ").replace("\t"," ").replace("  "," ").strip()
    
                ref_parts = ref.split("\t")
                new_ref_id = ref_parts[1]
                
                if (ref_parts[9]!=NULL):
                    new_ref_id = new_ref_id+"_"+str(ref_parts[9])
                
                rstr = ref_parts[0]+"\t"+new_ref_id+"\t"+cat+"\t"+ref_parts[5]+"\t"+ref_parts[6]+"\t"+ref_parts[8]+"\t"+ref_parts[7]
            
                lines_output.append(rstr)

    return lines_error,  lines_output, lines_article, lines_section

def call(fn, citations_fh, article_info_fh, article_sections_fh, error_fh):
    try:

        myfile = open(fn,"r")
        error, data, article, sections = read(myfile)

        ################################
        # Write to output files
        ################################

        if len(data)>0:
            for l in data:
                citations_fh.write(l + "\n")
     
        if len(article)>0:
            for l in article:
                article_info_fh.write(l + "\n")

        if len(error)>0:    
            for l in error:
                error_fh.write(l + "\n")
                
        if len(sections)>0:    
            for l in sections:
                article_sections_fh.write(l + "\n")
    except:
        error_fh.write("iERROR\t" + str(fn) + "\n")

def run(input_dir, output_dir):
    citations_fh =          codecs.open(output_dir+"pmc_reference_citations.txt","w", "utf-8")
    article_info_fh =  codecs.open(output_dir+"pmc_reference_article.txt","w", "utf-8")
    article_sections_fh = codecs.open(output_dir+"pmc_reference_sections.txt","w", "utf-8")
    error_fh =   codecs.open(output_dir+"pmc_reference_error.txt","w", "utf-8")

    for root, subFolders, files in os.walk(input_dir):
        try:
            for f in files:
                print "Processing: "+os.path.join(root,f)
                call(os.path.join(root,f), citations_fh, article_info_fh, article_sections_fh, error_fh)

        except:
            error_fh.write("eERROR\t"+str(root)+"\n")

    citations_fh.close()
    article_info_fh.close()
    article_sections_fh.close()
    error_fh.close()

    return output_dir+"pmc_reference_article.txt", output_dir+"pmc_reference_citations.txt", output_dir+"pmc_reference_sections.txt"
    