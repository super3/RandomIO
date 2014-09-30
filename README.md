RandomIO
===============

[![Build Status](https://travis-ci.org/wiggzz/RandomIO.svg)](https://travis-ci.org/wiggzz/RandomIO) [![Coverage Status](https://img.shields.io/coveralls/wiggzz/RandomIO.svg)](https://coveralls.io/r/wiggzz/RandomIO?branch=master)

`RandomIO` provides a readable interface for cryptographic quality random bytes.  It also allows generation of random files, dumping random bytes to files, and a `.read()` method for reading bytes.

### File generation

Generate a 100 byte file from a seed with one line:

```python
import RandomIO

path = RandomIO.RandomIO('seed string').genfile(50)
with open(path,'rb') as f:
	print(f.read())

# b"\x0b\x04\x1f\xb9I\x18Y\xc8\\\xe5,\xfc\x94\xd6\xf5(\xcb\xd9k\xb3M>\xe9\xc8R
#   \xa1\xb2\xdc\xba\\g\x0f3\xbcR\x93\xedeZ;\xfc\xa1\xfb\x85%\x8e'\xbb\x0b\xc2"
```

It is possible to specify the directory to generate the file in, or the file name

```python
# specify a directory:

path = RandomIO.RandomIO('seed string').genfile(100,'dir/')
print(path)

# 'dir/22aae6183b5202cd0c74381c673394d2'

# or file name:

path = RandomIO.RandomIO('seed string').genfile(100,'dir/file')
print(path)

# 'dir/file'
```

### Byte generation

Also allows reading random bytes and dumping those bytes to a file object.

```python
import RandomIO

s = RandomIO.RandomIO()
print(s.read(100))

# b'\x8bfT\x9c\x06_)\xa2,\xd0'

# or generate seeded random bytes
s = RandomIO.RandomIO('seed string')
print(s.read(100))

# b'\xc7\x15\xce7n\xaa\x8ca]u'

# dump the bytes into a file object
s = RandomIO.RandomIO('seed string')
with open('path/to/file','wb') as f:
	s.dump(10,f)

with open('path/to/file','rb') as f:
	print(f.read())
	
# b'\xc7\x15\xce7n\xaa\x8ca]u'
```


