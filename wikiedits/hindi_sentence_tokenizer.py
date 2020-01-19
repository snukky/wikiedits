class HindiSentenceTokenizer:
    def tokenize(self,text):
        sentence_end=('|','।','!','?')
        text_len=len(text)
        sentences=[]
        pos=[0]*len(sentence_end)
        splitting_point=0
        while len(text)>0:
            for i in range(len(sentence_end)):
                pos[i]=text.find(sentence_end[i])
            if pos.count(-1)==len(pos):
                break
            splitting_point=min([x for x in pos if not x==-1])
            sentences.append(text[:splitting_point+1])
            text=text[splitting_point+1:]
            ans=sentences[len(sentences)-1]
            i=0
            while i<len(ans) and ans[i]==' ':
                i=i+1
            if i<len(ans):
                ans=ans[i:]
                i=len(ans)-1
                while i>0 and ans[i]==' ':
                    i=i-1
                if i>0:
                    ans=ans[:i+1]
                    yield ans
    
            
        
        
