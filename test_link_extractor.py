import link_extractor as le
import unittest
import urllib2

class test_link_extractor(unittest.TestCase):
    
    def test_link1(self):
        test_text = "<a href='http://www.example.com'>Example</a>"
        link_dict = le.extract_links(test_text)
        self.assertEquals(link_dict,{'http://www.example.com':1})
        
        # note dependency on test_text above
        test_text2 = test_text + test_text
        link_dict = le.extract_links(test_text2)
        self.assertEquals(link_dict,{'http://www.example.com':2})
    
    def test_feed_link(self):
        blog_url = "http://realizationsinbiostatistics.blogspot.com"
        blog_text = urllib2.urlopen(blog_url).read()
        feed_url = le.extract_feed_link(blog_text)
        self.assertEquals(feed_url,"http://realizationsinbiostatistics.blogspot.com/feeds/posts/default")
        
    def test_feed_link_from_url(self):
        blog_url = "http://realizationsinbiostatistics.blogspot.com"
        feed_url = le.extract_feed_link_from_url(blog_url)
        self.assertEquals(feed_url,"http://realizationsinbiostatistics.blogspot.com/feeds/posts/default")        
        
    def test_extract_links_from_list(self):
        blog_list = ["http://www.example.com","http://www.foo.com/sub"]
        text_to_do = '<a href="http://www.notinit.com">a</a> boo <a href="http://www.foo.com/sub">here i am</a> blah <a href="http://www.foo.com/sub">asdf</a> basdg <a href="http://www.example.com">example</a>'
        expected = {'http://www.example.com':1,"http://www.foo.com/sub":2}
        actual=le.extract_links_from_list(text_to_do,blog_list)
        self.assertEquals(actual,expected)    

    def test_extract_links_from_url(self):
        blog_url = "http://realizationsinbiostatistics.blogspot.com"
        bloglist = ['http://learnbayes.blogspot.com','http://www.johndcook.com/blog','http://www.notinthere.com']
        blogroll = le.extract_links_from_url(blog_url,bloglist)
        self.assertEquals(blogroll,bloglist[0:2])
    
    def text_extract_title_from_text(self):
        blog_text = "<html><head><title>Foo</title></head><body>bar</body></html>"
        self.assertEquals(le.extract_title_from_text(blog_text,"Foo"))

    def test_extract_title_from_url(self):
        blog_url = "http://realizationsinbiostatistics.blogspot.com"
        self.assertEquals(le.extract_title_from_url(blog_url),"Realizations in Biostatistics")    
        
if __name__=="__main__":
    unittest.main()