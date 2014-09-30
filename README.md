RandomIO
===============

### Byte generator

Class that allows reading random bytes and piping those bytes to a file.

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

### File generator

Or generate a file with one line:

```python
file_name = RandomIO.RandomIO('seed string').genfile(100)
```
