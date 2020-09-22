#first programming project as a IT student

def main():
    name=input("Enter name of file containing World Happiness computation data: ")
    import os
    if not os.path.isfile(name) :
        print("Note:File is not found, please try again")
        return main()
    metric=input("Choose metric to be tested from min, mean, median or harmonic_mean: ")
    if metric not in ("min", "mean", "median", "harmonic_mean"):
        print("Note:only accept one of these strings: min, mean, median or harmonic_mean, please try again")
        return main()
    perform=input("""Chose action to be performed on the data using the specified metric, Options are
                     list and correlation """)
    if perform not in ("list","correlation"):
        print("Note:only accept 'list' or 'correlation', please try again")
        return main()
    readfile=open(name, "r")
    fline=list()
    for line in readfile:       
        fline.append(line.split(",")) 
    readfile.close()
    normalise(fline)
         

    

    
def normalise(fline):
    for i in fline:
        for n in range(len(i)):
            try:
                i[n]= float(i[n])
            except ValueError:
                n+=1
    #1.normalise GDP
    for x in range(2,8):
         GDP=""
         for i in fline:
             GDP+=i[x]+","
             liGDP=list(GDP.split(","))      #get the GDP column in string and transfer it to a list
             fixGDP=[]
             for n in range(1, len(liGDP)):
                 try:
                     fixGDP.append(float(liGDP[n]))
                 except:
                     n+=1
             min_GDP=(min(fixGDP))
             max_GDP=(max(fixGDP))
         for i in fline:
            try:
                i[x]= (i[x]-min_GDP)/(max_GDP-min_GDP)
            except TypeError:
                i[x]=i[x]

# Find the minimum list, New column added: i[8] represents minimum of country
    for i in range(len(fline)):
        i+=1
        if i<len(fline):
            listcoun=[]
            for n in range(len(fline[i])):
                n+=2
                if n<len(fline[i]) and type(fline[i][n])==float:
                    listcoun.append(fline[i][n])
            mincoun=min(listcoun)    
            fline[i].append(mincoun)
      
#Get the mean of each country as i[9] 
    for i in range(len(fline)): 
        counlist=list()
        i+=1
        sumcoun=0
        if i<len(fline):
            for n in fline[i][2:8]:
                if type(n)==float:
                    counlist.append(n)           
            for m in counlist:
                sumcoun+=m
            mean=sumcoun/len(counlist)
            mean=float(mean)
            fline[i].append(mean)
                        
#Using same counlist get the median of each country as i[10]            
            counlist.sort()
            half=len(counlist)//2
            median=(counlist[half] + counlist[~half])/2
            fline[i].append(median)
         

#Get harmonic mean i[11]
    for i in range(len(fline)): 
        counlist=list()
        i+=1
        sumcoun=0
        if i<len(fline):
            for n in fline[i][2:8]:
                if type(n)==float and n !=0:
                    counlist.append(1/n)                                        
            for m in counlist:
                sumcoun+=m
            hmean=len(counlist)/sumcoun
            hmean=float(hmean)
            fline[i].append(hmean)        

#Get the rank for lifeladder
    lifeladder=[]
    for i in range(len(fline)):
        i+=1
        if i<len(fline):
           lifeladder.append(fline[i][1])
    liferank=[sorted(lifeladder).index(x) for x in lifeladder]
    liferank=[i+1 for i in liferank]

            
#above is processed data after normalized and found min, mean, medi,hmean with attached column
#below is to calculate the result as required
    if (metric,perform)==("min","list"):
        metric_list(fline,8)
    elif (metric,perform)==("min","correlation"):
        mincorre(fline,8,liferank,"min")
    elif (metric,perform)==("mean","list"):
        metric_list(fline,9)
    elif (metric,perform)==("mean","correlation"):
        mincorre(fline,9,liferank,"mean")
    elif (metric,perform)==("median","list"):
        metric_list(fline,10)
    elif (metric,perform)==("median","correlation"):
        mincorre(fline,10,liferank,"median")
    elif (metric,perform)==("harmonic_mean","list"):
        metric_list(fline,11)
    elif (metric,perform)==("harmonic_mean","correlation"):
        mincorre(fline,11,liferank,"harmonic_mean")
#Using min metric for spearsman correlation
def mincorre(fline,n,liferank,a):
    minlist=[]
    for i in range(len(fline)):
        i+=1
        if i<len(fline):
            minlist.append(fline[i][n])
    minrank=[sorted(minlist).index(x) for x in minlist]
    minrank=[i+1 for i in minrank]   
    lmindiff=[]
    lmindiff=[liferank[i]-minrank[i]  for i in range(len(liferank))]
    lmindiffsqrt=sum(i*i for i in lmindiff)
    min_spearsc=1-(6*lmindiffsqrt)/((len(minrank))*(len(minrank)**2-1))
    print("The correlation coefficient between the study ranking and the ranking using", a," metric is \n",
            round(min_spearsc,4))
       
#Display country, score pairs using min value
def metric_list(fline,n):
    counminlist=[]
    for i in range(len(fline)):
        i+=1
        a=list()     # a=[country, min]
        if i<len(fline):
            a.append(fline[i][0])
            a.append(fline[i][n])
        counminlist.append(a)       
    counminlist.remove([])
    print("Ranked list of countries' happiness scores based the min metric: \n")              
    for i in sorted(counminlist, key = lambda x: x[1],reverse=True):
        print(i[0],(round(i[1],4))) 



         
