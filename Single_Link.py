import urllib.request
from bs4 import BeautifulSoup

def filterToken(tokens):
    for a in tokens:
        print(a)
        if len(a)>0 and (a[len(a)-1] == '.' or a[len(a)-1] == ',' or a[len(a)-1] == '!' or a[len(a)-1] == '?') :
            tokens[tokens.index(a)]=a[0:len(a)-1]
            
    tokens = [a for a in tokens if a.isalpha() and len(a)>0]
    return tokens

link = "https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class"
try :
    response = urllib.request.urlopen(link)
except :
    print("Unable to fetch data from link")

print("Visiting Link : ",link)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
mydivs = soup.findAll("div", {"class": "question"})

for tag in mydivs:
    tdTags = tag.find_all("p")

text = ''
for elem in tdTags:
    if(len(elem.get_text())>0):
        text = text+" "+elem.get_text()
    
toke=filterToken(text.split(' '))


asw = set(vis_links)