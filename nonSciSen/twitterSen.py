import csv
import random
import language_tool_python

tool = language_tool_python.LanguageTool('en-US')
fileID  : str = "1"
topic   : str = "ukraine"
path2data : str = "Data/0410_UkraineCombinedTweetsDeduped.csv"
#path2data   : str = "/Data/040" + str(fileID) + "_UkraineCombinedTweetsDeduped.csv"
path2result : str = "Results/"+ topic + "Tweets.txt"
path2names  : str = "Data/facebook-lastnames-withcount.txt"

def prepareNames(names : list) -> list:
    prepNames : list = []
    for row in names:
        prepNames.append(row[8:].rstrip("\n"))
    return prepNames 
        

def applicable(sentence : str) -> tuple[bool, bool, bool, bool]:
    short : bool = False
    long : bool = False
    ascii : bool = False
    if(sentence.count(" ") < 4): short = True
    if(sentence.count(" ") > 100): long = True
    if(not sentence.isascii()): ascii = True
    if("http" in sentence): ascii = True
    return (not (short or long or ascii), short, long, ascii)


def processSentence(sentence : str) -> str: 
    newSen = ""
    sentence = sentence.replace("\n", "").replace("\r", "")
    words = sentence.split(" ")
    for word in words:
        word = word.lstrip().rstrip("\n").rstrip("\r")
        if len(word) > 0:
            if word[0] == "@": 
                word = random.choice(names)
            if "#" in word:
                word = ""
        newSen = newSen + " " + word
    newSen = newSen + ".\n"
    return newSen


def main() -> tuple[int, int, int]:
    sentences : list = []
    with open(path2data, "r") as csvFile:
        csv_reader = csv.reader(csvFile, delimiter=',')
        sentences = [row[12] for row in csv_reader if row[14] == "en"]

    usable = 0
    total = len(sentences)
    with open(path2result, "a") as target:
        lengthShortFault : int = 0
        lengthLongFault : int = 0
        nonAsciiFault : int = 0
        for sentence in sentences:
            sentence = processSentence(sentence)
            applicableResult : tuple[bool, bool, bool, bool] = applicable(sentence)
            if(applicableResult[0]):
                usable = usable + 1
                target.write(sentence)

            else:
                if(applicableResult[1]): lengthShortFault = lengthShortFault+1
                if(applicableResult[2]): lengthLongFault = lengthLongFault+1
                if(applicableResult[3]): nonAsciiFault = nonAsciiFault+1
    return(lengthShortFault, lengthLongFault, nonAsciiFault, usable, total)


with open (path2names, "r") as source: 
    names = source.readlines()

names = prepareNames(names)

statisticsPath : str = "Statistics.txt"
fault       : tuple[int, int, int, int, int] = main()
usable = fault[3]
total = fault[4]

with open(statisticsPath, "a") as target: 
    target.write("Usable Sentences: " + str(usable) + "\n")
    target.write("Total Sentences: " + str(total) + "\n")
    target.write("Sentences too short " + str(fault[0]) + "\n")
    target.write("Sentences too long " + str(fault[1]) + "\n")
    target.write("Sentences containing non Ascii " + str(fault[2]) + "\n")
    target.write("---------------------------\n\n")
