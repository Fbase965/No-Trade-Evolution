import struct

def unpack_garc(data):
    magic, hdr_size, endian, ver, sec_count, data_offset, total_size, max_file = struct.unpack('<4sIHHIIII', data[:0x1C])
    assert magic == b'GARC' or magic == b'CRAG', f"Invalid magic: {magic}"
    
    # 1. FATO / OTAF
    fato_offset = hdr_size
    fato_magic, fato_size, fato_count, fato_pad = struct.unpack('<4sIHH', data[fato_offset:fato_offset+12])
    print(f'FATO count: {fato_count}')
    
    # 2. FATB / BTAF
    fatb_offset = fato_offset + fato_size
    fatb_magic, fatb_size, fatb_count = struct.unpack('<4sII', data[fatb_offset:fatb_offset+12])
    print(f'FATB count: {fatb_count}')
    
    fatb_entries = []
    for i in range(fatb_count):
        entry_offset = fatb_offset + 12 + i * 12
        start_off, end_off, length = struct.unpack('<III', data[entry_offset:entry_offset+12])
        fatb_entries.append((start_off, end_off, length))
    
    # 3. FIMG / BMIF
    fimg_offset = fatb_offset + fatb_size
    fimg_magic, fimg_size, data_len = struct.unpack('<4sII', data[fimg_offset:fimg_offset+12])
    data_start = fimg_offset + 12
    
    files = []
    for i, (start_off, end_off, length) in enumerate(fatb_entries):
        file_bytes = data[data_start + start_off : data_start + end_off]
        files.append(file_bytes)
    return files

with open("E:/Pokemon-XY-No-Trade-Mod/tools/inspect_garc.py", "r") as f:
    pass

import sys
from pyctr.type.romfs import RomFSReader
class SubIO:
    def __init__(self, fp, offset, size):
        self.fp = fp
        self.offset = offset
        self.size = size
        self.pos = 0
        self.closed = False
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
    garc7 = romfs.open('/a/0/1/7').read()

print("Unpacking /a/0/1/8 (Evolutions)...")
files8 = unpack_garc(garc8)
print(f"Extracted {len(files8)} files from /a/0/1/8. Sample file sizes: {[len(f) for f in files8[:5]]}")

print("Unpacking /a/0/1/7 (Personal Stats)...")
files7 = unpack_garc(garc7)
print(f"Extracted {len(files7)} files from /a/0/1/7. Sample file sizes: {[len(f) for f in files7[:5]]}")
