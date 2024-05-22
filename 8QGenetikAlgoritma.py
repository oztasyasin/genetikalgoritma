#Implementation of N-Queen Problem by Dr. Zeki Yetgin, October 2018
#Just change the input functions to implement any other problem.

import time,random, numpy as np, math, copy
from collections import namedtuple

def GenetikAlgoritma(ilklendirmeFonk,objektifFonk,seleksiyonFonk,caprazlamaFonk, mutasyonFonk):
    print("lutfen bekleyin...biraz zaman alacak...")
    model=modelYarat()              #model algoritma parametrelerini kapsıyor
    Pop = ilklendirmeFonk(model)    #başlangıç populasyon random olarak oluşturuluyor
    #popülasyon her guncellendinde, objektif degerleri hesap et ve mevcut iyiyi (eliti) bul
    Degerler = objektifHesapla(Pop) #tüm bireylerin objektif değerleri hesaplanıyor
    elitID = Degerler.argmin()      #elit = mevcut popülasyonun en iyisi bulunuyor
    best = Pop[elitID]              #best = global en iyi = başlangıçta elit
    bestDeger = Degerler[elitID] 
    for iter in range(model.maxIter):
                sonrakiPop=[]
                #elit bireyi yeni populasyona ekle
                sonrakiPop.append(Pop[elitID])
                #cocuklari uret, mutasyona uğrat ve yeni populasyona ekle
                for i in range(1, model.popSize):
                        parent1ID = seleksiyonFonk(Degerler, model)
                        parent2ID = seleksiyonFonk(Degerler, model)
                        child = caprazlamaFonk(Pop[parent1ID], Pop[parent2ID], model)
                        child = mutasyonFonk(child,model)
                        sonrakiPop.append(child)
                Pop = sonrakiPop
                #popülasyon güncellendi. hemen objektif değerleri ve eliti bul
                Degerler = objektifHesapla(Pop)
                elitID=Degerler.argmin()
                elitDeger = Degerler[elitID]
                #en iyiyi (best) takip et 
                if elitDeger<bestDeger:
                      bestDeger = elitDeger
                      best =Pop[elitID]
                print("%d.iterasyonda en iyi objektif deger: "%iter,bestDeger)
                if bestDeger==0:
                    break
            
    print("En iyi cozum: ",np.array(best), " ve objektif degeri: ", bestDeger)
    return best

def objektifHesapla(Pop):
    PopSize=len(Pop)
    degerler=np.zeros(PopSize)
    for i in range(PopSize):
        degerler[i]=objektifFonk(Pop[i])
    return degerler

def mutasyonFonk(birey, model):
    if random.random() < model.mutasyonOrani:
        index=random.randrange(model.dim)
        birey[index]=random.randrange(model.dim)
    return birey

def seleksiyonFonk(Degerler, model): #Turnuva: turnuvaSize kadar Pop dan ID seç-->sample() ile basit
    adaylarID=random.sample(range(model.popSize),model.turnuvaSize) 
    degerler=Degerler[adaylarID]     #vektörel işlem..degerler bir dizi = adayların objektif degerleri
    kazananID=degerler.argmin()
    return adaylarID[kazananID]                  #turnuvadaki en iyi ID
	       
	    	
def caprazlamaFonk(parent1,parent2, model): #tek noktalı (single point) çaprazlama
    child=parent1.copy();
    if random.random() < model.caprazlamaOrani:
        n = len(parent1)
        point = random.randint(0, n - 1)
        child[point:n]= parent2[point:n]
    return child  

def caprazlamaFonk_2Point(parent1, parent2, model):
    child = parent1.copy()
    if random.random() < model.caprazlamaOrani:
        n = len(parent1)
        point1, point2 = sorted(random.sample(range(n), 2))
        child[point1:point2] = parent2[point1:point2]
    return child


def modelYarat():
    model=namedtuple('model', 'popSize,dim,nElits,mutasyonOrani, turnuvaSize, maxIter');
    model.maxIter=100;
    model.popSize=1000      #kromozom sayısı = cozum sayisi	
    model.dim=8            #gen sayisi = bir cozumun boyutu = vezir sayisi
    model.mutasyonOrani=0.05
    model.caprazlamaOrani=0.90
    model.turnuvaSize=10    #turnuva tabanlı seleksiyonda, turnuvaya katılacakların sayisi
    return model

def objektifFonk(cozum):
    '''number of queens that attack each other'''
    y=0
    dim=len(cozum)		#dim = cozum boyutu = vezir sayisi
    tahta = np.zeros((dim,dim));
    for i in range(dim):      	  #tahtada sadece vezir pozisyonları 1 olsun, digerleri 0. 
       tahta[cozum[i],i] = 1

    for i in range(dim):      #aynı satirdaki vezirleri say
        say = np.sum(tahta[i])
        if say>=2:
            y = y + say

    for k in range(2):  #aynı sol ve sağ çaprazdaki vezirleri say
        for i in range(-dim+1,dim): 
            say = np.sum(np.diagonal(tahta,i))
            if say>=2:
                y = y + say
        tahta=tahta[::-1]  #diagonal fonksiyonu sadece sol çapraz için çalışıyor. sağ çapraz için tahtayı tersleyip aynı işlemi uygula  

    return y   
	
def ilklendirmeFonk(model):
    pop=[]  
    for i in range(model.popSize):
        birey=[]    
        for i in range(model.dim):
                birey.append(random.randint(0,model.dim-1))
        pop.append(birey)
    return pop

def main():
	start = time.time()
	GenetikAlgoritma(ilklendirmeFonk,objektifFonk,seleksiyonFonk,caprazlamaFonk, mutasyonFonk)
	end = time.time()
	print("time elapsed(sec)=",end - start)

def main_2point():
    results = []
    for popSize in [500, 1000]:
        for mutasyonOrani in [0.01, 0.05, 0.1]:
            for caprazlamaOrani in [0.8, 0.9]:
                model = modelYarat()
                model.popSize = popSize
                model.mutasyonOrani = mutasyonOrani
                model.caprazlamaOrani = caprazlamaOrani
                start = time.time()
                best = GenetikAlgoritma(ilklendirmeFonk, objektifFonk, seleksiyonFonk, caprazlamaFonk_2Point, mutasyonFonk)
                end = time.time()
                duration = end - start
                results.append((popSize, mutasyonOrani, caprazlamaOrani, duration, best))
                print(f"popSize: {popSize}, mutasyonOrani: {mutasyonOrani}, caprazlamaOrani: {caprazlamaOrani}, duration: {duration}, best: {best}")

    # Print results in a table format
    print("\nResults:\n")
    print("popSize | mutasyonOrani | caprazlamaOrani | duration (sec) | best solution")
    for res in results:
        print(f"{res[0]}      | {res[1]:<14} | {res[2]:<14} | {res[3]:<14} | {res[4]}")


main_2point()	
