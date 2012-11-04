# the purpose of this module is to get word counts from a blog stored
# as a local json file, and store them in a term document matrix in out\tdf.txt
import json
import re
import os
import codecs

def main():
    # get json files
    json_files = [fil for fil in os.listdir("out/") if fil.endswith(".json")]
    
    # Loop over all the entries
    blog_wc = {}
    stop_words = ['a','an','the']
    master_word_list = set()
    for fil in json_files:
        # process each file, create a dictionary of words and frequencies
        print "Processing: " + fil
        wc={}
        blog_json = json.load(file ("out/" + fil))
        blog_url = blog_json[0]['blogurl'].strip()
        for i in range(1,len(blog_json)):
    
            # Extract a list of words
            try:
                words=getwords(blog_json[i]['content'][0].encode('ascii','ignore'))
            except IndexError:
                # I guess our json had no content, so continue
                break        
            for word in words:
                if word in stop_words: continue
                wc.setdefault(word,0)
                master_word_list.add(word)
                wc[word]+=1
        # now append the word count dictionary to a master dictionary        
        blog_wc[blog_url]=wc  
    
    # now, convert our dictionary of dictionaries into a tdm, and write it out          
    out = codecs.open(os.path.join(os.getcwd(), 'out', 'tdf.txt'), 'w',encoding='iso-8859-1')
    out.write('Blog')
    for word in master_word_list: out.write('\t%s' % word)
    out.write('\n')
    for blogurl in blog_wc:
        print blogurl
        out.write(blogurl)
        for word in master_word_list:
            if word in blog_wc[blogurl].keys(): 
                out.write('\t%d' % blog_wc[blogurl][word])
            else: 
                out.write('\t0')
        out.write('\n')
    out.close()    
    return

def getwords(html):
    """
    Return a list of words in the HTML text
    """
    # Remove all the HTML tags
    #txt=re.compile(r'<[^>]+>').sub('',html)
    
    # Split words by all non-alpha characters
    words=re.compile(r'[^A-Z^a-z]+').split(html)
    
    # Convert to lowercase
    return [word.lower() for word in words if word!='']

if __name__=="__main__":
    main()