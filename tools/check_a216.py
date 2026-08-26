import struct

with open("E:/Pokemon-XY-No-Trade-Mod/tools/list_a21.py", "r") as f:
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
    garc_evo = romfs.open('/a/2/1/6').read()

print(f"GARC /a/2/1/6 size: {len(garc_evo)}")
magic, hdr_size, endian, ver, sec_count, data_offset, total_size, max_file = struct.unpack('<4sIHHIIII', garc_evo[:0x1C])
print(f"Header: magic={magic}, hdr={hdr_size}, ver={hex(ver)}, data_offset={hex(data_offset)}, size={total_size}, max_file={max_file}")

fato_off = hdr_size
fato_magic, fato_len, fato_entries, fato_pad = struct.unpack('<4sIHH', garc_evo[fato_off:fato_off+12])
print(f"FATO: entries={fato_entries}")

fatb_off = fato_off + fato_len
fatb_magic, fatb_len, fatb_entries = struct.unpack('<4sII', garc_evo[fatb_off:fatb_off+12])
print(f"FATB: entries={fatb_entries}")

fimg_off = fatb_off + fatb_len
fimg_magic, fimg_len, data_len = struct.unpack('<4sII', garc_evo[fimg_off:fimg_off+12])
data_start = fimg_off + 12
print(f"FIMG: data_len={data_len}")

# Let's inspect entry sizes
# In GARCv4: each FATB entry has: flags (4 bytes), start (4 bytes), end (4 bytes), length (4 bytes) -> 16 bytes!
entries = []
for i in range(fatb_entries):
    e_off = fatb_off + 12 + i * 16
    flags, start, end, length = struct.unpack('<IIII', garc_evo[e_off:e_off+16])
    file_data = garc_evo[data_start + start : data_start + end]
    entries.append(file_data)

print(f"Successfully extracted {len(entries)} Pokemon evolution entries!")
print(f"Entry 1 (Bulbasaur, size={len(entries[1])}): {entries[1].hex(' ')}")
print(f"Entry 64 (Kadabra, size={len(entries[64])}): {entries[64].hex(' ')}")
print(f"Entry 93 (Haunter, size={len(entries[93])}): {entries[93].hex(' ')}")
print(f"Entry 123 (Scyther, size={len(entries[123])}): {entries[123].hex(' ')}")
print(f"Entry 133 (Eevee, size={len(entries[133])}): {entries[133].hex(' ')}")
