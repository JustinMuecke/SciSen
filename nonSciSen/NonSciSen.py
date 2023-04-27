import json

dataPath : str = "Data/data_Small.json"
abbrPath : str = "abbreviation.txt"
outputPath : str = "Results/RedditSen.txt"
statisticsPath : str = "Statistics.txt"



def applicable(sentence : str) -> tuple[bool, bool, bool, bool]:
    short : bool = False
    long : bool = False
    ascii : bool = False
    if(sentence.count(" ") < 4): short = True
    if(sentence.count(" ") > 100): long = True
    if(not sentence.isascii()): ascii = True
    if("http" in sentence): ascii = True
    if(sentence == "[Deleted]"): ascii = True
    if(sentence == "[Removed]"): ascii = True
    if(sentence == "\\n"): ascii = True
    if(sentence == ""): ascii = True
    return (not (short or long or ascii), short, long, ascii)


def splitAtDot(inputString : str) -> list[str]:
    sentences = list()
    
    tempSentences : list[str]= inputString.split(". ")

## ALSO SPLIT AT: :, ?, !, ;, \n

    sentence : str= ""
    abbreviated : bool = False
    for tmpSentence in tempSentences:
        tmpSentence = tmpSentence+". "
        for abb in abbreviations: 
            if tmpSentence.__contains__(abb):
                sentence += tmpSentence
                abbreviated = True
                break
       
        if(not abbreviated):
            sentence += tmpSentence
            sentences.append(sentence)
            sentence = ""  
        abbreviated = False

    return sentences


postList = list()
with open(dataPath) as f:
    for post in f:
        postDict = json.loads(post)
        postList.append(postDict)


abbreviations = list()
with open(abbrPath , "r") as source:
    for line in source:
        abbre = line.rstrip("\n")
        abbreviations.append(line.rstrip("\n"))


usable : int = 0
total : int = 0
lengthShortFault : int = 0
lengthLongFault : int = 0
nonAsciiFault : int = 0

for post in postList:
    text = post["body"]
    text = text.replace('\n', ' ').replace('\r', '')
    text = text.replace("&gt;", "")
    sentences = splitAtDot(text)
    for sentence in sentences:
        total = total + 1
        applicableResult : tuple[bool, bool, bool, bool] = applicable(sentence)
        if(applicableResult[0]):
            usable = usable + 1
            with open(outputPath, "a") as target: 
                target.write(sentence.lstrip().rstrip() + "\n")
        else: 
            if(applicableResult[1]): lengthShortFault = lengthShortFault+1
            if(applicableResult[2]): lengthLongFault = lengthLongFault+1
            if(applicableResult[3]): nonAsciiFault = nonAsciiFault+1

with open(statisticsPath, "a") as target: 
    target.write("Usable Sentences: " + str(usable) + "\n")
    target.write("Total Sentences: " + str(total) + "\n")
    target.write("Sentences too short " + str(lengthShortFault) + "\n")
    target.write("Sentences too long " + str(lengthLongFault) + "\n")
    target.write("Sentences containing non Ascii " + str(nonAsciiFault) + "\n")
    target.write("---------------------------\n\n")



            
                
