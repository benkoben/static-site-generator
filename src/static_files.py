import os
import shutil

"""
    copy_static recursively copies all the contents of a source folder to a destination folder
"""
def copy_static(src:str, dst:str):
    for item in os.listdir(src):
        src_rel_path = os.path.join(src, item)
        dst_rel_path = os.path.join(dst, item)
        if os.path.isfile(src_rel_path):
            print(f"[INFO] copying {src_rel_path} to {dst_rel_path}")
            shutil.copy(src_rel_path, dst_rel_path)
        else:
            if not os.path.exists(dst_rel_path):
                print(f"[INFO] creating directory {dst_rel_path}")
                os.mkdir(dst_rel_path)
            copy_static(src_rel_path, dst_rel_path)