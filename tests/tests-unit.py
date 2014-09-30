#
# The MIT License (MIT)
#
# Copyright (c) 2014 William T. James
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
import os

import RandomIO

class TestRandomIO(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gen(self):
        s = RandomIO.RandomIO()
        b = s.read(100)
        
        self.assertEqual(len(b),100)
        
        self.assertEqual(RandomIO.RandomIO(123456).read(100),RandomIO.RandomIO(123456).read(100))
        self.assertEqual(RandomIO.RandomIO(b'byte string seed').read(100),RandomIO.RandomIO(b'byte string seed').read(100))
        self.assertEqual(RandomIO.RandomIO(1.23456).read(100),RandomIO.RandomIO(1.23456).read(100))
        
    def test_consistent(self):
        s1 = RandomIO.RandomIO('seed string')
        s2 = RandomIO.RandomIO('seed string')
        s3 = RandomIO.RandomIO('seed string')
        s4 = RandomIO.RandomIO('another seed')
        
        self.assertEqual(s1.read(100),s2.read(100))
        self.assertNotEqual(s3.read(100),s4.read(100))
        
    def test_crossplatform(self):
        string_seed1 = b'\t\xb0\xef\xd9\x05p\xe1W\x17\x8a9\xc6!;^6\x1d\xadj\
\xb4#n\x1d/\x12+\xe6\xb1\x80\xc86\x06I\xc4!\x8b39\x84E\x1d\x14\xdf\x14e\x12\
\xfa\xf0\r\x1b'

        s = RandomIO.RandomIO('seed1').read(50)

        self.assertEqual(s,string_seed1)
        
        string_123456 = b'\x18\xb2\xce\x8a \xc9\xe2n\xd9\xf6\x06\x0b8\xf9\xb9\
\xf8\x9b#81z\xf8\x02\x83\x1e\xa2\xf02\x7f\xad\xd7*h\xad9\xf6\x14U\xca\x90\\i\
\xcc~#h\xaa\xb4\x1b['

        s = RandomIO.RandomIO(123456).read(50)
        
        self.assertEqual(s,string_123456)
        
    def test_read(self):
        s1 = RandomIO.RandomIO('seed string')
        
        with self.assertRaises(RuntimeError) as ex:
            s1.read()
            
        self.assertEqual(str(ex.exception),'Size must be greater than zero')
        
    def test_dump(self):
        s1 = RandomIO.RandomIO('seed string')
        s2 = RandomIO.RandomIO('seed string')
    
        file1 = 'file1'
        file2 = 'file2'
        
        with open(file1,'wb') as f:
            s1.dump(100,f)
        
        with open(file2,'wb') as f:
            s2.dump(100,f)
        
        with open(file1,'rb') as f:
            contents1 = f.read()
        
        with open(file2,'rb') as f:
            contents2 = f.read()
            
        self.assertEqual(len(contents1),100)
        self.assertEqual(contents1,contents2)
        
        os.remove(file1)
        os.remove(file2)

    def test_genfile(self):
        path = RandomIO.RandomIO('seed string').genfile(100)
        
        with open(path,'rb') as f:
            contents = f.read()
        
        self.assertEqual(len(contents),100)
        
        os.remove(path)
        
        dir = 'test_directory/'
        
        os.mkdir(dir)
        path = RandomIO.RandomIO('seed string').genfile(100,dir)
        
        (h1,t1) = os.path.split(dir)
        (h2,t2) = os.path.split(path)
        self.assertEqual(h1,h2)
        
        with open(path,'rb') as f:
            contents = f.read()
            
        self.assertEqual(len(contents),100)
        
        os.remove(path)
        os.rmdir(dir)
        
        
    def test_large(self):
        length = 100000000
        file1 = RandomIO.RandomIO('seed string').genfile(length)
        file2 = RandomIO.RandomIO('seed string').genfile(length)
        
        with open(file1,'rb') as f1:
            with open(file1,'rb') as f2:
                for c in iter(lambda:f1.read(1000),b''):
                    self.assertEqual(c,f2.read(1000))
                    
        os.remove(file1)
        os.remove(file2)
        
        
if __name__ == '__main__':
    unittest.main()