import re
import os
import imp

cwd = os.path.dirname(os.path.abspath(__file__))

detect = imp.load_compiled("detect",cwd+"/lib/detect.pyc")

# ACRONYMS that should not be confused with tool names (to be continued)
BLACKLIST = set()
BLACKLIST.add("DNA")
BLACKLIST.add("Y2K")

###########################
# Clean term
# e.g., trailing ".", brackets, etc.
############################
def clean(t):
    
    t = t.strip()
    if t.endswith("."):
        t = t[0:-1].strip()
    if t.startswith("[") and  t.endswith("]"):
        t = t[1:len(t)-1].strip()
    if t.startswith("\"") and  t.endswith("\""):
        t = t[1:len(t)-1].strip()
    if t.endswith("."):
        t = t[0:-1].strip()
    return t


###########################################
#
# EXTRACTION FUNCTIONS
# * LAST TOKEN (usually a good candidate for a tool name (context dependent)
# * FIRST TOKEN (usually a good candidate for a tool name (context dependent)
# * Software patterns (I+II)
# * Database patterns
#
##############################################


def extractLastToken(l):
    
    cand = ""
    cand_code =""
    
    if " " in l.lower():
        cand = l.split(" ")[len(l.split(" "))-1]
        CONTEXT = l.split(" ")[len(l.split(" "))-2].lower()
        
        if CONTEXT == "using" or CONTEXT == "with" or CONTEXT == "through" or CONTEXT == "called" or CONTEXT == "to" or CONTEXT == "in" or CONTEXT == "by" or CONTEXT == "database" or CONTEXT == "software" or CONTEXT == "tool" or CONTEXT == "system" :
               
            caps_count = 0
                         
            for c in cand:
                if c.isupper():
                    caps_count= caps_count+1
             
            if (caps_count<2) or cand in BLACKLIST:
                cand = ""
            else:
                cand_code = "LAST_TOKEN"
                 
                if cand.startswith("(") and cand.endswith(")"):
                    cand = cand[1:-1]
                if cand.endswith("?"):
                    cand = cand[:-1]
        else:
            cand = ""
    return cand_code+"|"+cand

def extractColon(l,breakpoint,space):
    cand = ""
    cand_code =""
    
    success = 0
    
    if breakpoint+space in l:
    
        if breakpoint!="," or l.split(breakpoint+space)[1].startswith("a ") or l.split(breakpoint+space)[1].startswith("an ") or l.split(breakpoint+space)[1].startswith("the "):
           
            cand_code = "COLON"
            
            LEFTOFCOLON = l.split(breakpoint+space)[0]
            
            if " " not in LEFTOFCOLON:
                
                cand = LEFTOFCOLON
                cand_code = "COLON_SINGLE"

                if cand in BLACKLIST:
                    cand = ""
                    cand_code = "COLON"
                else:
                    success = 1
                
                
            if len(l.split(breakpoint+space)[0].split(" "))==2:
                
                    cand = l.split(breakpoint+space)[0].split(" ")[1]
    
                    newa = re.sub(r"\(?(v|V)?[0-9]*\.?([0-9]+|V|I|II|III|IV|X)\)?","",cand).strip()
                    if newa == "":
                        cand = l.split(breakpoint+space)[0].split(" ")[0]
                        cand_code = "COLON_SINGLE_SUFFIX"
                        success = 1
                        
                    if success == 0:  
                        cand = l.split(breakpoint+space)[0].split(" ")[1]
                        
                        if cand == "database" or cand == "update":
                            cand = l.split(breakpoint+space)[0].split(" ")[0]
                            cand_code = "COLON_SINGLE_SUFFIX"
                            success = 1
                            
                            
                    if success == 0:  
                        #BEFORE BREAKPOINT two tokens Both start with capital letter, at least two letters each, first not a gerund
                        
                        first = l.split(breakpoint+space)[0].split(" ")[0]
                        second = l.split(breakpoint+space)[0].split(" ")[1]
                        
                        if first[0].isupper() and second[0].isupper() and not first.endswith("ing") and len(first)>1 and not first.lower().startswith("toward") and not first.lower().startswith("beyond"):
                        
                            if breakpoint!="," or l.split(breakpoint+space)[1].startswith(", a ") or l.split(breakpoint+space)[1].startswith(", an ") or l.split(breakpoint+space)[1].startswith(", the "):
                            
                                cand = l.split(breakpoint+space)[0].strip()
                                
                                if first == "The":
                                    cand = second
                                
                                cand_code = "COLON_DOUBLE_BOTH_C"
                                success = 1
                            
                    if success == 0:
                        cand = ""
                        cand_code = "COLON_SINGLE_SUFFIX_TBD"
            
            if success ==0:
                reobj = re.compile('([A-Z]+[a-z]+[A-Z]+[a-zA-Z]+)')
                result = reobj.findall(LEFTOFCOLON)

                if len(result)>0:
                    for link in result:
                        cand = cand+link+"/"
        
                    cand = cand[:-1]
                    cand_code = "COLON_PATTERN"
                    success = 1
                else:
                    cand=""
                
                    
    return cand_code+"|"+cand


