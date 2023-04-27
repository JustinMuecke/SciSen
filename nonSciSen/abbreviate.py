abbreviation = list()

with open("Data/abbr_html.txt", "r") as source: 
    for input in source.readlines():
        if(".</td>" in input):
            print(".")
            inputTail = input.replace("</td>", "").replace("<td>", "").rstrip() + "\n"
            abbreviation.append(" " + inputTail)
    

with open("abbreviation.txt", "a") as target: 
    for abb in abbreviation: 
        target.write(abb)