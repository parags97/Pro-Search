import urllib.request
from bs4 import BeautifulSoup
import queue
import math
import string
from collections import defaultdict
import io
from array import *
import csv

links = queue.Queue(maxsize=0)
preLinks = ['https://stackoverflow.com/questions','https://stackoverflow.com/questions/tagged/php','https://stackoverflow.com/questions/tagged/xml','https://stackoverflow.com/questions/tagged/c%23','https://stackoverflow.com/questions/tagged/react-native','https://stackoverflow.com/questions/tagged/sql','https://stackoverflow.com/questions/tagged/jquery','https://stackoverflow.com/questions/tagged/ios','https://stackoverflow.com/questions/tagged/javascript','https://stackoverflow.com/questions/tagged/node.js','https://stackoverflow.com/questions/tagged/python','https://stackoverflow.com/questions/tagged/algorithm','https://stackoverflow.com/questions/tagged/java','https://stackoverflow.com/questions/tagged/android']
for i in preLinks:
    links.put(i)
vis_links = []
tokens = []
dictonary = defaultdict(list)
WebText = ''
matrix = [[]]

class packet(object):
    url = ""
    rep = 0
   
    # The class "constructor" - It's actually an initializer 
    def __init__(self):
        self.rep = ""
        self.url = 0
    
def filterToken(tokens):
    for a in tokens:
        if len(a)>0 and (a[len(a)-1] == '.' or a[len(a)-1] == ',' or a[len(a)-1] == '!' or a[len(a)-1] == '?') :
            tokens[tokens.index(a)]=a[0:len(a)-1]
            
    tokens = [a for a in tokens if a.isalpha() and len(a)>0]
    return tokens
    
def addToDict(tokens,url,text):
    global dictonary
    tokens = set(tokens)
    for i in tokens:
        obj = packet()
        rep = text.count(i)
        obj.url = url
        obj.rep = rep
        dictonary[i].append(obj)
 
def generateMatrix():
    global dictonary,vis_links,matrix
    n = len(dictonary)
    m = len(vis_links)
    matrix = [[0]*(m+1) for i in range(n)]
    c = -1
    for i in dictonary:
        c = c+1
        tf = 0
        idf = 0
        matrix[c][0] = i
        for j in range(1,m+1):
            for k in dictonary[i]:
                if(k.url == vis_links[j-1]):
                    tf = k.rep
                    idf = math.log(m/len(dictonary[i]))
                    matrix[c][j]=round(tf*idf, 2)
                    break
            else:
                matrix[c][j]=0
                
def storeMatrix(matrix):
    """with io.open('StackOverFlow.txt', "w", encoding="utf-8") as f:
    f.write('Links:\n')
    for i in range
    for i in matrix:
        line = ''
        for j in i:
            line = line+str(j)+'  '
        f.write(line+'\n')"""
    csvfile = "StackOverflow.csv"
    global vis_links
    matrix.append(vis_links)
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(matrix)
   

    
#Crawler       
while(len(vis_links)<=8000) :
    if (links.empty()!=True) :
        link = links.get()
        print(len(vis_links))
        vis_links.append(link)
        try :
            response = urllib.request.urlopen(link)
        except :
            print("Unable to fetch data from link")
            continue
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        mydivs = soup.findAll("div", {"class": "question"})
        WebText=''
        tdTags=[]
        for tag in mydivs:
            tdTags = tag.find_all("p")
        for elem in tdTags:
            WebText = WebText+' '+elem.get_text()
        WebText=WebText.lower() 
        tokens = filterToken(WebText.split(' '))
        addToDict(tokens,link,WebText)
        
      #tokens = 
        for element in soup.find_all('a'):
            if element.get('href') and '/questions/' in element.get('href') and element.get('href') not in vis_links and 'tagged' not in element.get('href'):
                temp = element.get('href')
                if 'http' in temp:
                    if 'stackoverflow.com' in temp:
                        links.put(temp)
                else:
                    temp = 'https://stackoverflow.com'+temp
                    if temp not in vis_links:
                        links.put(temp)
    else :
        print("No Further Links")
        break


generateMatrix()
storeMatrix(matrix)

    
    
#Query processing
"""query = input("Enter Query - ").lower().split(' ')

doc = []

n = len(dictonary)
m = len(vis_links)
for k in query:
  for i in range(n):
    if(matrix[i][0] == k):
      for j in range(1,m):
        if (matrix[i][j]>1) and vis_links[j] not in doc:
          doc.append(vis_links[j])
          
print("The resulting url related to the searched query are")
for i in doc:
    print(i)
    """