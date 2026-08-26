import os
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

def build_mod():
    rom_path = r'D:\Pokemon Y (Europe) (EnJaFrDeEsItKo)\Pokemon Y (Europe) (En,Ja,Fr,De,Es,It,Ko).3ds'
    print(f"Reading original ROM: {rom_path}")
    
    with open(rom_path, 'rb') as f:
        f.seek(0x4000 + 0x1B0)
        romfs_offset_units, romfs_size_units = struct.unpack('<II', f.read(8))
        romfs_offset = 0x4000 + romfs_offset_units * 0x200
        romfs_size = romfs_size_units * 0x200
        sub = SubIO(f, romfs_offset, romfs_size)
        romfs = RomFSReader(sub, case_insensitive=True)
        garc_evo = bytearray(romfs.open('/a/2/1/5').read())

    hdr_size = struct.unpack('<I', garc_evo[4:8])[0]
    fato_len = struct.unpack('<I', garc_evo[hdr_size+4:hdr_size+8])[0]
    fatb_off = hdr_size + fato_len
    fatb_len, fatb_entries = struct.unpack('<II', garc_evo[fatb_off+4:fatb_off+12])
    fimg_off = fatb_off + fatb_len
    data_start = fimg_off + 12

    print(f"Patching evolution data for {fatb_entries} entries...")
    
    patched_count = 0
    # Evolution levels for pure trade evolutions
    level_map = {
        64: 37,  # Kadabra -> Alakazam
        67: 37,  # Machoke -> Machamp
        75: 37,  # Graveler -> Golem
        93: 37,  # Haunter -> Gengar
        525: 38, # Boldore -> Gigalith
        533: 38, # Gurdurr -> Conkeldurr
        588: 35, # Karrablast -> Escavalier
        616: 35, # Shelmet -> Accelgor
        708: 35, # Phantump -> Trevenant
        710: 35, # Pumpkaboo -> Gourgeist (Average)
        788: 35, # Pumpkaboo (Small)
        789: 35, # Pumpkaboo (Large)
        790: 35, # Pumpkaboo (Super)
    }

    for sp_id in range(fatb_entries):
        e_off = fatb_off + 12 + sp_id * 16
        flags, start, end, length = struct.unpack('<IIII', garc_evo[e_off:e_off+16])
        entry_start = data_start + start
        
        for s in range(0, length, 6):
            if s + 6 <= length:
                slot_off = entry_start + s
                method, param, target = struct.unpack('<HHH', garc_evo[slot_off:slot_off+6])
                
                # Case 1: Pure Trade (Method 5) or Karrablast/Shelmet trade (Method 7)
                if method in [5, 7]:
                    lvl = level_map.get(sp_id, 37)
                    # Method 4 = Level Up
                    struct.pack_into('<HHH', garc_evo, slot_off, 4, lvl, target)
                    print(f"  [Species {sp_id:03d}] Changed to Level {lvl} -> Target {target}")
                    patched_count += 1
                
                # Case 2: Trade holding Item (Method 6)
                elif method == 6:
                    # Method 8 = Use Item directly (like Evolution Stone)
                    struct.pack_into('<HHH', garc_evo, slot_off, 8, param, target)
                    print(f"  [Species {sp_id:03d}] Changed to Use Item ID {param} -> Target {target}")
                    patched_count += 1

    print(f"\nSuccessfully patched {patched_count} evolution methods!")
    
    # Save the modified GARC to all destination folders
    dest_dirs = [
        r"E:\Pokemon-XY-No-Trade-Mod\Mod-Package\3DS_Luma3DS\luma\titles\0004000000055D00\romfs\a\2\1", # Pokemon X 3DS
        r"E:\Pokemon-XY-No-Trade-Mod\Mod-Package\3DS_Luma3DS\luma\titles\0004000000055E00\romfs\a\2\1", # Pokemon Y 3DS
        r"E:\Pokemon-XY-No-Trade-Mod\Mod-Package\Citra_Lime3DS\Pokemon_X\romfs\a\2\1",                    # Pokemon X Citra
        r"E:\Pokemon-XY-No-Trade-Mod\Mod-Package\Citra_Lime3DS\Pokemon_Y\romfs\a\2\1",                    # Pokemon Y Citra
    ]
    
    for d in dest_dirs:
        os.makedirs(d, exist_ok=True)
        file_path = os.path.join(d, "5")
        with open(file_path, "wb") as out:
            out.write(garc_evo)
        print(f"Saved: {file_path} ({len(garc_evo)} bytes)")

if __name__ == "__main__":
    build_mod()
