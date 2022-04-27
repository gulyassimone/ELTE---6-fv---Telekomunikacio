import zlib

txt = "hello"
with open('123456', 'w') as f:
    f.write(hex(zlib.crc32((txt).encode('UTF-8')) % (1 << 32)))
