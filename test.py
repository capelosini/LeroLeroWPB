import random
from Model import Model

def getWord(text):
    contextKey=85

    text=text.lower().strip()
    currentWord=text.split(" ")[-1]
    nextWords=modelObj.model["data"][currentWord]
    nextWords=sorted(nextWords, key=lambda k: k["freq"], reverse=True)
    text=text[0].upper()+text[1:]
    if len(text.split(" ")) >= 2: nextWord=random.choice(list(filter(lambda x: x["score"]>=contextKey, getBestContext(text.split(" ")[-2], nextWords))))["nextWord"]
    else: nextWord=nextWords[0]["nextWord"]
    return text+" "+nextWord

def getSimilarity(word1, word2):
    word1=word1.lower().strip()
    word2=word2.lower().strip()
    if word1==word2:
        return 100
    if len(word2) > len(word1): word1, word2 = word2, word1
    i=0
    points=0
    for l in word2:
        if l == word1[i]:
            points+=1
        i+=1
    return round(100/len(word1)*points)

def getContextScore(contextWord, context):
    hs=0
    for i in context:
        p=getSimilarity(i, contextWord)
        if p > hs: hs=p
    return hs

def getBestContext(context, nextWords):
    l=[]
    for i in nextWords:
        if "context" in dict.keys(i): l.append({"nextWord": i["nextWord"], "score": getContextScore(context, i["context"])})
    return sorted(l, key=lambda k: k["score"], reverse=True)

def searchWord(tWord):
    key=60
    l=filter(lambda x: getSimilarity(x, tWord)>=key, dict.keys(modelObj.model["data"]))
    l=[{"word": w, "sim": getSimilarity(w, tWord)} for w in l]
    return sorted(l, key=lambda k: k["sim"], reverse=True)

def generateText(prompt, size):
    prompt=prompt.split(" ")
    prompt[-1]=searchWord(prompt[-1])[0]["word"]
    prompt=" ".join(prompt)
    for i in range(size):
        prompt=getWord(prompt)
    return prompt


modelObj=Model("model")

while True:
    inputText=input("Prompt: ")
    
    print(generateText(inputText, 20))