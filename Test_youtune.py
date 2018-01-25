import unittest
from itunesutils import youtune
import itertools

class TestYouTube(unittest.TestCase):
    
    def setup(self):
        self.source_file = './sourceMusic.txt'
        pass
    
    def test_find_missing_songs(self):
        yt = youtune.YouTune('./sourceMusic.txt', '/Users/junesung/Music/iTunes/iTunes Media/Music/',
                     './destMusic.txt', '/Volumes/Public/Shared Music/iTunes Media/Music/')
        missing_songs = yt.find_missing_songs()
        self.assertTrue(len(missing_songs) > 0)
    '''
    def test_MusicSequence(self):
        songs = youtune.MusicSequence(self.source_file)
        print('total songs: %d' % len(songs))
        self.assertTrue(len(songs) > 0)
    
    def test_MusicIterator(self):
        songs = youtune.MusicIterator(self.source_file)
        for index, song in enumerate(songs):
            if (index % 5000 == 0):
                print('%s\n' % song)
        self.assertTrue(len(songs) > 0)
        
    def test_MusicGenerator2(self):
        songs = youtune.MusicGenerator2(self.source_file)
        gen = itertools.takewhile(lambda t: t[0] < 5, enumerate(songs))
        for i, s in gen:
            print(s)
        print(list(itertools.islice(songs, 5)))
        self.assertTrue(len(songs) > 0)
    '''
        
if __name__ == '__main__':
    unittest.main()