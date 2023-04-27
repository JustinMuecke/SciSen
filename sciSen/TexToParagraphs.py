# -*- coding: utf-8 -*-
"""
* extract paragraphs from LateX files, as best as possible:
   * remove environments within sections
   * replace references with "<reference>" tag, grammatically relevant citations with random names
       * random names taken from Kaggle dataset https://www.kaggle.com/datasets/jojo1000/facebook-last-names-with-count
   * replace in-text $math$ with "<equation>" tag
   * remove TeX commands

discarded:
   * for SciSen Section dataset: paragraphs whose titles do not match the titles given by the synonym dictionary synonyms_extended.json
   * files that could not be opened
  
"""

import os
import regex as re
import json
import random
from tqdm import tqdm


InputPath_tex: dict = {"as":"/media/nvme3n1/proj_scisen/datasets/texfiles-as",
                        "a":"/media/nvme3n1/proj_scisen/datasets/texfiles-a",
                        "b":"/media/nvme3n1/proj_scisen/datasets/texfiles-b",
                        "c":"/media/nvme3n1/proj_scisen/datasets/texfiles-c"}
InputPath_randomnames: str = "data/facebook-lastnames-withcount.txt"
InputPath_citegramprefix: str = "data/citegramprefix.txt" #to detect grammatically relevant citations
InputPath_secsynonyms: str = "data/synonyms_extended.json" #to select paragraphs for section classification
OutputPath_selected_paragraphs: str = "/media/nvme3n1/proj_scisen/datasets/SciSections.jsonl" #for section classification
OutputPath_all_paragraphs: str = "/media/nvme3n1/proj_scisen/datasets/SciSections_all.jsonl"


#%% extract text from a LaTeX paragraph
def get_text_from_section(title, tex): #(section):
    """Gathers text from the section given by the title into one string"""
    """tex: LaTeX file, title: name of relevant section"""
    """ removes: all environments and their contents, commands incl. subparagraph headings"""
    
    query_string = r"\\section{" +re.escape(title)+ r"}(.*?)\\section"
    try:
        text = re.findall(query_string, tex, re.DOTALL)[0]
    except IndexError: #special cases for last section
        try:           
            query_string = r"\\section{" +re.escape(title)+ r"}(.*?)\\clearpage"
            text = re.findall(query_string, tex, re.DOTALL)[0]
        except IndexError:
            try:           
                query_string = r"\\section{" +re.escape(title)+ r"}(.*?)\\bibliography"
                text = re.findall(query_string, tex, re.DOTALL)[0]
            except IndexError:
                try:           
                    query_string = r"\\section{" +re.escape(title)+ r"}(.*?)\\end\{document\}"
                    text = re.findall(query_string, tex, re.DOTALL)[0]
                except IndexError:
                    raise
    
    # clean text:
    text = re.sub(r'\n', ' ', text) #linebreaks
    text = remove_tex_env(text) #environments & contents
    text = replace_tex_math(text) # replace with <equation> tag
    text = replace_tex_grammatical(text) # replace grammatically relevant citations with random name, /..ref with <reference> tag
    text = remove_tex_cmd(text) #LaTeX commands
    text = remove_tex_style(text) #LaTeX style commands
    text = remove_tex_cmd2(text) #remaining commands
    text = re.sub(r"\~",r" ",text) #spaces
    text = ' '.join(text.split()) # multiple spaces
    text = re.sub(r"--",r"–",text) #n-dash
    text = re.sub(r"``",r'"',text) #quotation marks
    text = re.sub(r"''",r'"',text) #quotation marks
    text = re.sub(r"---",r"—",text) #m-dash
    text = re.sub(r'[\~\\\{\}]', '', text) # tilde, backslash, curly brackets
    text = re.sub(r"\( ", r"(", text) #deletion after bracket
    text = re.sub(r"\[ ", r"[", text) #deletion after bracket
    text = re.sub(r"\( \)",r"()",text) #empty brackets
    text = re.sub(r"\[ \]",r"[]",text) #empty brackets
    text = re.sub(r" \(\)",r"",text) #empty brackets
    text = re.sub(r"\[\]",r"",text) #empty brackets
    text = re.sub("\( ", "(", text)
    text = re.sub("\[ ", "[", text)
    text = re.sub("\(<reference>\)", "<reference>", text) #replacement remnant
    text = re.sub("\[<reference>\]", "<reference>", text) #replacement remnant
    text = re.sub(r"\(and \)", r"", text) #replacement remnant
    text = ' '.join(text.split()) # multiple spaces
    text = re.sub(r' \.', '.', text) # deletion before full stop
    text = re.sub(r' \,', ',', text) # deletion before comma
    text = re.sub(r' \?', '?', text) # deletion before question mark
    return text
    


