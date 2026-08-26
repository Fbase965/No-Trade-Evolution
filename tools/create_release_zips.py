import os
import zipfile

def create_zips():
    base_dir = r"E:\Pokemon-XY-No-Trade-Mod"
    pkg_dir = os.path.join(base_dir, "Mod-Package")
    releases_dir = os.path.join(base_dir, "Releases")
    os.makedirs(releases_dir, exist_ok=True)
    
    # 1. 3DS Luma3DS Zip
    luma_zip_path = os.path.join(releases_dir, "Pokemon_3DS_Luma3DS_NoTradeMod.zip")
    luma_source = os.path.join(pkg_dir, "3DS_Luma3DS")
    with zipfile.ZipFile(luma_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(luma_source):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, luma_source)
                zf.write(full_path, rel_path)
    print(f"Created: {luma_zip_path} ({os.path.getsize(luma_zip_path)} bytes)")

    # 2. Citra / Azahar Zip
    citra_zip_path = os.path.join(releases_dir, "Pokemon_Citra_Azahar_NoTradeMod.zip")
    citra_source = os.path.join(pkg_dir, "Citra_Lime3DS")
    with zipfile.ZipFile(citra_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(citra_source):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, citra_source)
                zf.write(full_path, rel_path)
    print(f"Created: {citra_zip_path} ({os.path.getsize(citra_zip_path)} bytes)")

if __name__ == "__main__":
    create_zips()
