# extract links from HTML text

from BeautifulSoup import BeautifulSoup
import urllib2
import unicodedata
import re
from sys import stderr

def extract_links(text):
    # return all the domains to which 
    extracted_links = dict()
    try:
        text_soup = BeautifulSoup(text)
    except HTMLParser.HTMLParseError:
        print 'Failed to extract links due to parse error'
    all_links = text_soup.findAll('a')
    feedburner_re = re.compile('feedburner',flags=re.I)
    num_ip_re = re.compile('https?:\/\/([0-9]+\.){3,3}[0-9]+:?.*')
    # old tld (\.com|\.co|\.uk|\.org|\.net|\.cc|\.tw|\.ly|\.tv|\.cc|\.us|\.co|\.edu|\.eu|\.ch|\.dk|\.se|\.gov|\.de|\.mil|\.gl|\.ca|\.nl|\.fr|\.pl|\.es|\.br|\.fi|\.no|\.ru|\.au|\.sa|\.nz|\.il|\.name|\.info|\.biz|\.kr)
    dom_re = re.compile('(https?:\/\/[a-zA-Z0-9-]+)(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})(\/)?(blog)?',flags=re.I)
    for lnk in all_links:
        if lnk.has_key('href'):
            try:
                this_key=lnk['href'] # + "|" + lnk.contents[0]
            except TypeError:
                this_lnk=unicodedata.normalize('NFKD', lnk['href']).encode('ascii','ignore')
                #this_contents=unicodedata.normalize('NFKD', lnk.contents[0]).encode('ascii','ignore')
                this_key=this_lnk # + "|" + this_contents

            # for this purpose, I'm only interested in domain
            #print this_key
            #print dom_re.findall(this_key)
            if this_key.find('mailto:')>-1 or len(num_ip_re.findall(this_key))>0:
                # skip mailto and numerical IP addr links
                continue
            try:
                this_key=''.join(dom_re.findall(this_key)[0])
            except IndexError:
                print 'NOTE: found a link I couldn''t parse: ' + this_key
            #print '--> ' + this_key + '\n'
            # get rid of feedburner stuff, because it is put in automatically
            if this_key!='http://feeds.feedburner.com/':
                extracted_links.setdefault(this_key,0)
                extracted_links[this_key] += 1
    return extracted_links

def extract_links_from_list(text,bloglist):
    # return all the domains to which 
    extracted_links = dict()
    try:
        text_soup = BeautifulSoup(text)
    except HTMLParser.HTMLParseError:
        print 'Failed to extract links due to parse error'
    all_links = text_soup.findAll('a')
    feedburner_re = re.compile('feedburner',flags=re.I)
    dom_re = re.compile('(https?:\/\/[a-zA-Z0-9-]+)(\.[a-zA-Z0-9-]+)?(\.[a-zA-Z0-9-]+)?(\.com|\.co\.uk|\.org|\.net|\.cc|\.tw|\.ly|\.tv|\.cc|\.us|\.co|\.edu)(\/blog)',flags=re.I)
    for lnk in all_links:
        if lnk.has_key('href'):
            try:
                this_key=lnk['href'] # + "|" + lnk.contents[0]
            except TypeError:
                this_lnk=unicodedata.normalize('NFKD', lnk['href']).encode('ascii','ignore')
                #this_contents=unicodedata.normalize('NFKD', lnk.contents[0]).encode('ascii','ignore')
                this_key=this_lnk # + "|" + this_contents

            # for this purpose, I'm only interested if they are a part of the blog list
            # strip of trailing slash, if any
            if len(this_key)>1 and this_key[len(this_key)-1]=='/':
                this_key = this_key[0:len(this_key)-1]
            #print this_key
            found_blog=0
            for this_blog in bloglist:
                if this_key.find(this_blog)>-1:
                    this_key=this_blog
                    found_blog=1
                    break
            #print '--> ' + this_key + '\n'
            # get rid of feedburner stuff, because it is put in automatically
            if found_blog==1:
                extracted_links.setdefault(this_key,0)
                extracted_links[this_key] += 1
    return extracted_links

def extract_feed_link(text):
    """
    Return the link to the feed in a blog
    Assumes the blog has link tags with rel of alternate, either Feed, Atom, or RSS in title, and an href
    """
    this_feed_link = ""
    try:
        text_soup=BeautifulSoup(text)
    except HTMLParser.HTMLParseError:
        print "Failed to extract feed link due to parse error"
    all_alternates = text_soup.findAll('link',rel='alternate')
    for lnk in all_alternates:
        if lnk.has_key('title'):
            this_title=lnk['title'].lower()
            # we ignore comments feeds
            if (this_title.find('atom')>-1 or this_title.find('rss')>-1 or this_title.find('feed')>-1) and this_title.find('comments')==-1:
                this_feed_link = lnk['href']
                # just find the first feed link
                break
    return this_feed_link
    
def extract_title(text):
    """
    Return the link to the feed in a blog
    Assumes the blog has link tags with rel of alternate, either Feed, Atom, or RSS in title, and an href
    """
    this_feed_link = ""
    try:
        text_soup=BeautifulSoup(text)
    except HTMLParser.HTMLParseError:
        print "Failed to extract feed link due to parse error"
    this_title = text_soup.find('title').contents[0]
    return this_title

def extract_feed_link_from_url(blog_url):
    blog_text = urllib2.urlopen(blog_url).read()
    feed_url = extract_feed_link(blog_text)
    return feed_url
    
def extract_links_from_url(blog_url,bloglist):
    blog_text = urllib2.urlopen(blog_url).read()
    links = extract_links_from_list(blog_text,bloglist).keys()
    return links
    
def extract_title_from_url(blog_url):
    blog_text = urllib2.urlopen(blog_url,timeout=10).read()
    return extract_title(blog_text)
