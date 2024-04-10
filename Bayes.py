from os import walk,path
from data import *
import matplotlib.pyplot as plt
import sys
import os.path

class Bayes:
    
    def __init__(self):
        # Synarthsh gia ta dedomena ths klashs
        self.data = Data()
        #dianismata
        self.negdianisma=self.data.get01('train','neg')
        self.posdianisma=self.data.get01('train','pos')
        #arithmos le3ewn sto le3ilogio
        self.words=self.WordsCounter()
        #Ari8mos twn kritikwn sto epipedo ekpaideyshs
        self.negNumbers = self.NegCounter()
        self.posNumbers = self.PosCounter()
        #Synolo olwn twn le3ewn  
        self.SumOfNeg = self.SumNegCounter()
        self.SumOfPos = self.SumPosCounter()
        #ari8mos le3ewn se ka8e kathgoria 
        self.totalNegWords = self.totalSumNeg()
        self.totalPosWords = self.totalSumPos()
        #Bayes P(X|C) me C=1 kai C=0
        self.negPossibilities = self.CounterOfNegPossibility()
        self.posPossibilities = self.CounterOfPosPossibility()
        #Ypologismos pi8anothtas na exoume C=1 kai C=0(P(C=1) kai P(C=0))
        self.positiveP = self.CounterPSimpleP()
        self.negativeP = self.CounterNSimpleP()


#"""---------------------------------------- TRAIN ----------------------------------------------"""

    def WordsCounter(self): #Ypologismos le3ewn sto le3ilogio
        file = open(self.data.link()+"\\"+"dictionary.txt","r")
        counter=0
        for i in file.readlines():
            counter=counter+1
        file.close()
        return counter

    def NegCounter(self): #Ypologismos arnhtikwn kritikwn
        path=self.data.link()+"\\"+"train"
        negPath=path+"\\"+"neg"
        negNumbers=len([file for file in os.listdir(negPath)if os.path.isfile(os.path.join(negPath, file))])
        return negNumbers

    def PosCounter(self): #Ypologismo 8etikwn kritikwn
        path=self.data.link()+"\\"+"train"
        PosPath=path+"\\"+"pos"
        posNumbers= posNum = len([file for file in os.listdir(PosPath)if os.path.isfile(os.path.join(PosPath, file))])
        return posNumbers

    def SumNegCounter(self): #Ypologizei to a8roisma twn arnhtikwn le3ewn se ka8e kritikh
        SumOfNeg=[]
        for i in range(self.words):
            sum1=0
            for j in range(self.negNumbers):
                sum1=self.negdianisma[j][i]+sum1
            SumOfNeg.append(sum1)
        return SumOfNeg

    def SumPosCounter(self): #Ypologizei to a8roisma twn 8etikwn le3ewn se ka8e kritikh
        SumOfPos=[]
        for i in range(self.words):
            sum1=0
            for j in range(self.posNumbers):
                sum1=self.posdianisma[j][i]+sum1
            SumOfPos.append(sum1)
        return SumOfPos

    def totalSumNeg(self):  
        totalNegWords=0
        for i in range(len(self.SumOfNeg)):
            totalNegWords = totalNegWords + self.SumOfNeg[i]
        return totalNegWords

    
    def totalSumPos(self):
        totalPosWords=0
        for i in range(len(self.SumOfPos)):
            totalPosWords = totalPosWords + self.SumOfPos[i]
        return totalPosWords


    def CounterOfNegPossibility(self): #Epistrefei thn pi8anotha P(X|C) me C=0 
        negPossibilities=[]
        for i in range(self.words):
            negPossibilities.append(self.SumOfNeg[i]/self.totalNegWords)
        return negPossibilities

    
    def CounterOfPosPossibility(self): #Epistrefei thn pi8anotha P(X|C) me C=1
        posPossibilities=[]
        for i in range(self.words):
            posPossibilities.append(self.SumOfPos[i]/self.totalPosWords)
        return posPossibilities

    def CounterPSimpleP(self): #Epistrefei thn P(C=1)
        positiveP=self.posNumbers/(self.posNumbers+self.negNumbers)
        return positiveP


    def CounterNSimpleP(self): #Epistrefei thn P(C=0)
        negativeP=self.negNumbers/(self.posNumbers+self.negNumbers)
        return negativeP
    
