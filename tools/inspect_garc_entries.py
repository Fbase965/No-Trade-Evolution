import struct

with open("E:/Pokemon-XY-No-Trade-Mod/tools/test_garc_unpack.py", "r") as f:
    pass

import sys
from pyctr.type.romfs import RomFSReader
class SubIO:
    def __init__(self, fp, offset, size):
        self.fp = fp; self.offset = offset; self.size = size; self.pos = 0; self.closed = False
    def seek(self, pos, whence=0):
        if whence == 0: self.pos = pos
        elif whence == 1: self.pos += pos
        elif whence == 2: self.pos = self.size + pos
        return self.pos
    def tell(self): return self.pos
    def read(self, n=-1):
        if n < 0 or self.pos + n > self.size: n = self.size - self.pos
        if n <= 0: return b''
        self.fp.seek(self.offset + self.pos)
        d = self.fp.read(n)
        self.pos += len(d)
        return d
    def close(self): self.closed = True

with open(r'D:\Pokemon Y (Europe) (EnJaFrDeEsItKo)\Pokemon Y (Europe) (En,Ja,Fr,De,Es,It,Ko).3ds', 'rb') as f:
    f.seek(0x4000 + 0x1B0)
    romfs_offset_units, romfs_size_units = struct.unpack('<II', f.read(8))
    romfs_offset = 0x4000 + romfs_offset_units * 0x200
    romfs_size = romfs_size_units * 0x200
    sub = SubIO(f, romfs_offset, romfs_size)
    romfs = RomFSReader(sub, case_insensitive=True)
    garc8 = romfs.open('/a/0/1/8').read()

print("GARC8 first 128 bytes:")
print(garc8[:128].hex(' '))

# Let's inspect FATO and FATB in detail
fato_off = 0x1C
fato_magic, fato_len, fato_entries, fato_pad = struct.unpack('<4sIHH', garc8[fato_off:fato_off+12])
print(f"FATO: magic={fato_magic}, len={fato_len}, entries={fato_entries}")
fato_offsets = [struct.unpack('<I', garc8[fato_off+12+i*4:fato_off+16+i*4])[0] for i in range(fato_entries)]
print(f"FATO offsets: {fato_offsets}")

fatb_off = fato_off + fato_len
fatb_magic, fatb_len, fatb_entries = struct.unpack('<4sII', garc8[fatb_off:fatb_off+12])
print(f"FATB: magic={fatb_magic}, len={fatb_len}, entries={fatb_entries}")
for i in range(fatb_entries):
    e_off = fatb_off + 12 + i * 16 # let's check if entry is 12 or 16 bytes
    vals = struct.unpack('<4I', garc8[e_off:e_off+16])
    print(f"FATB[{i}]: {vals}")
