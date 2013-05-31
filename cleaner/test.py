import datetime
import os
import shutil
import unittest
import cleaner


class Test_common_func(unittest.TestCase):
    
    def setUp(self):
        self.today = datetime.date.today()
        self.path = r"c:\test"
        
    def test_get_dateList(self):
        day1 = self.today - datetime.timedelta(days=1)
        day2 = self.today - datetime.timedelta(days=2)
        self.assertEqual(cleaner.get_dateList(1,3),[day1, day2])
        
        
    def test_is_validDatePath(self):
        testPath = os.path.join(self.path, self.today.strftime("%Y.%m.%d"))
        testDates = [self.today]
        self.assertTrue(cleaner.is_validDatePath(testPath, testDates))
        
class Test_io_func(unittest.TestCase):
    
    def setUp(self):
        self.today = datetime.date.today()
        self.resource = r"C:\testresource"#there are some test data in it
        self.path = r"c:\test"
        self.tmpPath = os.path.join(self.path, "path")
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        shutil.copytree(self.resource, self.tmpPath)

    def tearDown(self):
        shutil.rmtree(os.path.join(self.path, "path"))

    def test_get_subfolderList(self):
        dateString1 = (self.today - datetime.timedelta(days=1)).strftime("%Y.%m.%d")
        dateString2 = (self.today - datetime.timedelta(days=2)).strftime("%Y.%m.%d")
        subFolder1 = os.path.join(self.tmpPath, dateString1)
        subFolder2 = os.path.join(self.tmpPath, dateString2)
        self.assertEqual(cleaner.get_subfolderList(self.tmpPath, 1, 3).sort(), [subFolder1, subFolder2].sort())
    
    def test_clean_path(self):
        testPath = os.path.join(self.tmpPath, "delpath")
        testFile = os.path.join(self.tmpPath, "delfile.txt")
        self.assertTrue(os.path.isdir(testPath))
        self.assertTrue(os.path.isfile(testFile))
        cleaner.clean_path(testPath)
        self.assertFalse(os.path.isdir(testPath))
        cleaner.clean_path(testFile)
        self.assertFalse(os.path.isdir(testFile))
    
if __name__ == "__main__":
    unittest.main()