def extractSoftware(l):
    
    cand = ""
    cand_code =""
    
    success = 0
    
    if "software" in l.lower():

        cand_code = "SOFT"
  
        if success == 0:
            
            if "(" in l and ")" in l:
                m = re.search('\([A-Z][a-zA-Z]*[A-Z][a-zA-Z]+\)', l)
                try:
                    cand=m.group(0)[1:-1]
                    cand_code = "SOFT_TOKEN_CAPITAL_BRACKETS"
                    success = 1
                except:
                    cand=""

    return cand_code+"|"+cand


def extractDatabaseBroad(l):
    
    cand = ""
    cand_code =""

    m = re.search('(T|t)he (.){3,50} (((d|D)atabase)|((r|R)epository)|((k|K)nowledgebase)|((b|B)rowser)|((w|W)ebsite)|((a|A)rchive)|((r|R)egistry)|((c|C)ompendium)|((r|R)esource)|((d|D)ata (w|W)arehouse)|((p|P)roject))', l)
    try:
        cand=m.group(0)
        
        if not " of " in cand and not " for " in cand and not " in " in cand and not " its " in cand and not " with " in cand and not " through " in cand and not ". " in cand:
            start = cand.lower().rfind("the ")
            cand=cand[start+4:]
            if ":" in cand:
                cand = cand[:cand.find(":")]
            if "--" in cand:
                cand = cand[:cand.find("--")]
        
            up =0
            for tok in cand.split(" "):
                if tok[0].isupper():
                    up = 1
            if up ==1:
                cand_code = "DB_REGEXP_BROAD"
            else: 
                cand = ""
        
    except:
        cand=""    
                  
    return cand_code+"|"+cand

def extractAcro(l):
    
    cand = ""
    cand_code =""
    
    success = 0

    for c in detect.findCandidates(l):
        cand = cand+c+"/"
        success = 1
    if success == 1:
        cand_code = "ACRONYM"
    else:
        cand = ""
                    
    return cand_code+"|"+cand


def extractDatabase(l):
    
    cand = ""
    cand_code =""
    
    success = 0
    
    if "database" in l.lower() or  "data base" in l.lower() :
        
        cand_code = "DB"

        if success == 0:
            
            if "(" in l and ")" in l:
                m = re.search('\([A-Z][a-zA-Z]*[A-Z][a-zA-Z]+\)', l)
                try:
                    cand=m.group(0)[1:-1]
                    cand_code = "DB_TOKEN_CAPITAL_BRACKETS"
                    success = 1
                except:
                    cand=""


        if success == 0:
            m = re.search('((T|t)he ).*[d|D]ata ?[b|B]ase(?!s)', l)
         
            try:
                cand=m.group(0)
                
                if not " of " in cand and not " for " in cand and not " in " in cand and not " its " in cand and not " with " in cand and not " through " in cand and not ". " in cand:
                    start = cand.lower().rfind("the ")
                    cand=cand[start+4:]
                    if ":" in cand:
                        cand = cand[:cand.find(":")]
                    if "--" in cand:
                        cand = cand[:cand.find("--")]
                    cand_code = "DB_TOKEN_CAPITAL_INSIDE"
                    success = 1
                else:
                    cand=""
            except:
                cand=""   

    return cand_code+"|"+cand

def run(output_directory, in_fp):

    out = open(output_directory+"informatics_resource_extracted_names.txt","w")
    inf = open(in_fp, "rU")
    nl = sum(1 for _ in inf)
    for l in inf.readlines():
        pmid = l.split("\t")[0]
        title = clean(l.split("\t")[1].strip())

        extracted = extractColon(title,":"," ")
        if extracted.split("|")[1] == "":
            extracted = extractColon(title,"--","")
        if extracted.split("|")[1] == "":
            extracted = extractColon(title,","," ")
        if extracted.split("|")[1] == "":
            extracted = extractDatabase(title)
        if extracted.split("|")[1] == "":
            extracted = extractSoftware(title)
        if extracted.split("|")[1] == "":
            extracted = extractDatabaseBroad(title)
        if extracted.split("|")[1] == "":
            extracted = extractLastToken(title)

        if not re.match("[0-9][0-9][0-9][0-9].*",extracted.split("|")[1]):
            out.write(pmid+"|"+extracted.lower()+"|"+title+"\n")
    print "Extracted resource names from "+str(nl)+" PubMed records."
    out.close()
    return output_directory+"informatics_resource_extracted_names.txt"