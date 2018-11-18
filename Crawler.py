import urllib.request
from bs4 import BeautifulSoup
import queue
import math
import string
from collections import defaultdict
import io

links = queue.Queue(maxsize=0)
links.put('https://stackoverflow.com/questions')
vis_links = []
tokens = []
dictonary = defaultdict(list)

class packet(object):
    url = ""
    rep = 0
   
    # The class "constructor" - It's actually an initializer 
    def __init__(self):
        self.rep = ""
        self.url = 0
    
def filterToken(tokens):
    """invalidChars = set(string.punctuation.replace("-", ""))
    invalidChars = set(string.punctuation.replace(",", ""))
    tokens = [a for a in tokens if not any(char in invalidChars for char in a) and not a.isnumeric()]
    tokens = [a for a in tokens if not a.startswith(" ")]
    tokens = [a for a in tokens if not a.endswith(" ")]"""
    for a in tokens:
        if a[len(a)-1] == '.' or a[len(a)-1] == ',' :
            a = a[0:len(a)-2]
    tokens = [a for a in tokens if a.isalpha()]
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
 
#Crawler       
while(len(vis_links)<=20) :
    if (links.empty()!=True) :
        link = links.get()
        vis_links.append(link)
        try :
            response = urllib.request.urlopen(link)
        except :
            print("Unable to fetch data from link")
            continue
        print("Visiting Link : ",link)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        mydivs = soup.findAll("div", {"class": "question"})
        for tag in mydivs:
            tdTags = tag.find_all("p")
        for elem in tdTags:
            WebText = WebText+elem.get_text()
        tokens = filterToken(WebText.split(' '))
        addToDict(tokens,link,WebText)
        
      #tokens = 
        for element in soup.find_all('a'):
            if element.get('href') and '/questions' in element.get('href') and element.get('href') not in vis_links:
                temp = element.get('href')
                if 'http' in temp:
                    links.put(temp)
                else:
                    temp = 'https://stackoverflow.com'+temp
                    links.put(temp)
    else :
        print("No Further Links")
        break


#tf-idf matrix
from array import *
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
                 
            
with io.open('matrix.txt', "w", encoding="utf-8") as f:
    for i in matrix:
        line = ''
        for j in i:
            line = line+str(j)+'  '
        f.write(line+'\n')
    
#Query processing
query = input("Enter Query - ").lower().split(' ')

doc = []

for k in query:
  for i in range(n):
    if(matrix[i][0] == k):
      for j in range(1,m):
        if (matrix[i][j]>1) and vis_links[j] not in doc:
          doc.append(vis_links[j])
          
print("The resulting url related to the searched query are")
for i in doc:
    print(i)