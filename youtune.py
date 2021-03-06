import os
import logging
import codecs
import itertools
import shutil
from pathlib import Path
from os.path import relpath

class YouTune:
    ''' '''
    def __init__(self, source_music_file=None,
                 source_path_prefix='',
                 target_music_file=None,
                 target_path_prefix='',
                 logger=None):
        self.source_music_file = source_music_file
        self.source_path_prefix = source_path_prefix
        self.target_music_file = target_music_file
        self.target_path_prefix = target_path_prefix
        self.logger = logger or logging.getLogger(__name__)
    
    def version(self):
        return "v0.01"
    
    def _get_music_iter(self, file, heads=None):
        it = MusicGenerator(file)
        if heads == None:
            return it
        else:
            return itertools.islice(it, heads)
   
    def find_missing_songs(self):
        lookups = [ relpath(song, self.target_path_prefix) for song in self._get_music_iter(self.target_music_file, 200) ]
        rel_path = lambda song_path: relpath(song_path, self.source_path_prefix)
        return [Path(song).as_posix() for song in map(rel_path, self._get_music_iter(self.source_music_file, 100)) if song not in lookups]

    def copy_missing_songs(self, mising_songs, dryRun=True, maxCount=-1):
        for count, song_path in enumerate(mising_songs):
            source_path = "%s%s" % (self.source_path_prefix, song_path)
            target_path = "%s%s" % (self.target_path_prefix, song_path)
            try:
                if os.path.isdir(target_path):
                    self.logger.info('Create a directory "%s"' % target_path)
                    if not dryRun:
                        Path(target_path).mkdir(parents=True, exist_ok=True)
                else:
                    self.logger.info('cp "%s" "%s"' % (source_path, target_path))
                    if not dryRun:
                        shutil.copyfile(source_path, target_path) 
            except Exception as e:
                self.logger.error('ERROR - Unable to process %s - %s' % (target_path, e))
            if count == maxCount:
                break
    
    def setup(self):
        self.source_music_file = './sourceMusic.txt'
        self.source_path_prefix = '/Users/junesung/Music/iTunes/iTunes Media/Music/'
        self.target_music_file = './destMusic.txt'
        self.target_path_prefix = '/Volumes/Public/Shared Music/iTunes Media/Music/'
        
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

''' file is not closed after generator runs
class MusicGenerator2:
    ''''''
    def __init__(self, file_name):
        self.file_name = file_name
        
    def __iter__(self):
        fd = codecs.open(self.file_name, 'r', 'utf-8')
        return (line.strip() for line in fd)
'''

if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    logger = logging.getLogger('YouTuneLogger')
    
    handler = logging.FileHandler('YouTune.log', encoding='utf-8')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    
    yt = YouTune(logger=logger)
    yt.setup()
    missing_songs = yt.find_missing_songs()
    logger.info('Total missing songs=%d' % len(missing_songs))
    yt.copy_missing_songs(missing_songs)
    logger.info('Done.')