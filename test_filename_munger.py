import filename_munger as fm
import unittest
import urllib2

class test_filename_munger(unittest.TestCase):
    
    def test_munge(self):
        fn = "t\\h!s is.a?bad file'n|ame"
        self.assertEquals(fm.munge(fn),"t_h_s_is_a_bad_file_n_ame")


if __name__=="__main__":
    unittest.main()