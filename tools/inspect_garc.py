import struct
from pyctr.type.romfs import RomFSReader

class SubIO:
    def __init__(self, fp, offset, size):
        self.fp = fp
        self.offset = offset
        self.size = size
        self.pos = 0
        self.closed = False
    def seek(self, pos, whence=0):
        if whence == 0:
            self.pos = pos
        elif whence == 1:
            self.pos += pos
        elif whence == 2:
            self.pos = self.size + pos
        return self.pos
    def tell(self):
        return self.pos
    def read(self, n=-1):
        if n < 0 or self.pos + n > self.size:
            n = self.size - self.pos
        if n <= 0:
            return b''
        self.fp.seek(self.offset + self.pos)
        data = self.fp.read(n)
        self.pos += len(data)
        return data
    def close(self):
        self.closed = True

with open(r'D:\Pokemon Y (Europe) (EnJaFrDeEsItKo)\Pokemon Y (Europe) (En,Ja,Fr,De,Es,It,Ko).3ds', 'rb') as f:
    f.seek(0x4000 + 0x1B0)
    romfs_offset_units, romfs_size_units = struct.unpack('<II', f.read(8))
    romfs_offset = 0x4000 + romfs_offset_units * 0x200
    romfs_size = romfs_size_units * 0x200
    sub = SubIO(f, romfs_offset, romfs_size)
    romfs = RomFSReader(sub, case_insensitive=True)
    garc = romfs.open('/a/0/1/8').read()

magic, hdr_size, endian, ver, sec_count, data_offset, file_size, max_size = struct.unpack('<4sIHHIIII', garc[:0x1C])
print(f'GARC: magic={magic}, hdr={hdr_size}, ver={hex(ver)}, sec_count={sec_count}, data_offset={hex(data_offset)}, size={file_size}, max_file={max_size}')

pos = hdr_size
while pos < len(garc):
    sec_magic, sec_size = struct.unpack('<4sI', garc[pos:pos+8])
    print(f'Section at {hex(pos)}: {sec_magic}, size={sec_size} ({hex(sec_size)})')
    if sec_magic == b'FATA' or sec_magic == b'BTAF':
        file_count, = struct.unpack('<I', garc[pos+8:pos+12])
        print(f'  File count: {file_count}')
    pos += sec_size
