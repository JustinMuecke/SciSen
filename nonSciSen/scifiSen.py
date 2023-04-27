import language_tool_python


statisticsPath : str = "Statistics.txt"
tool = language_tool_python.LanguageTool('en-US')

lengthShortFault : int = 0
lengthLongFault : int = 0
nonAsciiFault : int = 0


def checkValidity(sentence : str) -> tuple[bool, bool, bool, bool]:
    short : bool = False
    long : bool = False
    ascii : bool = False
    if(sentence.count(" ") < 4): short = True
    if(sentence.count(" ") > 100): long = True
    if(not sentence.isascii()): ascii = True
    return (not (short or long or ascii), short, long, ascii)


with open("/home/justinmucke/git/22_scisen/nonSciSen/Data/internet_archive_scifi_v3.txt", "r") as source: 
    parts = source.readlines()
    corpus = parts[-1]
    sentences = corpus.split(". ")


iter        : int = 0
numOfSent   : int = 0
usable      : int = 0
total       : int = len(sentences)
lengthShortFault : int = 0
lengthLongFault : int = 0
nonAsciiFault : int = 0

for sentence in sentences:
    sentence = sentence.lstrip() + ". "
    applicableResult : tuple[bool, bool, bool, bool] = checkValidity(sentence)
    if(applicableResult[0]):
        usable = usable + 1
        with open("Results/ScifiSen"+ str(iter) + ".txt", "a") as target:
            target.write(sentence + "\n")
            numOfSent = numOfSent + 1
        if(numOfSent > 100000): 
            iter = iter + 1
            numOfSent = 0
        print("Iter = " + str(iter) +" / sentence = " + str(numOfSent))
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