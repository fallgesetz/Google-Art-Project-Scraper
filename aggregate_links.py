#!/usr/bin/env python
"""
Spider the google arts project for urls.


Note that this spider is pretty dumb and is not resiliant to changes in the sitemap.
The trade off, of course, is that we keep the code base simple. (A more resiliant implementation
might use breadth first search and a dictionary cache.)

-Leah Xue
June 19th, 2011
"""
#pip
from BeautifulSoup import BeautifulSoup, SoupStrainer
#standard library
import sys
import urllib2
import re
#mine
import imagescraper

main_url = "http://www.googleartproject.com"

def get_paintings_from_museum(museum_link):
    """
    
    Note:
    Main should just call get_museum_urls()
    """
    url = main_url + museum_link
    f = urllib2.urlopen(url)
    html = f.read()
    
    links = SoupStrainer("a", href=re.compile('/%s/(.*?)' % ( "museums")))
    soup = BeautifulSoup(html, parseOnlyThese=links)
    links_list = [tag['href'].encode('utf-8') for tag in soup]
    
    ret_dict = {} #hash for uniqueness
    for link in links_list:
        tokenized_url = link.split('/')
        if len(tokenized_url) == 4:
             ret_dict[link] = 1
    return ret_dict.keys()

def get_museum_urls():
    f = urllib2.urlopen(main_url)
    html = f.read()
    
    links = SoupStrainer("a", href=re.compile('/%s/(.*?)' % ( "museums")))
    soup = BeautifulSoup(html, parseOnlyThese=links)
    
    #Just a hunch, this is faster than set?
    links_dict = {}
    for tag in soup:
        links_dict[tag['href'].encode('utf-8')] = 1
    
    # we can distinguish between links to museums and links to individual art work by counting the number of /s
    total_urls = []
    for link in links_dict.keys(): 
        if len(link.split('/')) == 3:
            print link
            total_urls += get_paintings_from_museum(link)
    
    return total_urls

def scrape_all():
    
def main():
    blah = get_museum_urls()
    #generate all the 

if __name__ == "__main__":
    main()