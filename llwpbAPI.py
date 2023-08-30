import Model
import random

class API:
    def __init__(self, modelName="model"):
        self.modelObj=Model.Model(modelName)
    
    def getWord(self, text):
        contextKey=80

        text=text.strip()
        if text == "": return random.choice(list(dict.keys(self.modelObj.model["data"])))

        currentWord=text.split(" ")[-1]
        nextWords=self.modelObj.model["data"][currentWord.lower()]
        nextWords=sorted(nextWords, key=lambda k: k["freq"], reverse=True)
        text=text[0].upper()+text[1:]
        if len(text.split(" ")) >= 2: 
            bestContexts=self.getBestContext(text.split(" ")[-2], nextWords)
            try:
                # Choose the next word with score higher than contextKey
                nextWord=random.choice(list(filter(lambda x: x["score"]>=contextKey, bestContexts)))["nextWord"]
            except:
                nextWord=bestContexts[0]["nextWord"]
        
        else: nextWord=random.choice(nextWords)["nextWord"]
        if text[-1] in [".", "!", "?"]: nextWord=nextWord.capitalize()
        return text+" "+nextWord

    def getSimilarity(self, word1, word2):
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

    def getContextScore(self, contextWord, context):
        hs=0
        for i in context:
            p=self.getSimilarity(i, contextWord)
            if p > hs: hs=p
        return hs

    def getBestContext(self, context, nextWords):
        l=[]
        for i in nextWords:
            if "context" in dict.keys(i): l.append({"nextWord": i["nextWord"], "score": self.getContextScore(context, i["context"])})
        return sorted(l, key=lambda k: k["score"], reverse=True)

    def searchWord(self, tWord):
        key=60
        l=filter(lambda x: self.getSimilarity(x, tWord)>=key, dict.keys(self.modelObj.model["data"]))
        l=[{"word": w, "sim": self.getSimilarity(w, tWord)} for w in l]
        return sorted(l, key=lambda k: k["sim"], reverse=True)

    def generate(self, prompt, size):
        if prompt.strip() != "":
            prompt=prompt.split(" ")
            prompt[-1]=self.searchWord(prompt[-1])[0]["word"]
            prompt=" ".join(prompt)
        for i in range(size):
            prompt=self.getWord(prompt)
        return prompt
