# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pqnhs8CHTeXus1zSw5mKkVSVH-i5niRy

import pip

pip.main(['install', 'pymed'])
pip.main(['install', 'bs4'])
"""

from pymed import PubMed
from bs4 import BeautifulSoup

import xml.etree.ElementTree as ET
import json
import os

def read_xml(path, file_name):
    tree = ET.parse(path)
    all = tree.findall("./")
    book = tree.findall("PubmedBookArticle")
    art = tree.findall("PubmedArticle")
    
    print("the numbers of article: ", len(art), "\n")
    print("the numbers of book: ", len(book), "\n")
    print("the numbers of all iterms: ", len(all), "\n")

    article_details = []
    
    count = 0
    
    for paper in art:
        pmid = "None"
        articleTitle = "None"
        articleAbstract = ""
        articleAbstract_NoNone = ""
        temp = paper.find("MedlineCitation")
        pmid = temp.find("PMID").text
        RetractionOf = 0
        articles_dict = {}
        
        if temp.find("Article").find("ArticleTitle") != None:
            articleTitle = temp.find("Article").find("ArticleTitle").text
        
        if temp.find("Article").find("Abstract") != None:
            for i in temp.find("Article").find("Abstract").findall("AbstractText"):
                if i.findall("./")!=[]:
                    for j in i.findall("./"):
                        if j.text !=None:
                            articleAbstract+=" "+j.text
                        if j.tail!=None:
                            articleAbstract+=j.tail
                elif i.text!=None:
                    articleAbstract += " " + i.text
            articleAbstract = str.strip(articleAbstract)
            
        else:
            continue
        
        if RetractionOf == 1:
            continue
        else:
            count += 1

        articles_dict["pmid"] = pmid
        articles_dict["articleTitle"] = articleTitle
        articles_dict["articleAbstract"] = articleAbstract
    
        article_details.append(articles_dict)
        
    with open('/project/msi290_s22cs685/DPR_Shashank_Ankan_Elli/Pubmed_Articles/JSON/' + file_name +'.json', 'w') as outfile:
        json.dump(article_details, outfile)    
        

directory = '/project/msi290_s22cs685/DPR_Shashank_Ankan_Elli/Pubmed_Articles/test/'
arr = os.listdir(directory)
print(arr)
print(len(arr))

for i in arr:
    path = directory + i
    file_name = i.rsplit('.', 1)[0]
    read_xml(path, file_name)
