import PyPDF2
from tkinter.filedialog import askopenfilename
from Model import Model

modelObj=Model("model")

def readPage(n, obj):
    return clearText(obj.pages[n].extract_text())

def clearText(text):
    return text.replace("\n", " ").replace("\r", "").replace("“", "").replace("”", "").replace("‘", "").replace("’", "").replace("—", "").replace("–", "").replace("«", "").replace("»", "").replace("…", "").replace("•", "").replace("·", "").replace("©", "").replace("®", "").replace("§", "").replace(";", "").replace(":", "").replace("(", "").replace(")", "").replace('"', "").lower().strip()

def learnPageWords(page):
    words=page.split(" ")
    words=list(filter(lambda x: x.strip()!="", words))
    wordI=0
    for word in words:
        # Not getting the last word of the page
        if wordI==len(words)-1: break

        nextWord=words[wordI+1]
        if word not in dict.keys(modelObj.model["data"]):
            modelObj.model["data"][word]=[{"nextWord": nextWord, "freq": 1}]
            if wordI >= 1: modelObj.model["data"][word][0]["context"]=[words[wordI-1]]
            modelObj.model["vocab"]+=1
        else:
            found=False
            for i in range(len(modelObj.model["data"][word])):
                if modelObj.model["data"][word][i]["nextWord"]==nextWord:
                    if wordI >= 1 and "context" in dict.keys(modelObj.model["data"][word][i]) and words[wordI-1] in modelObj.model["data"][word][i]["context"]: modelObj.model["data"][word][i]["freq"]+=1
                    elif wordI >= 1 and "context" in dict.keys(modelObj.model["data"][word][i]): modelObj.model["data"][word][i]["context"].append(words[wordI-1])
                    modelObj.model["data"][word][i]["freq"]+=1
                    found=True
                    break
            if not found:
                modelObj.model["data"][word].append({"nextWord": nextWord, "freq": 1})
                if wordI >= 1: modelObj.model["data"][word][-1]["context"]=[words[wordI-1]]
        wordI+=1


try:
    FileLocation = askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt")])
    FileObj = open(FileLocation, 'rb')
except:
    print("No file selected!")
    exit()

#PDF
if FileLocation.endswith(".pdf"):
    pdfReader = PyPDF2.PdfReader(FileObj)
    numPages = len(pdfReader.pages)

    print("\nTotal number of pages: " + str(numPages))

    while True:
        startPage=input("\nEnter starting page number: ")
        endPage=input("Enter ending page number: ")
        if startPage=="": startPage=1
        if endPage=="": endPage=numPages
        startPage=int(startPage)
        endPage=int(endPage)
        if startPage<=0 or startPage>numPages or endPage<startPage or endPage>numPages:
            print("Invalid page number!")
        else:
            startPage-=1
            if endPage != numPages: endPage+=1
            break
#TXT
elif FileLocation.endswith(".txt"):
    print("\nReading text file...")
else:
    print("Invalid file type!")
    exit()


## Start the learn process

print("\nLearn process started!\n")

if FileLocation.endswith(".pdf"):
    for i in range(startPage, endPage):
        p=str(100/(endPage-startPage)*(i+1-startPage))
        p=p[:p.find(".")+3]+"%"
        print("Learning progress: "+p, end="\r")
        learnPageWords(readPage(i, pdfReader))
else:
    learnPageWords(clearText(FileObj.read().decode("utf-8")))

print("\nModel trained!\n\n Total model vocabulary: "+str(modelObj.model["vocab"]))

modelObj.save()