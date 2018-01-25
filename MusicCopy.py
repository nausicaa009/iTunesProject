from pathlib import Path
import os
import codecs

def get_subpaths(f, path):
    for p in path.iterdir():
        if p.is_dir():
            f.write("%s\n" % os.path.abspath(p))
            get_subpaths(f, p)
        else:
            f.write("%s\n" % os.path.abspath(p))
    
def write_file(filename, path):
    f = codecs.open(filename, 'w', "utf-8")
    get_subpaths(f, path)
    f.close()
    print("Done.")

def read_file(filename):
    f = codecs.open(filename, 'r', "utf-8")
    for line in f:
        print(line)
    f.close()
    
itunes_dir = '/Users/junesung/Music/iTunes/iTunes Media/Music'
mycloud_dir = '/Volumes/Public/Shared Music/iTunes Media/Music'

path = Path(mycloud_dir)            

src_filename = "%s/sourceMusic.txt" % os.getcwd()
dst_filename = "%s/destMusic.txt" % os.getcwd()

write_file(dst_filename, path)
    
'''
i, maxCount = 0, -1
ite = get_subpaths(path)
for p in ite:
    if i == maxCount:
        break
    i += 1
    print(p)
'''