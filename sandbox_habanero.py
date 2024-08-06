
import requests
from typing import Dict, List, Optional
from tqdm import tqdm

CN_BASE_URL = "https://doi.org"
HEADER = {"User-Agent":"python-requests/" + requests.__version__,
        "X-USER-AGENT":"python-requests/" + requests.__version__,
        "Accept":"text/x-bibliography; style = apa; locale = en-Us"}




all_dois=['[LREF: https://doi.org/10.1016/S0145-2126(01)00197-7]', '[LREF:https://doi.org/10.1038/s41467-021-21733-z]', '[LREF:https://doi.org/10.1093/humupd/dml009]', '[LREF:doi: 10.1111/j.2047-2927.2014.00193.x]', '[LREF: 10.1038/ncomms7684 ]', '[LREF: https://doi.org/10.1523/JNEUROSCI.5654-07.2008]', '[LREF:https://doi.org/10.1098/rstb.2020.0509]', '[LREF: https://doi.org/10.1101/2022.02.16.480748]', '[LREF:doi: 10.1016/j.rbmo.2016.06.006.]', '[LREF:https://doi.org/10.1038/s41380-023-02113-z]', '[LREF: https://doi.org/10.1186/s12864-022-08760-w]', '[LREF: https://doi.org/10.1016/j.jmb.2013.07.015]', '[LREF: https://doi.org/10.1038/nrg2958]', '[LREF: 10.1016/s0092-8674(01)00504-9]', '[LREF: https://doi.org/10.1038/sj.bjp.0706825]', '[LREF: https://doi.org/10.1186/s40348-015-0014-6]', '[LREF: https://doi.org/10.1186/s13059-019-1720-5]', '[LREF: doi:10.1146/annurev.genom.9.081307.164217]', '[LREF: 10.1038/nrg3373]', '[LREF: https://doi.org/10.1101/gr.187187.114]', '[LREF: https://doi.org/10.1073/pnas.1913688117]', '[LREF: https://doi.org/10.1186/1471-2148-12-9]', '[LREF:https://doi.org/10.1186/1471-2148-12-9]', '[LREF:https://doi.org/10.1038%2Fncb1911]', '[LREF:doi: 10.1152/ajpendo.00401.2011]', '[LREF:https://doi.org/10.1186/s13059-019-1720-5]', '[LREF: doi: 10.1038/nprot.2008.211]', '[LREF:https://doi.org/10.1371/journal.pgen.1004830]', '[LREF: https://doi.org/10.1016/j.tibtech.2019.02.003]', '[LREF:doi: 10.1093/ije/dyv166]', '[LREF: 10.1038/nbt.2303]', '[LREF:doi: 10.1093/nar/28.22.4474]', '[LREF:doi: 10.1093/molehr/gat021]', '[LREF: https://doi.org/10.1016/j.ajhg.2021.03.016]', '[LREF:DOI: 10.1126/science.aau5656]', '[LREF: 10.1038/s41586-020-2287-8]', '[LREF:https://doi.org/10.1093/gigascience/giab074]', '[LREF: https://doi.org/10.1093/bioinformatics/btu170]', '[LREF:doi: 10.1016/j.mayocp.2018.03.020]', '[LREF: doi:10.1016/j.tig.2012.03.002]', '[LREF: https://doi.org/10.14806/ej.17.1.200]', '[LREF: https://doi.org/10.1371/journal.pgen.1004830]', '[LREF:https://doi.org/10.1073/pnas.1106896108]', '[LREF: doi:10.1111/mec.14877 ]', '[LREF:https://doi.org/10.24272/j.issn.2095-8137.2022.481]', '[LREF: 10.1038/nrg.2015.25]', '[LREF: https://doi.org/10.24272/j.issn.2095-8137.2022.481]', '[LREF:https://doi.org/10.1098/rstb.2016.0442]', '[LREF: 10.1038/gim.2017.86 ]', '[LREF: doi: 10.1038/ng2123]', '[LREF: 10.1038/nature15393 ]', '[LREF:10.1186/gb-2007-8-9-227]', '[LREF:10.1038/nsmb.1821]', '[LREF:https://doi.org/10.1111/mec.14877]', '[LREF: 10.1101/gr.107680.110]', '[LREF:doi: 10.1097/MCO.0b013e32834121b1]', '[LREF: https://doi.org/10.1152/ajpregu.00320.2009]', '[LREF: https://doi.org/10.3389/fgene.2022.1060898]', '[LREF: doi: 10.3390/molecules26216706]', '[LREF:doi: 10.1016/s0092-8674(01)00504-9]', '[LREF:https://doi.org/10.1371/journal.pone.0110963]', '[LREF: https://doi.org/10.1016/j.tig.2012.03.002]', '[LREF:https://doi.org/10.1101/gr.206938.116]', '[LREF: https://doi.org/10.1093/bioinformatics/btp352]', '[LREF: DOI: 10.1126/science.aau5656]', '[LREF:doi: 10.1016/j.aju.2017.12.004]', '[LREF: https://doi.org/10.1073/pnas.252626599]', '[LREF:https://doi.org/10.1146/annurev.genom.9.081307.164217]', '[LREF:doi: 10.1097/NNR.0000000000000037]', '[LREF: https://doi.org/10.1093/gigascience/giab074]', '[LREF: https://doi.org/10.1093/molbev/mst136]', '[LREF:https://doi.org/10.1016/j.ajhg.2021.03.016]', '[LREF: doi: https://doi.org/10.1242/jeb.208835]', '[LREF: 10.1073/pnas.1106896108]', '[LREF:10.1038/nature08162]', '[LREF: https://doi.org/10.1093/gbe/evz148]', '[LREF: https://doi.org/10.1098/rstb.2020.0509]', '[LREF: 10.1534/genetics.117.1114]', '[LREF:doi: 10.1002/em.22233]', '[LREF:https://doi.org/10.1016/s0960-9822(98)70105-8]', '[LREF: 10.1371/journal.pbio.2001333 ]', '[LREF: 10.1016/j.csbj.2020.07.018]', '[LREF: 10.3389/fgene.2022.1060898]', '[LREF:https://doi.org/10.1038/s41467-024-48917-7]', '[LREF:https://doi.org/10.1101/gr.187187.114]', '[LREF:https://doi.org/10.1038/ncomms7684]', '[LREF: 10.1146/annurev.genom.9.081307.164217]', '[LREF:doi: https://doi.org/10.1242/jeb.208835]', '[LREF: https://doi.org/10.1093/bioinformatics/bty350]', '[LREF: 10.1093/bib/bbs086]', '[LREF: https://doi.org/10.1111/mec.14877]', '[LREF:https://doi.org/10.1073/pnas.1109272108]', '[LREF: https://doi.org/10.1093/bfgp/elv014 ]', '[LREF:doi: 10.1101/gr.187187.114]', '[LREF: https://doi.org/10.2147/NSS.S56077]', '[LREF: 10.3390/genes12121958]', '[LREF: 10.1073/pnas.252499499]', '[LREF: DOI: 10.1101/gr.177121.114]', '[LREF: https://doi.org/10.1038/nmeth.1923]']




doi_list = [x.strip("[LREF:").strip("]") for x in all_dois]

def fetch_doi(doi_list:List[str],base_url:Optional[str]=CN_BASE_URL,
              **kwargs):
    """
    Fetches an APA style format of the doi
    """

    doi_dictionary = dict()
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
#%%
morko = fetch_doi(doi_list)
#%%

bad = {k:v for k,v in morko.items() if v is None}
bad = list(bad.keys())




