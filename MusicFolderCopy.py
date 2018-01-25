from pathlib import Path
import os
import shutil
from os.path import abspath

def get_subpaths(path):
    lst = [path]
    for p in path.iterdir():
        if p.is_dir():
            lst.extend(get_subpaths(p))
        else:
            lst.append(p)
    return lst       
            

def find_missing_paths(src_path_list, dst_path_list):
    return [p for p in src_path_list if p not in dst_path_list]
        
def copy_missing_paths(mising_paths, dst_root, dryRun=True, maxCount=-1):
    count = 0
    for p in mising_paths:
        try:
            if os.path.isdir(p):
                dir_name = '%s/%s' % (dst_root, p)
                if not dryRun:
                    Path(dir_name).mkdir(parents=True, exist_ok=True)
                print('Create a directory %s' % dir_name)
            else:
                file_name = '%s/%s' % (dst_root, p)
                if not dryRun:
                    shutil.copyfile(abspath(p), file_name) 
                print('cp %s %s' % (abspath(p), file_name))
        except:
            print('ERROR - Unable to process %s/%s' % (dst_root, p))
        count += 1
        if count == maxCount:
            break

def get_src_dst_path_list():
    global cur_dir, src_dir, dst_dir
    os.chdir(src_dir)
    src_path_list = get_subpaths(Path('.'))
    os.chdir(dst_dir)
    dst_path_list = get_subpaths(Path('.'))
    return src_path_list, dst_path_list


itunes_dir = '/Users/junesung/Music/iTunes/iTunes Media/Music'
mycloud_dir = '/Volumes/Public/Shared Music/iTunes Media/Music'

test_src_dir = '/Users/junesung/Documents/workspace/iTunesProject/test_dir/src' 
test_dst_dir = '/Users/junesung/Downloads/test_dir/dst'

cur_dir = os.getcwd()
src_dir = itunes_dir
dst_dir = mycloud_dir

src_path_list, dst_path_list = get_src_dst_path_list()

os.chdir(src_dir)

missing_paths = find_missing_paths(src_path_list, dst_path_list)
print("Total %d paths to copy." % len(missing_paths))

copy_missing_paths(missing_paths, dst_dir, maxCount=10)