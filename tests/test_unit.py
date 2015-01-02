#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2014 William T. James for Storj Labs
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
import redis
import hashlib
import subprocess
import binascii

import RandomIO
from sys import platform as _platform

if _platform.startswith('linux') or _platform == 'darwin':
    cat_cmd = 'cat'
    iotools_call = ['IOTools.py']
elif _platform == 'win32':
    cat_cmd = 'type'
    iotools_call = ['python', os.path.join('bin', 'IOTools.py')]


class TestRandomIO(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gen(self):
        s = RandomIO.RandomIO()
        b = s.read(100)

        self.assertEqual(len(b), 100)

        self.assertEqual(
            RandomIO.RandomIO(123456).read(100),
            RandomIO.RandomIO(123456).read(100))
        self.assertEqual(RandomIO.RandomIO(b'byte string seed').read(
            100), RandomIO.RandomIO(b'byte string seed').read(100))
        self.assertEqual(RandomIO.RandomIO(1.23456).read(
            100), RandomIO.RandomIO(1.23456).read(100))

    def test_consistent(self):
        s1 = RandomIO.RandomIO('seed string')
        s2 = RandomIO.RandomIO('seed string')
        s3 = RandomIO.RandomIO('seed string')
        s4 = RandomIO.RandomIO('another seed')

        self.assertEqual(s1.read(100), s2.read(100))
        self.assertNotEqual(s3.read(100), s4.read(100))

    def test_crossplatform(self):
        string_seed1 = b'\t\xb0\xef\xd9\x05p\xe1W\x17\x8a9\xc6!;^6\x1d\xadj\
\xb4#n\x1d/\x12+\xe6\xb1\x80\xc86\x06I\xc4!\x8b39\x84E\x1d\x14\xdf\x14e\x12\
\xfa\xf0\r\x1b'

        s = RandomIO.RandomIO('seed1').read(50)

        self.assertEqual(s, string_seed1)

        string_123456 = b'\x18\xb2\xce\x8a \xc9\xe2n\xd9\xf6\x06\x0b8\xf9\xb9\
\xf8\x9b#81z\xf8\x02\x83\x1e\xa2\xf02\x7f\xad\xd7*h\xad9\xf6\x14U\xca\x90\\i\
\xcc~#h\xaa\xb4\x1b['

        s = RandomIO.RandomIO(123456).read(50)

        self.assertEqual(s, string_123456)

    def test_read(self):
        s1 = RandomIO.RandomIO('seed string')

        with self.assertRaises(RuntimeError) as ex:
            s1.read()

        self.assertEqual(
            str(ex.exception),
            'Stream size must be specified if bytes to read is not.')

    def test_dump(self):
        s1 = RandomIO.RandomIO('seed string')
        s2 = RandomIO.RandomIO('seed string')

        file1 = 'file1'
        file2 = 'file2'

        with open(file1, 'wb') as f:
            s1.dump(f, 100)

        with open(file2, 'wb') as f:
            s2.dump(f, 100)

        with open(file1, 'rb') as f:
            contents1 = f.read()

        with open(file2, 'rb') as f:
            contents2 = f.read()

        self.assertEqual(len(contents1), 100)
        self.assertEqual(contents1, contents2)

        os.remove(file1)
        os.remove(file2)

    def test_genfile(self):
        path = RandomIO.RandomIO('seed string').genfile(100)

        with open(path, 'rb') as f:
            contents = f.read()

        self.assertEqual(len(contents), 100)

        os.remove(path)

        dir = 'test_directory/'

        os.mkdir(dir)
        path = RandomIO.RandomIO('seed string').genfile(100, dir)

        (h1, t1) = os.path.split(dir)
        (h2, t2) = os.path.split(path)
        self.assertEqual(h1, h2)

        with open(path, 'rb') as f:
            contents = f.read()

        self.assertEqual(len(contents), 100)

        os.remove(path)
        os.rmdir(dir)

    def test_large(self):
        length = 100000000
        file1 = RandomIO.RandomIO('seed string').genfile(length)
        file2 = RandomIO.RandomIO('seed string').genfile(length)

        with open(file1, 'rb') as f1:
            with open(file1, 'rb') as f2:
                for c in iter(lambda: f1.read(1000), b''):
                    self.assertEqual(c, f2.read(1000))

        os.remove(file1)
        os.remove(file2)

    def test_read_limit(self):
        s1 = RandomIO.RandomIO('seed string', 100)

        s1.seek(90)

        buf1 = s1.read(100)

        self.assertEqual(len(buf1), 10)

    def test_read_zero(self):
        s1 = RandomIO.RandomIO('seed string')

        b = s1.read(0)

        self.assertEqual(len(b), 0)

    def test_seek_beginning(self):
        s1 = RandomIO.RandomIO('seed string')

        buf1 = s1.read(10)

        s1.seek(0)

        buf2 = s1.read(10)

        self.assertEqual(buf1, buf2)

    def test_seek_middle(self):
        s1 = RandomIO.RandomIO('seed string')

        s1.seek(10000)

        buf1 = s1.read(10)

        s1.seek(-10, os.SEEK_CUR)

        buf2 = s1.read(10)

        self.assertEqual(buf1, buf2)

    def test_seek_end(self):
        s1 = RandomIO.RandomIO('seed string', 1000)

        s1.seek(900)

        buf1 = s1.read(10)

        s1.seek(100, os.SEEK_END)

        buf2 = s1.read(10)

        self.assertEqual(buf1, buf2)

    def test_tell_beginning(self):
        s1 = RandomIO.RandomIO('seed string')

        s1.read(100)

        p = s1.tell()

        self.assertEqual(p, 100)

    def test_tell_seek_parity(self):
        s1 = RandomIO.RandomIO('seed string')

        s1.seek(100)

        p = s1.tell()

        self.assertEqual(p, 100)

    def test_seek_end_not_possible(self):
        s1 = RandomIO.RandomIO('seed string')

        with self.assertRaises(RuntimeError) as ex:
            s1.seek(100, os.SEEK_END)

        self.assertEqual(
            str(ex.exception),
            'Cannot seek from end of stream if size is unknown.')

    def test_iotools_txt(self):
        output = 'txt_test.out'
        size = 10485760
        subprocess.call(
            iotools_call + ['pairgen', str(size),
                            '-p', '10', '-o', output])

        with open(output, 'r') as pairsfile:
            for line in pairsfile:
                (hexseed, hash) = line.rstrip().split(' ')
                seed = binascii.unhexlify(hexseed)
                testhash = hashlib.sha256(
                    RandomIO.RandomIO(seed).read(size)).hexdigest()
                self.assertEqual(hash, testhash)
        os.remove(output)

    def test_iotools_redis(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        output = 'redis_test.out'
        size = 10485760

        subprocess.call(
            iotools_call + ['pairgen', str(size), '-p', '10', '-o', output,
                            '--redis'])
        subprocess.call(
            '{0} {1} | redis-cli --pipe'.format(cat_cmd, output), shell=True)

        for hexseed in r.scan_iter():
            seed = binascii.unhexlify(hexseed)
            testhash = hashlib.sha256(
                RandomIO.RandomIO(seed).read(size)).hexdigest()
            self.assertEqual(r.get(hexseed).decode('ascii'), testhash)
        os.remove(output)
        r.flushall()

if __name__ == '__main__':
    unittest.main()
