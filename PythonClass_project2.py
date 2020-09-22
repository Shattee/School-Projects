#a program that reads in two text files
#containing the works to be analysed and builds a profile for each. The two profiles
#are compared and returned besides a score which reflects the distance between
#the two works in terms of their style; low scores, down to 0.

def main(textfile1,textfile2,feature):   
    textfile1,textfile2,feature,test_result=test(textfile1,textfile2,feature) #call test function to check 
    if not test_result:
        return (None, None, None)
    text1 = open(textfile1,'r').read()
    text2 = open(textfile2,'r').read()
    text1 = text1.lower()
    text2 = text2.lower()
    if feature=='conjunctions': 
        p1=conjunctions(text1)
        p2=conjunctions(text2)
        dist=distance(p1,p2)
        return (dist,p1,p2)
    elif feature=='unigrams':
        p1=unigrams(text1)
        p2=unigrams(text2)
        dist=distance(p1,p2)
        return (dist,p1,p2)
    elif feature=='punctuation':
        p1=punctuation(text1)
        p2=punctuation(text2)
        dist=distance(p1,p2)
        return (dist,p1,p2)
    elif feature=='composite':
        p1=composite(text1)
        p2=composite(text2)
        dist=distance(p1,p2)
        return (dist,p1,p2)

def test(textfile1,textfile2,feature):
    import os  
    filelist=[textfile1,textfile2]
    for i in filelist:
        if type(i) != str: 
            return (None,None,None,False)
        elif not os.path.isfile(i) :
            return (None,None,None,False)
    feature_list=["conjunctions", "unigrams", "punctuation","composite"]
    if not feature in feature_list:
        return (None,None,None,False)
    return(textfile1,textfile2,feature,True)

def distance(p1,p2):
    distancelist=[]
    samewords=[]
    p1keys=list(p1.keys())
    p2keys=list(p2.keys())
    for i in p1keys:
        if i in p2keys:
            distancelist.append(float(p1[i])-float(p2[i])) #have same words, get the difference and save them to same words list
            samewords.append(i)
        else:
            distancelist.append(p1[i]) #unique words             
    for c in p2keys:
        if c not in samewords: # pick out the unique words of text2
            distancelist.append(p2[c])            
    dvalue=0 #difference value
    import math
    for n in distancelist:
        dvalue+=n*n
    
    return (round(math.sqrt(dvalue),4))
    
def conjunctions(text):    
    chlist=list(range(128))
    del chlist[97:123]
    for c in chlist:
        text = text.replace(chr(c), " ")       
    textwords = text.split()   
    conjunction=["also", "although", "and", "as", "because", "before", "but", "for", "if", "nor", "of",
                "or", "since", "that", "though", "until", "when", "whenever", "whereas",
                "which", "while", "yet"]
    conjunction_dist={}
    
    for c in conjunction:
        conjunction_dist[c]=conjunction_dist.get(c,0)  #uniform dict format       
    for w in textwords:                      #start to count
        if w in conjunction_dist:
            conjunction_dist[w] = conjunction_dist.get(w,0) + 1    
    return conjunction_dist
          
def unigrams(text):    
    chlist=list(range(128))
    del chlist[97:123]
    chlist.remove(39)
    chlist.remove(45)
    text=text.replace("--"," ") # "--" between words is considered as space
   
    for c in chlist:
        text = text.replace(chr(c), " ")          
    textwords = text.split( )    
    for i in range(len(textwords)):  # delete extra "'" infront or at the end
        if textwords[i][0] == "'" or textwords[i][-1] == "'":
            textwords[i]=textwords[i].strip("'")
        elif textwords[i][0] == "-" or textwords[i][-1]=="-":
            textwords[i]=textwords[i].strip("-") 
    
    textwords=[x for x in textwords if x != ''] # delete '' which appeared after strip function    
    count_words={} 
    for w in textwords: 
        count_words[w]=count_words.get(w,0)+1
    count_words=dict(sorted(count_words.items()))
    return count_words

def punctuation(text):
    count_punctuation={',': 0, ';': 0, '-': 0, "'": 0}  
    for i in text:
        if i==';' or i==',':
            count_punctuation[i]=count_punctuation.get(i,0)+1   
    textlist=list(text)
    chlist=[]  # list of a-z
    for i in range(97,123):
        chlist.append(chr(i))
    
    for i in range(len(textlist)):
        if textlist[i]=="'" or textlist[i]=='-':
            if textlist[i-1] in chlist and textlist[i+1] in chlist: #choose "'" or "-" between letters to count
                count_punctuation[textlist[i]]=count_punctuation.get(textlist[i],0)+1 
    return count_punctuation            
      
            
def composite(text):
    #count paragraphs
    paratext=text.strip() #delete blank before or after text
    paratext=paratext.split('\n\n')
    paratext=[x for x in paratext if x!=''] #delete empty paragraph
    print(len(paratext))
    
    #count how many sentences for each text
    sentext=text 
    endsign=['. ', '! ', '? ','."', '!"', '?"', ".'","!'", "?'", '.\n', '!\n', '?\n','."\n', '!"\n', '?"\n', ".'\n","!'\n", "?'\n"]#situations of sentences' ending 
    for ch in endsign:
        sentext=sentext.replace(ch, '^')    
    sentext = sentext.split('^')     
    sentext = [x for x in sentext if x != '' and x !='\n' ] #eliminate the situation that count empty string as a sentence
        
    #count how many words for each text in total
    words=unigrams(text)
    list_numwords=list(words.values())
    numwords=0
    for n in list_numwords:
        numwords+=n
    conjunction= conjunctions(text)   #call conjunction function to get its dictionary   
    count_punctuation = punctuation(text) #call punctuation function to get its dictionary
    
    #dicts for 'words_per_sentence'and'sentences_per_par'
    per={'words_per_sentence':str(round(numwords/len(sentext),4)), 'sentences_per_par':str(round(len(sentext)/len(paratext),4))}
            
    #merge dict
    composite_dist={} 
    for d in [conjunction,count_punctuation, per]: #combine three dictionaries together
        composite_dist.update(d)   
    return composite_dist
