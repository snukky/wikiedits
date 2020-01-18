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
            yield sentences[len(sentences)-1]
    
            
        
        
