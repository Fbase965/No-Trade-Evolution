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

    # Let's list all files in RomFS to inspect the a/0/... structure
    print("Searching RomFS files...")
    all_files = []
    # To list files in RomFSReader, let's explore directories
    def scan_dir(path):
        info = romfs.get_info_from_path(path)
        # Check subdirectories
        for d in info.contents:
            subpath = f"{path.rstrip('/')}/{d}"
            try:
                subinfo = romfs.get_info_from_path(subpath)
                if subinfo.type == 'dir':
                    scan_dir(subpath)
                else:
                    all_files.append((subpath, subinfo.size))
            except Exception as e:
                pass
    scan_dir('/')
    print(f"Total files found in RomFS: {len(all_files)}")
    a0_files = [f for f in all_files if f[0].startswith('/a/0/')]
    print(f"Files in /a/0/: {len(a0_files)}")
    for f in sorted(a0_files):
        if f[0].startswith('/a/0/1') or f[0].startswith('/a/0/2'):
            print(f"  {f[0]}: size={f[1]}")
