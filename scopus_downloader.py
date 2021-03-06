
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib
import requests
import json
import xml.etree.ElementTree as ET

infilename='C:/Users/jbishoff/Desktop/reduced_Corpus.txt'
outfilename= 'C:/Users/jbishoff/Desktop/Corpus_with_abstracts.txt'
scopus_api_key = 'INSERT_API_KEY_HERE'
infile=open(infilename,'r', encoding='utf8')
outfile=open(outfilename, 'w', encoding='utf8')
i=1

for line in infile:
    print(i)
    title_text = line
    title_text_encoded = urllib.parse.quote_plus(title_text)
    #search the title in quotes in scopus
    url = 'https://api.elsevier.com/content/search/scopus?query=TITLE%28%22' + title_text_encoded + '%22%29&apiKey=' + scopus_api_key
    scopusresponse=requests.get(url)
    scopusjson = scopusresponse.json()
    number_results = scopusjson['search-results']['opensearch:totalResults']
    
#if there is exactly one result from the search
    if number_results == "1":
        eid = scopusjson['search-results']['entry'][0]['eid']
        #go get the abstract text
        abstract_url = 'https://api.elsevier.com/content/abstract/eid/' + eid + '?apiKey=' + scopus_api_key + '&view=meta_abs'
        abstractresponse = requests.get(abstract_url)       
        #take abstract_response xml and parse out the abstract
        namespaces = {'ce':'http://www.elsevier.com/xml/ani/common',
                      'dc':'http://purl.org/dc/elements/1.1/',
                      'prism':'http://prismstandard.org/namespaces/basic/2.0/',
                      'abstract':'http://www.elsevier.com/xml/svapi/abstract/dtd',
                      }
        root = ET.fromstring(abstractresponse.text)
        coredata = root.find('abstract:coredata', namespaces)
        title = coredata.find('dc:title', namespaces)
        print('TITLE:', title.text, ' | ')
        description = coredata.find('dc:description', namespaces)
        if description:
            abstract= description.find('abstract:abstract', namespaces)
            para= abstract.findall('ce:para', namespaces)
            the_damn_abstract = ""
            for paras in para:
                the_damn_abstract=the_damn_abstract + paras.text
        else:
            the_damn_abstract = "ABSTRACT NOT FOUND" 
        print('ABSTRACT:', the_damn_abstract) 
        outline = str(i)+ ' | ' + title.text + ' | ' + the_damn_abstract + '\n'
        outfile.write(outline)           
        
    else: #there are 0 or > 1 results in the search for the title
        outline = str(i) + ' | ' + line.rstrip() + ' | ABSTRACT NOT FOUND \n'
        outfile.write(outline)
    i+=1
outfile.close()
