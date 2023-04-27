"""
Adapted from the non-scientific sentence extraction.
Extract sentences from the text previously extracted from the LaTeX files.
Sentences must be at least 4 spaces/words, at most 100 words, start with a capital letter, end with a punctuation mark (.!?), and not contain non-ascii signs.

Run with
SaveAsParagraphs = False to save all sentences, and with
SaveAsParagraphs = True to save only sentences relevant for the section classification task
"""

import json
from tqdm import tqdm
import regex as re
import pandas as pd

SaveAsParagraphs = False #[False, True]

if SaveAsParagraphs:
    dataPath : str = "/media/nvme3n1/proj_scisen/datasets/SciSections.jsonl"
    outputPathJson : str = "/media/nvme3n1/proj_scisen/datasets/SciSections_sentences.jsonl"
    outputPathTxt : str = "/media/nvme3n1/proj_scisen/datasets/SciSen_MLSConly.txt"
    statisticsPath : str = "/media/nvme3n1/proj_scisen/git_repos/Luise/22_scisen/sciSen/data/Statistics_MLSConly.txt"
else:
    dataPath : str = "/media/nvme3n1/proj_scisen/datasets/SciSections_all.jsonl"
    outputPathTxt : str = "/media/nvme3n1/proj_scisen/datasets/SciSen.txt"
    statisticsPath : str = "/media/nvme3n1/proj_scisen/git_repos/Luise/22_scisen/sciSen/data/Statistics_all.txt"
abbrPath : str = "data/abbreviation_extended.txt"

STATISTICS = []
def applicable(sentence : str) -> bool:
    stats = []
    applicable = True
    if (re.search("[A-Z]", sentence[0]) is None): # starts with a capital letter
        applicable = False 
        stats.append('capital')
    if not (sentence.rstrip()[-1] in '.?!'):# ends with a punctuation mark
        applicable = False 
        stats.append('punctuation')
    if not (re.search("[\^\_\=]", sentence) is None): # remnants from LaTeX extraction (likely uncaught equations)
        applicable = False 
        stats.append('TeX')
    if(sentence.count(" ") < 4): # at least 4 words long
        applicable = False 
        stats.append('short')
    if(sentence.count(" ") > 100): # at most 100 words long
        applicable = False 
        stats.append('long')
    if not (sentence.isascii()): # ascii
        applicable = False 
        stats.append('ascii')
    STATISTICS.append(stats)
    return applicable

def splitAtPunctuation(inputString : str) -> list[str]: #split at .,?,!
    sentences = list()
    
    tempSentences0 : list[str]= re.split("([\.\?\!] )", inputString)
    tempSentences : list[str]= []
    for i in range(1, len(tempSentences0), 2):
        tempSentences.append(tempSentences0[i-1]+tempSentences0[i])
    if (len(tempSentences)*2 < len(tempSentences0)):
        tempSentences.append(tempSentences0[-1]) # this sentence does not meet the criteria (end of sentence-punctuation), but we keep it for counting

    sentence : str= ""
    abbreviated : bool = False
    abbs_EOS = [" etc.", " et al."]
    abbreviated_EOS : bool = False #possible end-of-sentence abbreviation
    for tmpSentence in tempSentences:
        #tmpSentence = tmpSentence+". "
        if (abbreviated_EOS): 
            if (len(sentence) < 1) or not (re.search("[A-Z]", sentence[0]) is None): # empty sentence or captical letter following possible EOS-abbreviation -> probably a new sentence
                sentences.append(sentence)
                sentence = ""
                abbreviated_EOS = False
        for abb in abbreviations: 
            if tmpSentence.__contains__(abb):
                if tmpSentence[-(len(abb)+1):-1] == abb: #check if it was in fact split by abbreviation [not the case if, e.g. followed by a comma instead of space]
                    sentence += tmpSentence
                    abbreviated = True
                    if abb in abbs_EOS:
                        abbreviated_EOS = True
                    break       
        if(not abbreviated):
            sentence += tmpSentence
            sentences.append(sentence)
            sentence = ""  
        abbreviated = False
    return sentences


paragraphList = list()
with open(dataPath) as f:
    for paragraph in f:
        paragraphDict = json.loads(paragraph)
        paragraphList.append(paragraphDict)


abbreviations = list()
with open(abbrPath , "r") as source:
    for line in source:
        abbre = line.rstrip("\n")
        abbreviations.append(line.rstrip("\n"))

n_total = len(paragraphList)
counter = 0
n_total_sen = 0
usable_sen_total = 0

sentence_file = open(outputPathTxt, "w", encoding = "utf-8")
if SaveAsParagraphs:
    paragraph_file = open(outputPathJson, "w", encoding = "utf-8")

for paragraph in tqdm(paragraphList):
    usable_sen_paragraph = 0
    if SaveAsParagraphs:
        paragraph_sentences = []
    counter += 1
    #print(f"File {paragraph['paper_id']}, paragraph {paragraph['section_title']}")
    #print(f"{counter}/{n_total} paragraphs processed")
    text = paragraph["processed_text"]
    text = text.replace('\n', ' ').replace('\r', '')
    text = text.replace("&gt;", "")
    sentences = splitAtPunctuation(text)
    for sentence in sentences:
        if len(sentence) > 0:
            n_total_sen += 1
            if(applicable(sentence)):
                usable_sen_paragraph += 1
                if SaveAsParagraphs:
                    paragraph_sentences.append(sentence.lstrip().rstrip())
                sentence_file.write(sentence.lstrip().rstrip() + "\n")
            elif SaveAsParagraphs:
                paragraph_sentences.append("[removed]")
    usable_sen_total += usable_sen_paragraph
    if SaveAsParagraphs:
        paragraph_file.write(f"{json.dumps({'n_sentences': usable_sen_paragraph, 'sentences': paragraph_sentences, 'section_category': paragraph['section_category'], 'section_title': paragraph['section_title'], 'rank': paragraph['rank'], 'paper_id': paragraph['paper_id']})}\n")


sentence_file.close()
if SaveAsParagraphs:
    paragraph_file.close()
                    
print(f"Usable Sentences: {usable_sen_total}")
print(f"Total Sentences: {n_total_sen}")
print('Non-applicable Sentences:')
print(pd.Series(STATISTICS).value_counts())

with open(statisticsPath, "a") as target: 
    target.write(f"Usable Sentences: {usable_sen_total}" + "\n")
    target.write(f"Total Sentences: {n_total_sen}" + "\n")
    target.write("Non-applicable Sentences:" + "\n")
    target.write(str(pd.Series(STATISTICS).value_counts()))