import unittest
import youtune
import itertools
#import warnings
#warnings.simplefilter("ignore", ResourceWarning)

class TestYouTube(unittest.TestCase):
    
    def setup(self):
        pass
    
    def test_find_missing_songs(self):
        yt = youtune.YouTune('./sourceMusic.txt',
                             '/Users/junesung/Music/iTunes/iTunes Media/Music/',
                             './destMusic.txt',
                             '/Volumes/Public/Shared Music/iTunes Media/Music/')
        missing_songs = yt.find_missing_songs()
        print(len(missing_songs))
        self.assertTrue(len(missing_songs) > 0)

    def test_MusicSequence(self):
        songs = youtune.MusicSequence('./sourceMusic.txt')
        print('total songs: %d' % len(songs))
        self.assertTrue(len(songs) > 0)
    
    def test_MusicIterator(self):
        songs = youtune.MusicIterator('./sourceMusic.txt')
        for index, song in enumerate(songs):
            if (index % 5000 == 0):
                print('%s\n' % song)
        self.assertTrue(True)
        
    def test_MusicGenerator(self):
        songs = youtune.MusicGenerator('./sourceMusic.txt')
        gen = itertools.takewhile(lambda t: t[0] < 5, enumerate(songs))
        for _, s in gen:
            print(s)
        print(list(itertools.islice(songs, 5)))
        self.assertTrue(True)

        
if __name__ == '__main__':
    unittest.main()
    #unittest.main(warnings='ignore')