import os
import codecs
import itertools
import shutil
from pathlib import Path
from os.path import relpath

class YouTune:
    ''' '''
    def __init__(self, source_music_file,
                 source_path_prefix,
                 target_music_file,
                 target_path_prefix):
        self.source_music_file = source_music_file
        self.source_path_prefix = source_path_prefix
        self.target_music_file = target_music_file
        self.target_path_prefix = target_path_prefix
    
    def version(self):
        return "v0.01"
    
    def _get_music_iter(self, file, heads=None):
        it = MusicGenerator2(file)
        if heads == None:
            return it
        else:
            return itertools.islice(it, heads)
   
    def find_missing_songs(self):
        lookups = [ relpath(song, self.target_path_prefix) for song in self._get_music_iter(self.target_music_file, 200) ]
        rel_path = lambda song_path: relpath(song_path, self.source_path_prefix)
        return [Path(song).as_posix() for song in map(rel_path, self._get_music_iter(self.source_music_file, 100)) if song not in lookups]

    def copy_missing_songs(self, mising_songs, dryRun=True, maxCount=-1):
        count = 0
        for song_path in mising_songs:
            try:
                source_path = "%s%s" % (self.source_path_prefix, song_path)
                target_path = "%s%s" % (self.target_path_prefix, song_path)
                if os.path.isdir(target_path):
                    if not dryRun:
                        Path(target_path).mkdir(parents=True, exist_ok=True)
                    print('Create a directory %s' % target_path)
                else:
                    if not dryRun:
                        shutil.copyfile(source_path, target_path) 
                    print('cp %s %s' % (source_path, target_path))
            except:
                print('ERROR - Unable to process %s' % target_path)
            count += 1
            if count == maxCount:
                break
        
        
class MusicSequence:
    ''' sequence implementation to load songs from a file'''
    def __init__(self, file_name):
        self.file_name = file_name
        with codecs.open(file_name, 'r', 'utf-8') as fd:
            self.songs = [line for line in fd ]
        
    def __getitem__(self, index):
        return self.songs[index]
    
    def __len__(self):
        return len(self.songs)
    
    def __repr__(self):
        return '%s' % self.file_name
    
class MusicIterator:
    ''' iterator implementation to load songs from a file'''
    def __init__(self, file_name):
        self.file_name = file_name
        self.fd = codecs.open(self.file_name, 'r', 'utf-8')
    
    def __iter__(self):
        return self    
    
    def __next__(self):
        line = self.fd.readline().strip()
        if line:
            return line
        else:
            self.fd.close()
            raise StopIteration()

class MusicGenerator:
    ''''''
    def __init__(self, file_name):
        self.file_name = file_name
        
    def __iter__(self):
        with codecs.open(self.file_name, 'r', 'utf-8') as fd:
            for line in fd:
                yield line.strip()

class MusicGenerator2:
    ''''''
    def __init__(self, file_name):
        self.file_name = file_name
        
    def __iter__(self):
        fd = codecs.open(self.file_name, 'r', 'utf-8')
        return (line.strip() for line in fd)


if __name__ == '__main__':
    '''
    songs = MusicSequence('../sourceMusic.txt')
    print('total songs: %d' % len(songs))
    
    songs = MusicIterator('../sourceMusic.txt')
    for index, song in enumerate(songs):
        if (index % 5000 == 0):
            print('%s\n' % song)
    '''
    
    '''
    songs = MusicGenerator2('../sourceMusic.txt')
    gen = itertools.takewhile(lambda t: t[0] < 5, enumerate(songs))
    for i, s in gen:
        print(s)
    print(list(itertools.islice(songs, 5)))
    '''
    
    yt = YouTune('../sourceMusic.txt', '/Users/junesung/Music/iTunes/iTunes Media/Music/',
                 '../destMusic.txt', '/Volumes/Public/Shared Music/iTunes Media/Music/')
    missing_songs = yt.find_missing_songs()
    print('Total missing songs=%d' % len(missing_songs))
    
    yt.copy_missing_songs(missing_songs)
    
    print('Done.')