# -*- coding: utf-8 -*-

import feedparser
import re

def get_word_counts(url):
    d = feedparser.parse(url)
    wc = {}
    
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
            
        #print e.summary
            
        
        words = get_words(getattr(d.feed, 'title', 'Unknown title') + " " + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return getattr(d.feed, 'title', 'Unknown title'), wc
    
def get_words(html):
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    return [word.lower() for word in words if word != ' ']
            
    
apcount = {}
wordcounts = {}
feedlist = [line for line in file('feedlist.txt')]
for feedurl in feedlist:
    title, wc = get_word_counts(feedurl)
    wordcounts[title] = wc
    for word, count in wc.items():
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1

word_list = []
for w, bc in apcount.items():
    frac = float(bc)/len(feedlist)
    if frac > 0.1 and frac < 0.5:
        word_list.append(w)
        
print "World list"
print word_list
