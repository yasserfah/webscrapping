# -*- coding: utf-8 -*-
"""
Created on Thu May  6 00:47:53 2021

@author: admin
""" 
import pandas as pd
liste_mag=[]
list=[]
import time #### Temps de computation pour le scrapping 
start = time.time()
#récupération du HTML
for i in range(1,5000,50):
  # Requete
  import requests
  r=requests.get('https://www.imdb.com/search/title/?title_type=feature&num_votes=5000,&sort=user_rating,desc&start='+str(i)+'&ref_=adv_nxt')
  #Parsing du text en html à l'aide de BeautifulSOup
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(r.text, 'html.parser')
  #Récupération des balises qui contiennent l'information pertinente(ici l'url)
  results=soup.find_all('div',attrs={"class":"lister-item-image float-left"})
  #Création d'une liste avec l'ensemble des url
  for j in range(0,len(results)):
    # Alimentation de la liste par les url
    list.append('https://www.imdb.com'+results[j].find_all('a')[0]["href"])
    #print(list)
for i in range(0,len(list)): ##### Pour chaque url dans l'objet liste défini plus haut 
    #print(ele)
    r = requests.get(list[i])   #### Requete
    soup = BeautifulSoup(r.text, 'html.parser')#Parsing du text en html à l'aide de BeautifulSOup
    #Récupération des balises adéquates et filtrer pour récuperer les bons éléments
    try:# Test des opérations
     titles=soup.find('h1').text.strip()
     #print(titles)
     note=soup.find('span',attrs={'itemprop':'ratingValue'}).text.strip() if soup.find(attrs={'itemprop':'ratingValue'}) else 'XXX'
     print(note) 
     score=soup.find('div',attrs={'class':'metacriticScore score_favorable titleReviewBarSubItem'}).text.strip() if soup.find(attrs={'class':'metacriticScore score_favorable titleReviewBarSubItem'}) else 'XXX'
     #print(score) 
     votes=soup.find('span',attrs={'class':'small'}).text.strip() if soup.find(attrs={'class':'small'}) else 'XXX'
     #print(votes) 
     directors=soup.find('div',attrs={'class':'credit_summary_item'}).text[10:].strip() if soup.find(attrs={'class':'credit_summary_item'}) else 'XXX'
     #print(directors) 
     writers=soup.find_all('div',attrs={'class':'credit_summary_item'})[1].text[9:].strip() if soup.find(attrs={'class':'credit_summary_item'}) else 'XXX'
     #print(writers) 
     duree=soup.find('time').text.strip() if soup.find('time') else 'XXX'
     #print(duree)     
     genre=soup.find_all('div',attrs={'class':'see-more inline canwrap'})[1].text[8:].strip() if soup.find(attrs={'class':'see-more inline canwrap'}) else 'XXX'
     #print(genre) 
     date=soup.find_all('div',attrs={'class':'txt-block'})[10].contents[2] if soup.find(attrs={'class':'txt-block'}) else 'XXX'
     #print(date)
     year=soup.find_all('div',attrs={'class':'txt-block'})[10].text[-35:-31] if soup.find(attrs={'class':'txt-block'}) else 'XXX'
    
    #print(year)
     pays=soup.find_all('div',attrs={'class':'txt-block'})[8].text[9:] if soup.find(attrs={'class':'txt-block'}) else 'XXX'
     #print(pays)
     filming_location=soup.find_all('div',attrs={'class':'txt-block'})[12].contents[3].contents[0] if soup.find(attrs={'class':'txt-block'}) else 'XXX'
    #print(filming_location)
     nbre_reviews=soup.find_all('div',attrs={'class':'user-comments'})[0].contents[11].contents[0][8:13] if soup.find(attrs={'class':'user-comments'}) else 'XXX'
     #print(nbre_reviews)
     filmographie=soup.find('div',attrs={'class':'inline canwrap'}).text.strip() if soup.find(attrs={'class':'inline canwrap'}) else 'XXX'
     budget=soup.find_all('div',attrs={'class':'txt-block'})[13].text[9:20].strip() if soup.find(attrs={'class':'txt-block'}) else 'XXX'
     #print(budget)
     Opening_weekend_USA=soup.find_all('div',attrs={'class':'txt-block'})[14].text[22:34].strip() if soup.find(attrs={'class':'txt-block'}) else 'XXX'
    #print(Opening_weekend_USA)
     Gross_USA=soup.find_all('div',attrs={'class':'txt-block'})[15].text[13:24] if soup.find(attrs={'class':'txt-block'}) else 'XXX'
     #Gross_USA = [float(str(i).replace(",", "")) for i in Gross_USA]
    #print('Gross_USA')
     Cumulative_worldwide_gross=soup.find_all('div',attrs={'class':'txt-block'})[16].text[30:43] if soup.find(attrs={'class':'txt-block'}) else 'XXX'
     #Cumulative_worldwide_gross = [float(str(i).replace(",", "")) for i in Cumulative_worldwide_gross]

    #print(Cumulative_worldwide_gross) 
     Runtime=soup.find_all('div',attrs={'class':'txt-block'})[19].text[9:17].strip() if soup.find(attrs={'class':'txt-block'}) else 'XXX'
    #print(Runtime)
     Sound_Mix=soup.find_all('div',attrs={'class':'txt-block'})[20].text[11:].strip() if soup.find(attrs={'class':'txt-block'}) else 'XXX'
    #print(Sound_Mix)
     Color=soup.find_all('div',attrs={'class':'txt-block'})[21].text[7:].strip() if soup.find(attrs={'class':'txt-block'}) else 'XXX'
    #print(Color) 
     Aspect_ratio=soup.find_all('div',attrs={'class':'txt-block'})[22].text[15:].strip() if soup.find(attrs={'class':'txt-block'}) else 'XXX'
    #print(Aspect_ratio)
     
    # Stockage des élements dans une liste
     liste_mag.append((titles,note,score,votes,directors,writers,duree,genre,date,filming_location,nbre_reviews,budget,Opening_weekend_USA,Gross_USA,Cumulative_worldwide_gross,Runtime,Sound_Mix,Color,Aspect_ratio,filmographie,year,pays))
    except:# S'il y a un problème, on passe à la prochaine valeur
      continue
  #Conversion de la liste de tuples en dataframe
df=pd.DataFrame(liste_mag,columns=['titles','note','score','votes','directors','writers','duree','genre','date','filming_location','nbre_reviews','budget','Opening_weekend_USA','Gross_USA','Cumulative_worldwide_gross','Runtime','Sound_Mix','Color','Aspect_ratio','filmographie','year','pays'])
print(df)
#Conversion du dataframe en csv
df.to_csv('imdb3.csv',index=False,encoding='utf-8') 
print("Computation time =",  time.time() - start )#le temps de computation