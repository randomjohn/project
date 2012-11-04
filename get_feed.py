# -*- coding: utf-8 -*-

# the purpose of this file is to extract the text contents from blogs that are given in a list
# (either feedlist.txt or one supplied as an argument)

import os
import sys
import re
from datetime import datetime as dt
import json
import feedparser
from BeautifulSoup import BeautifulStoneSoup
from nltk import clean_html
import codecs
import link_extractor as le
import filename_munger as fm

# Example feed:
# http://feeds.feedburner.com/oreilly/radar/atom


def cleanHtml(html):
    """
    Clean up any html
    """
    return BeautifulStoneSoup(clean_html(html),
                              convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents

def get_feed(blogurl,bloglist):
    """
    Get a blog and write its contents out to a json file
    """
    try:
        feed_url = le.extract_feed_link_from_url(blogurl)
        fp = feedparser.parse(feed_url)
    except:
        "Unable to retrieve or parse %s" % blogurl
        return
    try:
        print >> sys.stderr, "Fetched %s entries from '%s'" % (len(fp.entries[0].title.encode('ascii','ignore')), fp.feed.title.encode('ascii','ignore'))
    except IndexError:
        print >> sys.stderr, "Retrieved no entries from '%s'" % feed_url
        return None
        
    blog_data = {'blogurl':blogurl,'title': fp.feed.title, 'blogroll':le.extract_links_from_url(blogurl,bloglist)}
    blog_posts = [blog_data]
    for e in fp.entries:
        try:
            blog_posts.append({'blogtitle':fp.feed.title,
                'content': cleanHtml(e.content[0].value), 
                'link': e.links[0].href,
                'links':le.extract_links(e.content[0].value),
                'bloglinks':le.extract_links_from_list(e.content[0].value,bloglist)
                })
        except AttributeError:
            blog_posts.append({'blogtitle':fp.feed.title, 
                'content': cleanHtml(e.summary), 
                'link': e.links[0].href,
                'links':le.extract_links(e.summary),
                'bloglinks':le.extract_links_from_list(e.summary,bloglist)
                })
    
    if not os.path.isdir('out'):
        os.mkdir('out')
    
    #out_file = '%s__%s.json' % (fp.feed.title.replace("'","").replace("-",""), dt.utcnow())
    out_file = '%s.json' % (fm.munge(fp.feed.title))
    #out_file = 'foo.json'
    f = codecs.open(os.path.join(os.getcwd(), 'out', out_file), 'w',encoding='iso-8859-1')
    f.write(json.dumps(blog_posts))
    f.close()
    print >> sys.stderr, 'Wrote output file to %s' % (f.name, )
    return f.name

    
def main():
    if len(sys.argv)>1:
        blog_file = sys.argv[1]
    else:
        # use a default if none supplied
        blog_file='feedlist.txt'
    apcount={}
    wordcounts={}
    bloglist=[line for line in file(blog_file)]
    for blogurl in bloglist:
        get_feed(blogurl,bloglist)
    
    
if __name__=="__main__":
    main()