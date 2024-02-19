from unidecode import unidecode
include = []
def trimline(line):
    newLine = ''
    count = 1
    for i in line:
        if i.isalpha() or i in include:
            newLine += i
    if "Chapter " in line:
        newLine += str(count)
        count += 1

    return newLine + "\n"

def parse(textToParse):
    open('processed.txt', 'w').close()
    infile = open(textToParse, "r")
    outfile = open("processed.txt", "a")
    while True:
        line = infile.readline()
        if not line:
            break
        # if "Chapter 2" in line:
        #     break
        outfile.write(trimline(unidecode(line)))
    outfile.close()
    infile.close()



def parseSourceText(textToParse):
    parse(textToParse)
    f = open("processed.txt", "r")
    content = f.read()
    print(len(content))

    