#%% LaTeX processing functions

def remove_tex_env(tex):
    """removes tex environments \begin{...}...\end{...} or \[...\] from the input string"""
    environments = re.findall(r"\\begin{(.*?)}", tex, re.DOTALL)
    text = tex
    for env in environments:
        text = re.sub(r"\\begin\{"+re.escape(env)+r"\}.*?\\end\{"+re.escape(env)+r"\}", " ", text) 
    text = re.sub(r"\\\[.*?\\\]", " ", text)
    return text


def replace_tex_math(tex):
    """replaces in-text math environments $$...$$ and $...$ with <equation> tag"""
    text = tex 
    #remove between double $$
    text = re.sub(r"\$\$.*?\$\$","<equation>", text)
    #remove between single $$
    if text[0] == "$":
        text = " "+text
        environments = re.findall(r"[^\\]\$.*?\$", text, re.DOTALL)
        text = text[1:]
    else:
        environments = re.findall(r"[^\\]\$.*?[^\\]\$", text, re.DOTALL)
    loop = len(environments) != 0
    while loop:  
        for i, env in enumerate(environments): #loop to avoid replacing dollar signs       
            if env[-2] == "\\":
                envtoend = " $"+re.findall(re.escape(env)+r"(.*?)$", text, re.DOTALL)[0]
                environments =re.findall(r"[^\\]\$.*?[^\\]\$", envtoend, re.DOTALL)
                environments[0] = env+environments[0][2:]
                break
            text = re.sub(re.escape(env[1:]), "<equation>", text) 
            if i == len(environments)-1: #last element
                loop = False
                break         
    return text

def replace_tex_grammatical(tex):
    """replaces \citet{...}, \citealt{...} and \citeauthor{},
    as well as \cite{...} following preceding words given in InputPath_citegramprefix
    with random names,
    \..ref{} with <reference>"""
    text = tex
    # names
    occurences = re.findall(r"\\citet\{.*?\}", text) + re.findall(r"\\citeauthor\{.*?\}", text) + re.findall(r"\\citealt\{.*?\}", text)
    for o in occurences:
        text = re.sub(re.escape(o), random.choice(randomnames), text)
    for lead in citegramprefix:
        occurences = re.findall(r"[\~ \(]"+lead+r"[ \~]"+r"\\cite\{.*?\}", text)
        occurences += re.findall(r"[\~ \(]"+lead+r"[ \~]"+r"\[\\cite\{.*?\}\]", text)
        for o in occurences:
            orep = re.sub(r"\[\\cite\{.*?\}\]",r"\cite{placeholder}", o)
            orep = re.sub(r"\\cite\{.*?\}", " "+random.choice(randomnames), orep)
            text = re.sub(re.escape(o), orep, text)
    # numbers
    occurences = re.findall(r"\\[^ ]*?ref{.*?\}", text)
    for o in occurences:
        text = re.sub(re.escape(o), "<reference>", text)
    return text
    

def remove_tex_cmd(tex):
    """removes tex commands \cmd{...} from the input string """
    text = ""
    append_next = True
    open_par = 0 #open parentheses
    log = ""    
    for l in tex:
        if log != "": # after \, before {}
            if l == " ":
                text += log+l
                log = ""
            elif l == "{":
                log = ""
                append_next = False
                open_par = 1
            else:
                log += l
        elif append_next: # outside of command
            if l == "\\":
                log += l
            else:
                text += l
        else: # within {}
            if l == "{":
                open_par += 1
            elif l == "}":
                if open_par == 1:
                    open_par = 0
                    append_next = True
                    text += " "
                else:
                    open_par -= 1
    return text

