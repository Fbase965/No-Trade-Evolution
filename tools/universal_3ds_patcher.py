import os
import sys
import struct
from pyctr.type.romfs import RomFSReader

# Game Definitions for Nintendo 3DS
GAMES = {
    # Gen 6: XY
    "0004000000055D00": {"name": "Pokemon X", "folder": "Pokemon_X", "evo_path": "/a/2/1/5", "gen": 6},
    "0004000000055E00": {"name": "Pokemon Y", "folder": "Pokemon_Y", "evo_path": "/a/2/1/5", "gen": 6},
    # Gen 6: ORAS
    "000400000011C400": {"name": "Pokemon Omega Ruby", "folder": "Pokemon_Omega_Ruby", "evo_path": "/a/1/9/5", "gen": 6},
    "000400000011C500": {"name": "Pokemon Alpha Sapphire", "folder": "Pokemon_Alpha_Sapphire", "evo_path": "/a/1/9/5", "gen": 6},
    # Gen 7: Sun / Moon
    "0004000000164800": {"name": "Pokemon Sun", "folder": "Pokemon_Sun", "evo_path": "/a/0/1/8", "gen": 7},
    "0004000000175E00": {"name": "Pokemon Moon", "folder": "Pokemon_Moon", "evo_path": "/a/0/1/8", "gen": 7},
    # Gen 7: Ultra Sun / Ultra Moon
    "00040000001B5000": {"name": "Pokemon Ultra Sun", "folder": "Pokemon_Ultra_Sun", "evo_path": "/a/0/1/8", "gen": 7},
    "00040000001B5100": {"name": "Pokemon Ultra Moon", "folder": "Pokemon_Ultra_Moon", "evo_path": "/a/0/1/8", "gen": 7},
}

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

def patch_evolution_garc(garc_bytes):
    garc = bytearray(garc_bytes)
    hdr_size = struct.unpack('<I', garc[4:8])[0]
    fato_len = struct.unpack('<I', garc[hdr_size+4:hdr_size+8])[0]
    fatb_off = hdr_size + fato_len
    fatb_len, fatb_entries = struct.unpack('<II', garc[fatb_off+4:fatb_off+12])
    fimg_off = fatb_off + fatb_len
    data_start = fimg_off + 12

    level_map = {
        64: 37,  # Kadabra -> Alakazam
        67: 37,  # Machoke -> Machamp
        75: 37,  # Graveler -> Golem (also Alolan Graveler)
        93: 37,  # Haunter -> Gengar
        525: 38, # Boldore -> Gigalith
        533: 38, # Gurdurr -> Conkeldurr
        588: 35, # Karrablast -> Escavalier
        616: 35, # Shelmet -> Accelgor
        708: 35, # Phantump -> Trevenant
        710: 35, # Pumpkaboo -> Gourgeist
        788: 35, # Pumpkaboo (Small)
        789: 35, # Pumpkaboo (Large)
        790: 35, # Pumpkaboo (Super)
    }

    count = 0
    for sp_id in range(fatb_entries):
        e_off = fatb_off + 12 + sp_id * 16
        flags, start, end, length = struct.unpack('<IIII', garc[e_off:e_off+16])
        entry_start = data_start + start
        
        for s in range(0, length, 6):
            if s + 6 <= length:
                slot_off = entry_start + s
                method, param, target = struct.unpack('<HHH', garc[slot_off:slot_off+6])
                
                # Pure Trade / Mutual Trade
                if method in [5, 7]:
                    lvl = level_map.get(sp_id, 37)
                    struct.pack_into('<HHH', garc, slot_off, 4, lvl, target) # Method 4 = Level Up
                    count += 1
                # Trade with item
                elif method == 6:
                    struct.pack_into('<HHH', garc, slot_off, 8, param, target) # Method 8 = Use Item
                    count += 1
    return bytes(garc), count

def patch_rom(rom_path, base_output_dir=r"E:\Pokemon-XY-No-Trade-Mod\Mod-Package"):
    print(f"\n=======================================================")
    print(f"Loading ROM: {rom_path}")
    
    with open(rom_path, 'rb') as f:
        f.seek(0x100)
        ncsd_magic = f.read(4)
        
        # Partition 0 offset
        part0_offset = 0x4000
        if ncsd_magic != b'NCSD':
            f.seek(0x100)
            if f.read(4) == b'NCCH':
                part0_offset = 0
            else:
                print("Error: Not a valid 3DS or NCCH file!")
                return
        
        # Read Title ID
        f.seek(part0_offset + 0x108)
        title_id_int = struct.unpack('<Q', f.read(8))[0]
        title_id_str = f"{title_id_int:016X}"
        
        # Read RomFS offset & size
        f.seek(part0_offset + 0x1B0)
        romfs_offset_units, romfs_size_units = struct.unpack('<II', f.read(8))
        romfs_offset = part0_offset + romfs_offset_units * 0x200
        romfs_size = romfs_size_units * 0x200
        
        sub = SubIO(f, romfs_offset, romfs_size)
        romfs = RomFSReader(sub, case_insensitive=True)
        
        game_info = GAMES.get(title_id_str)
        if not game_info:
            print(f"Unknown Game Title ID: {title_id_str}")
            # Try to auto-detect evo path
            for test_path in ["/a/2/1/5", "/a/1/9/5", "/a/0/1/8"]:
                try:
                    if test_path in romfs:
                        print(f"Detected evolution path: {test_path}")
                        break
                except: pass
            return

        print(f"Game Identified: {game_info['name']} (Title ID: {title_id_str})")
        evo_path = game_info['evo_path']
        
        # Verify if path exists or search fallback
        target_path = evo_path
        try:
            raw_garc = romfs.open(target_path).read()
        except Exception:
            # Fallback search
            for candidate in ["/a/2/1/5", "/a/1/9/5", "/a/0/1/8"]:
                try:
                    raw_garc = romfs.open(candidate).read()
                    target_path = candidate
                    print(f"Found evolution table at fallback: {target_path}")
                    break
                except: pass

        print(f"Extracting {target_path} (size: {len(raw_garc)} bytes)...")
        patched_garc, patched_count = patch_evolution_garc(raw_garc)
        print(f"Successfully patched {patched_count} evolution methods!")
        
        # Output locations
        luma_dir = os.path.join(base_output_dir, "3DS_Luma3DS", "luma", "titles", title_id_str, "romfs", target_path.lstrip('/').replace('/', os.sep))
        luma_parent = os.path.dirname(luma_dir)
        os.makedirs(luma_parent, exist_ok=True)
        with open(luma_dir, "wb") as out_f:
            out_f.write(patched_garc)
            
        citra_dir = os.path.join(base_output_dir, "Citra_Lime3DS", game_info['folder'], "romfs", target_path.lstrip('/').replace('/', os.sep))
        citra_parent = os.path.dirname(citra_dir)
        os.makedirs(citra_parent, exist_ok=True)
        with open(citra_dir, "wb") as out_f:
            out_f.write(patched_garc)

        print(f"[OK] Generated Luma3DS Mod: {luma_dir}")
        print(f"[OK] Generated Citra/Azahar Mod: {citra_dir}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        patch_rom(sys.argv[1])
    else:
        # Default test with Pokemon Y
        patch_rom(r'D:\Pokemon Y (Europe) (EnJaFrDeEsItKo)\Pokemon Y (Europe) (En,Ja,Fr,De,Es,It,Ko).3ds')
