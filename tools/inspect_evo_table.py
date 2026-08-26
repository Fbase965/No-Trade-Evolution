import struct

with open("E:/Pokemon-XY-No-Trade-Mod/tools/find_exact_evo_garc.py") as f: pass
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

print(f"GARC /a/2/1/5 total size: {len(garc_evo)}")

hdr_size = struct.unpack('<I', garc_evo[4:8])[0]
fato_len = struct.unpack('<I', garc_evo[hdr_size+4:hdr_size+8])[0]
fatb_off = hdr_size + fato_len
fatb_len, fatb_entries = struct.unpack('<II', garc_evo[fatb_off+4:fatb_off+12])
fimg_off = fatb_off + fatb_len
data_start = fimg_off + 12

print(f"Total Pokemon entries in /a/2/1/5: {fatb_entries}")

# Let's inspect some key Pokemon:
# 1: Bulbasaur
# 2: Ivysaur
# 64: Kadabra
# 67: Machoke
# 75: Graveler
# 93: Haunter
# 123: Scyther
# 133: Eevee
species_names = {
    1: "Bulbasaur", 2: "Ivysaur", 64: "Kadabra", 67: "Machoke", 75: "Graveler",
    93: "Haunter", 95: "Onix", 123: "Scyther", 133: "Eevee", 137: "Porygon", 
    233: "Porygon2", 525: "Boldore", 533: "Gurdurr", 708: "Phantump", 710: "Pumpkaboo"
}

for sp_id, name in species_names.items():
    e_off = fatb_off + 12 + sp_id * 16
    flags, start, end, length = struct.unpack('<IIII', garc_evo[e_off:e_off+16])
    raw = garc_evo[data_start + start : data_start + end]
    print(f"\n[{sp_id}] {name} (bytes={len(raw)}):")
    # In Gen 6, each evolution entry is 6 or 8 bytes:
    # Let's check: each entry has: Method (u16), Param (u16), Target (u16)
    for s in range(0, len(raw), 6):
        if s + 6 <= len(raw):
            method, param, target = struct.unpack('<HHH', raw[s:s+6])
            if method != 0 or target != 0:
                print(f"   Slot {s//6 + 1}: Method={method}, Param={param}, TargetSpecies={target}")
