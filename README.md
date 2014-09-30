RandomIO
===============

### Byte generator

Class that allows reading random bytes and piping those bytes to a file.

```python
import RandomIO

s = RandomIO.RandomIO()
print s.read(100)

# "b'xxx'"

# or generate seeded random bytes
s = RandomIO.RandomIO('seed string')
print s.read(100)

# "b'xxx'"

# pipe the bytes into a file
s = RandomIO.RandomIO('seed')
s.pipe(100,'path/to/file')
```