def remove_tex_style(tex):
    """removes tex stylistics in the form of {\cmd text} from the input string, keeping text part. Does not handle nested brackets."""
    text = tex
    occurences = re.findall(r"\{\\[^\}\{]*? [^\}\{]*?\}", text) 
    for o in occurences:
        text = re.sub(re.escape(o), re.findall(r"\{\\.*? (.*?)\}", o)[0], text)
    return text 

def remove_tex_cmd2(tex):
    """removes remaining commands \\cmd . Run after remove_tex_style."""
    return re.sub(r"\\.*? "," ",tex)
    
#%% lists & dictionaries

def get_names_list():
    #facebook last names from https://www.kaggle.com/datasets/jojo1000/facebook-last-names-with-count?resource=download
    with open(InputPath_randomnames) as f:
        names = [l.strip()[6:].capitalize() for l in f]
    return names

def get_citegram_list():
    with open(InputPath_citegramprefix) as f:
        leadingwords = [l.strip() for l in f]
    return leadingwords

def get_permissible_titles():
    # combined from CiteWorth https://github.com/copenlu/cite-worth/blob/main/dataset_creation/data/permissible_section_titles.txt and Danial Podjavorsek's dictionary mapping of section headings to categories
    with open(InputPath_secsynonyms) as f:
        data = json.load(f)
    titles = data.keys()
    return data, titles

#%% main

randomnames = get_names_list()
citegramprefix = get_citegram_list()
synonyms, permissible_titles = get_permissible_titles()

debug_list = {'as':[],'a':[],'b':[],'c':[]}

selective_file = open(OutputPath_selected_paragraphs, "w")
all_file = open(OutputPath_all_paragraphs, "w")

counter_processed = 0
for ranking in InputPath_tex:  
    print("extracting papers ranked "+ranking+":")
    counter_notOpened = 0
    counter_noSections = 0
    counters_relTitles = []
    counter_all = 0
    counter_selected = 0
    for filename in tqdm(os.listdir(InputPath_tex[ranking])):
        section_data = {}
        counter_processed += 1
        try:
            file_tex = open(InputPath_tex[ranking]+"/"+filename, 'r').read()
        except:
            #print(filename+": Could not be opened.")
            counter_notOpened += 1
            continue
        section_titles = re.findall(r"\\section{(.*?)}", file_tex)
        if len(section_titles) == 0:
            #print(filename+": no sections found.")
            counter_noSections += 1
            continue
        count = 0
        for title in section_titles:
            try:
                section_text = get_text_from_section(title = title, tex = file_tex)
            except:
                #print(filename+": "+title+" could not be extracted")
                debug_list[ranking].append({
                    'paper_id': filename,
                    'section_title': title
                    })
                continue
            counter_all += 1
            all_file.write(f"{json.dumps({'paper_id': filename[:-4], 'section_title': title.lower(), 'rank': ranking, 'processed_text': section_text})}\n")
            if title.lower() in permissible_titles or title.lower().__contains__("appendix"):
                count += 1
                counter_selected += 1
                if(title.lower().__contains__("appendix")):
                    selective_file.write(f"{json.dumps({'paper_id': filename[:-4], 'section_title': title.lower(),'section_category': ['appendix'], 'rank': ranking, 'processed_text': section_text})}\n")
                else:
                    selective_file.write(f"{json.dumps({'paper_id': filename[:-4], 'section_title': title.lower(),'section_category': synonyms[title.lower()], 'rank': ranking, 'processed_text': section_text})}\n")
        counters_relTitles.append(count/len(section_titles))
        #print(f"Stored {count}/{len(section_titles)} sections from file {filename}")
    print(f"extracted {counter_all} paragraphs, {counter_selected} of which have permissible titles")
    print(f"Not readable: {counter_notOpened} files")
    print(f"No sections found: {counter_noSections} files")
    print(f"Other extraction issues: {len(debug_list[ranking])} paragraphs")
selective_file.close()
all_file.close()