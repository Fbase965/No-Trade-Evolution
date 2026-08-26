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
            else: all_paths.append(subp)
    scan('/')
    
    print(f"Scanning {len(all_paths)} files for evolution data...")
    # Eevee evolves to Vaporeon (134 = 0x0086), Jolteon (135 = 0x0087), Flareon (136 = 0x0088)
    # Kadabra (64) evolves to Alakazam (65 = 0x0041)
    # Haunter (93) evolves to Gengar (94 = 0x005E)
    # Machoke (67) evolves to Machamp (68 = 0x0044)
    target_pattern = b'\x41\x00' # 65
    
    for path in all_paths:
        try:
            info = romfs.get_info_from_path(path)
            if info.size < 1000 or info.size > 2000000: # Evolutions table is usually 50KB-1MB
                continue
            data = romfs.open(path).read()
            if b'CRAG' in data[:4]:
                # Check if this GARC contains evolution entries (like 8 entries of 6 or 8 bytes)
                # In Gen 6, Kadabra evolves into Alakazam (method 5: Trade, param 0, target 65)
                # (5, 0, 65) or (65, 5, 0)
                # Trade methods in XY: 5 (Trade), 6 (Trade holding item), 7 (Trade for Shelmet/Karrablast)
                if b'\x05\x00\x00\x00\x41\x00' in data or b'\x05\x00\x41\x00' in data or (b'\x41\x00' in data and b'\x5e\x00' in data and b'\x44\x00' in data and b'\x4c\x00' in data):
                    print(f"Candidate file found: {path} (size={info.size})")
        except Exception as e:
            pass
