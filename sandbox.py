
import re
import requests
from functools import lru_cache
from typing import Dict, List, Optional

from tqdm import tqdm
from docx import Document


LREF_PATTERN = re.compile(r'\[LR[^\]]*\]')

CN_BASE_URL = "https://doi.org"
HEADER = {"User-Agent":"python-requests/" + requests.__version__,
        "X-USER-AGENT":"python-requests/" + requests.__version__,
        "Accept":"text/x-bibliography; style = apa; locale = en-Us"}




def extract_references(docx_path:str, pattern: Optional[re.Pattern] = None)-> Dict[str, List[str]]:
    """
    Extracts all the references 
    found in a document path that match the given pattern. The given
    pattern is [LR:doi1;doi2]. A pattern can be changed by providing optional
    pattern argument or modifying LREF_PATTERN global variable.
    What is returned is a dictionary of intext pattern and List of strings
    """
    if pattern is None:
        pattern = LREF_PATTERN
        
    doc = Document(docx_path)
    
    doi_list = list()
    for para in doc.paragraphs:
        # Find all matches in the paragraph text
        matches = LREF_PATTERN.findall(para.text)
        doi_list.extend(matches)
    
    
    reference_dict = {k:k.strip("]").strip("[LR:").split(";") for k in doi_list}
    return reference_dict

@lru_cache(maxsize=256)
def fetch_request(url:str,
                  headers:Optional[Dict[str,str]]=HEADER,
                  )->Optional[str]:
    """
    Interface to the request
    """
    r = requests.get(url,headers=HEADER,allow_redirects=True,) 
    if not r.ok:
        return None
    r.encoding = "UTF-8"
    return r.text
    

def fetch_doi(doi_list:List[str],
              base_url:Optional[str]=CN_BASE_URL,
              headers:Optional[Dict[str,str]]=HEADER,
              )->Dict[str, Optional[str]]:
    """
    Fetches an APA style format of the doi
    """
    doi_dictionary = dict()
    for ids in tqdm(doi_list,"Fetching dois"):
        doi_dictionary[ids] = fetch_request(base_url + "/" + ids.strip())
    return doi_dictionary
        
    """
    for ids in tqdm(doi_list,desc="Fetching dois"):
        url = base_url + "/" + ids.strip()
        
        r = requests.get(url,headers=HEADER,allow_redirects=True,**kwargs) #add kwargs here
        #product 
        if not r.ok:
            doi_dictionary[ids] = None
        else:
            r.encoding = "UTF-8"
            doi_dictionary[ids] = r.text

    return doi_dictionary
    """
    
def intext_cit(literature_citation:str)->str:
    """
    Creates an APA style intext citation from a given string
    
    """
    authors, year =  literature_citation.split("(")[:2]
    year = year.split(")")[0]
    
    author_count = authors.count(".,") + authors.count("&")
    
    first_author = authors.split(",")[0].strip()
    if author_count == 2:
        second_author = " & "+ authors.split("&")[1].split(",")[0].strip()+", "
    # ., counts all authors and & counts last author
    # when there is one author this can be only 0
    elif author_count == 0: 
        first_author = first_author + ","
        second_author = " "
    else:
        second_author = " et al., "
    
    intext_citation = first_author + second_author + year
    return intext_citation 


_path = "testdoc/test.docx"
lrtext_doi = extract_references(_path) #converts it to lrtext_doi

merged_list = list({item for sublist in lrtext_doi.values() for item in sublist})
doi_citation = fetch_doi(merged_list)


#%%
bad_dois = {k:v for k,v in doi_citation.items() if v is None}
good_dois = {k:v for k,v in doi_citation.items() if v is not None}

doi_intext = {k:intext_cit(v) for k,v in good_dois.items()}

#%%
good_replacer = dict()
bad_replacer = dict()
for intext, doi_list in lrtext_doi.items():
    replacement = "("
    one_citation = len(doi_list) == 1
    
    if one_citation:
        joiner = ")"
        end = ""
    else:
        joiner = "; "
        end = ")"
        
    
    for doi in doi_list:
        intext_doi = doi_intext.get(doi,None)
        if intext_doi is None:
            intext_doi = "BAD_DOI:"+doi
        
        replacement = replacement + intext_doi + joiner
    else:
        replacement = replacement.rstrip("; ") + end
    
    if "BAD_DOI" in replacement:
        bad_replacer[intext] = replacement
    else:
        good_replacer[intext] = replacement
    