import struct
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

    all_paths = []
    def scan(p):
        info = romfs.get_info_from_path(p)
        for c in info.contents:
            subp = f"{p.rstrip('/')}/{c}"
            si = romfs.get_info_from_path(subp)
            if si.type == 'dir': scan(subp)
            else: all_paths.append((subp, si.size))
    scan('/')
    
    print(f"Total files in RomFS: {len(all_paths)}")
    
    # We look for a GARC with ~720+ entries or where Bulbasaur (1) -> Ivysaur (2) -> Venusaur (3)
    # or Kadabra (64) -> Alakazam (65)
    # In Gen 6, Bulbasaur evolves into Ivysaur at level 16: (Method 4: Level, Level 16, Target 2)
    # Ivysaur evolves into Venusaur at level 32: (Method 4: Level, Level 32, Target 3)
    # In bytes (little endian):
    # Method 4 (0x0004), Level 16 (0x0010), Target 2 (0x0002) -> 04 00 10 00 02 00
    # or Method 4 (0x0004), Level 32 (0x0020), Target 3 (0x0003) -> 04 00 20 00 03 00
    pattern1 = b'\x04\x00\x10\x00\x02\x00'
    pattern2 = b'\x04\x00\x20\x00\x03\x00'
    
    for path, size in all_paths:
        if size < 5000 or size > 5000000: continue
        try:
            d = romfs.open(path).read()
            if pattern1 in d and pattern2 in d:
                print(f"MATCH FOUND: {path} (size={size})")
        except Exception as e:
            pass
