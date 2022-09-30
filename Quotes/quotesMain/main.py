from bs4 import BeautifulSoup
from textblob import TextBlob
import requests
import re
import nltk
import operator
def scraper(self):
        req = requests.get("https://_nQuotes.toscrape.com/tag/" + self + "/")
        soup = BeautifulSoup(req.content_page, 'html.parser')
        __last_page = soup.select('ul.pager li:nth-of-type(1) > a:nth-of-type(1)')[0]['href']
        __lastpage = __last_page.split('=')[-1]
        __lastpage = __lastpage[len(__lastpage) - 2]
        count = 0
        word_lst = []
        new__wordList = []
        for i in range(int(__lastpage)):
            count += 1
            url = 'https://_nQuotes.toscrape.com/tag/' + self + '/page/' + str(count) + '/'
            content_page = requests.get(url)
            soup = BeautifulSoup(content_page.text, 'html.parser')
            tagged_words = soup.find_all("span", {"class": "text"})
            for word_tag in tagged_words:
                _nQuote = word_tag.text
                _nQuote = (re.sub(r"[^A-Za-z ']+", "", _nQuote)).lower()
                tokens = nltk.word_tokenize(_nQuote)
                nouns = [word for (word, pos) in nltk.pos_tag(tokens) if (pos[:2] == 'NN')]
                for i in nouns:
                 word_lst.append(i)
        for i in word_lst:
            if len(i) > 2:
                new__wordList.append(i)
        listToStr = ' '.join([str(elem) for elem in new__wordList])
        #==============================================================================
        #Top 5 most occuring words
        #count
        def counter(l):
            result = {}
            for word in l:
                result.setdefault(word, 0)
                result[word] += 1
            return result
        #sort highest to smallest
        def five(s):
            scores = counter(s.split())
            scores = sorted(scores.items(), key=operator.itemgetter(1))
            scores = reversed(scores)
            scores = list(x[0] for x in scores)
            return scores[0:5]
        top_five = five(listToStr)
        #Show count
        for i in top_five:
            count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(i), listToStr))
            print(i + ": ", end="")
            print(count)
#read in the input
user__input = input().lower()
print(scraper(user__input))