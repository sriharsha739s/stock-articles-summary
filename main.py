from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import re
import json
from summariser import read_article, sentence_similarity, build_similarity_matrix, generate_summary, generate_summary_from_file

#return article link using api
def getLinks():
    r = requests.get(url='https://stocknewsapi.com/api/v1/category?section=general&items=5&source=Market+Watch&token=6zbj08u3sjcst3lfgznjjesgsro7mvoehmjugbzi')
    links_dict = r.json()
    links = []
    for i in links_dict['data']:
        links.append(i['news_url'])
    return links



#retreving article content from url
def getContent(url):
    req = Request(url, headers={'User-Agent':'Chrome'})
    webpage = urlopen(req).read()
    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'html5lib')
        result = ''
        for item in soup.find_all('div', attrs={'class': 'paywall'}):
            result = item
    return(str(result))


#removing html tags from article content
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

#when getting data from html, lots of lines (\n) and extra spaces so need to remove that
def removeSpaces(string):
    phrases = string.split('.')
    sentences = []
    for sentence in phrases:
        s = sentence.lstrip()
        s = s.rstrip()
        s = s.replace('\n', '')
        sentences.append(s)
    return sentences
        

print(generate_summary(removeSpaces(cleanhtml(getContent('https://www.marketwatch.com/story/stocks-are-likely-to-go-sideways-from-here-heres-how-to-keep-your-portfolio-moving-forward-11628275049?mod=home-page'))),10))