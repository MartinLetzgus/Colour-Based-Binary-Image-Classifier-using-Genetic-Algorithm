import random
import os
import cv2
from operator import attrgetter
import pickle

class Classifier:
    def __init__(self,wR,wG,wB,tR,tG,tB):
        self.wR = wR
        self.wG = wG
        self.wB = wB
        self.tR = tR
        self.tG = tG
        self.tB = tB
        
    def __str__(self):
        return(str(self.wR) + ', ' + str(self.wG) + ', ' + str(self.wB) + ', ' + str(self.tR) + ', ' + str(self.tG) + ', ' + str(self.tB)  )
        
    def evaluate(self, dataset):
    ###Evaluate the accuracy of the classifier on a dataset
        score_1 = 0
        score_2 = 0
        
        
        for hist in dataset.data_1:
            size = sum(hist[0])
            b = sum(hist[0][self.tB:])/size
            r = sum(hist[1][self.tR:])/size
            g = sum(hist[2][self.tG:])/size
            
            if (r*self.wR + b*self.wB + g*self.wG > 0):
                score_1 += 1
                
        score_1/=len(dataset.data_1)
               
        for hist in dataset.data_2:
            size = sum(hist[0])
            b = sum(hist[0][self.tB:])/size
            r = sum(hist[1][self.tR:])/size
            g = sum(hist[2][self.tG:])/size
            
            if (r*self.wR + b*self.wB + g*self.wG < 0):
                score_2 += 1
                
        score_2/=len(dataset.data_2)
                
        self.score = (score_2+score_1)/2
        return((score_2+score_1)/2)

#---------------------------------------#
        
class Classifier_random(Classifier):
    
    def __init__(self):
        self.wR = random.randint(-100,100)
        self.wG = random.randint(-100,100)
        self.wB = random.randint(-100,100)
        self.tR = random.randint(0,256)
        self.tG = random.randint(0,256)
        self.tB = random.randint(0,256)
        
#---------------------------------------#
        
class Generation:
    def __init__(self, indiv,evolution):
        self.size = len(indiv)
        self.indiv = indiv
        self.evolution = evolution
        
    def __str__(self):
        return('nb indiv   : ' + str(len(self.indiv)) + '\n' 
               'best score : ' + str(self.get_best().score) + '\n'
               'best indiv : ' + str(self.get_best()) + '\n'
               'mean score : ' + str(self.get_mean()))
              
            
    def evaluate(self, dataset):
        for i in (self.indiv):
            i.evaluate(dataset)
        self.evolution.append([self.get_best().score,self.get_mean(),str(self.get_best())])
            
    def sort(self):
        best = sorted(self.indiv, key=attrgetter('score'),reverse=True)
        self.indiv = best

    def get_best(self):
        return(max(self.indiv, key=attrgetter('score')))
    
    def get_mean(self):
        return(sum(clas.score for clas in self.indiv)/len(self.indiv))
        
    def make_new_gen(self,nb_parents,mutation_rate=0.01):
        indiv = []
        self.sort()
        for i in range (self.size):
            p1 = random.choice(self.indiv[:nb_parents])
            p2 = random.choice(self.indiv[:nb_parents])
            if (random.random()>mutation_rate):
                wR = int((p1.wR if (random.random()<0.5) else p2.wR) + random.gauss(0,3))
            else:
                wR = random.randint(-100,100)
            if (random.random()>mutation_rate):
                wG = int((p1.wG if (random.random()<0.5) else p2.wG) + random.gauss(0,3))
            else:
                wG = random.randint(-100,100)
            if (random.random()>mutation_rate):
                wB = int((p1.wB if (random.random()<0.5) else p2.wB) + random.gauss(0,3))
            else:
                wB = random.randint(-100,100)
            if (random.random()>mutation_rate):
                tR = int((p1.tR if (random.random()<0.5) else p2.tR) + random.gauss(0,3))
            else:
                tR = random.randint(0,256)
            if (random.random()>mutation_rate):
                tG = int((p1.tG if (random.random()<0.5) else p2.tG) + random.gauss(0,3))
            else:
                tG = random.randint(0,256)
            if (random.random()>mutation_rate):
                tB = int((p1.tB if (random.random()<0.5) else p2.tB) + random.gauss(0,3))
            else:
                tB = random.randint(0,256)
            indiv.append(Classifier(wR,wG,wB,tR,tG,tB))            
            
        return Generation(indiv,self.evolution)    
    
    def save_evolution(self,path='evolution.pickle'):
        with open(path, 'wb') as handle:
            pickle.dump(self.evolution, handle)
         
#---------------------------------------#
                
class First_Generation(Generation):               
    def __init__(self, size):
        self.size = size
        self.indiv = []
        self.evolution = []
        for i in range (size):
            c = Classifier_random()
            self.indiv.append(c)     
            
#---------------------------------------#
                
class Dataset:
    def __init__(self, source_folder_1, source_folder_2):
        self.data_1 = []
        self.data_2 = []
        
        for f in os.listdir(source_folder_1):
            hist = []
            image = cv2.imread(str(source_folder_1) + "\\" + str(f)) #Image here is stored as BGR
            for i in range (3):
                hist.append(cv2.calcHist([image],[i],None,[256],[0,256]))
            self.data_1.append(hist)
        
        for f in os.listdir(source_folder_2):
            hist = []
            image = cv2.imread(str(source_folder_2) + "\\" + str(f)) #Image here is stored as BGR
            for i in range (3):
                hist.append(cv2.calcHist([image],[i],None,[256],[0,256]))
            self.data_2.append(hist)
            
            
    def __str__(self):
        return(str(len(self.data_1)) + ' ' + str(len(self.data_2)))
        
    def save(self,path='dataset.pickle'):
        with open(path, 'wb') as handle:
            pickle.dump(self, handle)
        
            
#---------------------------------------#