#"""------------------------------------TEST--------------------------------------------"""

    def getDianisma(self,file,typos): #Epistrefei to dianisma apo ena dwsmeno arxeio metrwntas le3eis aytou.
        location=self.data.read_test()+"\\"+typos+"\\"+file
        ls=[]
        dianisma=[]
        if(path.exists(location)):
            ls=open(location,"r",encoding="utf-8")
            dc = open(self.data.link()+"\\"+"dictionary.txt","r",encoding="utf-8")
            line=dc.readline().strip()
            locationfile=ls.readline()
            loclist=locationfile.split(" ")
            while line:
                counter=0
                if line in locationfile:
                    for i in loclist:
                        i=i.strip(".")
                        i=i.strip(",")
                        i=i.lower()
                        if(line==i):
                            counter=counter+1
                    dianisma.append(counter)
                else:
                    dianisma.append(0)
                line=dc.readline().strip()
            dc.close()
            ls.close()
            return dianisma
        else:
            print("Error: File doesn't exist in thiw folder.")
            sys.exit(0)


    
    def resultCalculator(self,file,typos): #Ypologizei thn pi8anothta P(X1|C)*P(X2|C)*....P(Xn|C) for C=1 and C=0
        dianisma=self.getDianisma(file,typos)
        Neg=1
        Pos=1
        for i in range(self.words):
            Neg=(Neg*(self.negPossibilities[i]**dianisma[i])*1000)
            Pos=(Pos*(self.posPossibilities[i]**dianisma[i])*1000)
        result_neg=Neg*self.negativeP
        result_pos=Pos*self.positiveP
        if(result_neg>result_pos):
            return 0
        elif(result_neg<result_pos):
            return 1

    def Result(self,typos): #a8roisma kritikwn poy htan akribeis.
        if typos != 'pos' and typos !='neg':
            return
        path=self.data.read_test()+"\\"+typos
        counter=0
        file=[]
        for(dirpath,folders,files) in walk(path):
            file.extend(files)
        for i in file:
            result =self.resultCalculator(i,typos)
            if(result==1 and typos=="pos"):
                counter=counter+1
            elif(result==0 and typos=="neg"):
                counter=counter+1
        return counter


    def accuracy(self): # Pososto akribeias
        negative=self.Result("neg")
        positive=self.Result("pos")
        summ=negative+positive
        Score=summ/25000
        return Score
                    
        
#"""----------------------Synarthsh grafoy gia kampylh or8othtas------------------"""

    def graph(self):
        accuracy=[59,67,55,19,5,1]
        train=[100,100,100,100,100,100]
        plt.plot(accuracy,label="Test acc")
        plt.plot(train,label="Train acc")
        plt.title("Kampylh or8othtas")
        plt.ylabel("Accuracy(%)")
        plt.xlabel("Example")
        plt.legend()
        plt.show()



    
#"""------------------------------------Programm running---------------------------"""
a=Bayes()

while True:
    c=input("\nHello!\nWould you like to see a file or to see the accuracy of our algorithm?Text file or accuracy! ")
    c=c.lower()
    if(c=="file"):
        file=input("Input name file(e.x abc.txt): ")
        typos= input("Type the folder of the file(e.x pos for positive reviews or neg for negative reviews): ")
        result=a.resultCalculator(file,typos)
        if(result==0):
            print("The file includes a Negative review!")
        else:
            print("The file includes a Positive review!")
    elif(c=="accuracy"):
        Score=a.accuracy()
        print("Accuracy Score: "+str(int(Score*100))+"%")
    else:
        print("Wrong Input.Closing programm....")
        sys.exit(0)

