import struct
with open("E:/Pokemon-XY-No-Trade-Mod/tools/inspect_evo_table.py") as f: pass
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
    garc_evo = romfs.open('/a/2/1/5').read()

hdr_size = struct.unpack('<I', garc_evo[4:8])[0]
fato_len = struct.unpack('<I', garc_evo[hdr_size+4:hdr_size+8])[0]
fatb_off = hdr_size + fato_len
fatb_len, fatb_entries = struct.unpack('<II', garc_evo[fatb_off+4:fatb_off+12])
fimg_off = fatb_off + fatb_len
data_start = fimg_off + 12

print("=== ALL TRADE EVOLUTIONS IN POKEMON XY ===")
for sp_id in range(fatb_entries):
    e_off = fatb_off + 12 + sp_id * 16
    flags, start, end, length = struct.unpack('<IIII', garc_evo[e_off:e_off+16])
    raw = garc_evo[data_start + start : data_start + end]
    for s in range(0, len(raw), 6):
        if s + 6 <= len(raw):
            method, param, target = struct.unpack('<HHH', raw[s:s+6])
            if method in [5, 6, 7]:
                print(f"Species {sp_id} (Slot {s//6 + 1}): Method={method}, Param={param}, Target={target}")
