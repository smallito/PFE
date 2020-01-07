import io
import numpy as np
import re
import spacy
import unidecode
from utils import find 

nlp = spacy.load('fr_core_news_sm')

def tax2vec(vecIn):
    mini = 100000
    bestWord = ""
    idx = 0
    for i in range(taxo.shape[1]):
        vecTax = taxo[:,i]
        dist = spatial.distance.cosine(vecIn, vecTax ) 
        if dist > 0 and mini > dist:
            mini = dist
            idx = i
    bestWord = re.findall(r'".+?"', fp[idx])[0].replace('"',"")
    return bestWord, mini 

#Helper function to get the un-normalized taxonomy
def getNormalWord(lineNum):
    fp = open("utils/taxonomieUTF.txt")
    for i, line in enumerate(fp):
        if i == lineNum:
            return line 
           

def findWordInTax(title):
    taxoOutput = []
    lineOutput = []
    title = nlp(title)
    titleTreated = ""
    for word in title:
        titleTreated += word.lemma_+" "
    titleTreated = titleTreated[:-1]
    with open("utils/taxonomieLemma.txt") as taxo:
        i = 0
        for line in taxo:
            i += 1
            line = re.findall(r'".+?"', line)[0].replace('"',"")
            line = line.strip('"').strip(',')
            line = " " + line + " "
            if line in titleTreated:
                outputLine = getNormalWord(i)
                outputLine = re.findall(r'".+?"', outputLine)[0].replace('"',"")
                outputLine = outputLine.strip('"').strip(',')
                outputLine = " " + outputLine + " "
                outputLine = find.strip_accent(outputLine) #remplace accents and special chars by their ascii counterparts 
                taxoOutput.append(str(outputLine))

    return taxoOutput


def get_taxo(text):
    out = list()
    outList = list()
    #Remove all problematic characters
    text = find.clean_doc(text)
    #Find the arretes 
    arrete = find.find_arretes(text)
    #Get their titles
    title = find.find_titles(text)
    #remove Duplicates
    title = find.remove_same(title)

    for t in title:
        out += findWordInTax(t)

    dictDuplicates = {i:out.count(i) for i in out}
    dictDuplicates = sorted(dictDuplicates.items(), key=lambda x: x[1], reverse=True)
    for elem in dictDuplicates:
        outList.append(elem[0])
    return outList
        
