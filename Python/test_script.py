import lyricsgenius
import logging
from time import time

logging.basicConfig(format='%(asctime)-15s [%(levelname)s]  %(message)s',
                    filename="genius.log")
genius_logger = logging.getLogger('genius_download')

DOWNLOAD_RETRIES = 5

GENIUS_ACCESS_TOKEN = ''
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["(.?Remix)", "(Live)", "(Acoustic Version)"]
genius.retries = 3

test_list = ["Jason Derulo", "Taco Hemingway", "Quebonafide", "Klocuch"]


def save_artists(artists_list):
    for artist in artists_list:
        i=0
        while i < DOWNLOAD_RETRIES:
            genius_logger.info("Trying to download data for artist called {0}...".format(artist))
            try:
                artist_lyrics = genius.search_artist(artist, sort="title", max_songs=10, include_features=False, allow_name_change=False)
            except TypeError:
                print("Type error, retrying...")
                genius_logger.warning("Download failed for {0}, {1} tries remaining".format(
                    artist, DOWNLOAD_RETRIES - i - 1))
                i += 1
                continue
            break
        if i < DOWNLOAD_RETRIES:
            genius_logger.info("Download for {0} succedded, saving to JSON...".format(artist))
            try:
                artist_lyrics.save_lyrics("{}.json".format(artist), overwrite=True, ensure_ascii=False)
                genius_logger.info("Saved {0} to JSON successfully".format(artist))
            except UnicodeEncodeError:
                print("Unicode error, saving ensuring ascii...")
                genius_logger.warning("Failed to save {0} to JSON, trying with ASCII...".format(artist))
                artist_lyrics.save_lyrics("{}.json".format(artist), overwrite=True, ensure_ascii=True)

t1=time()
save_artists(test_list)
t2=time()
print("saved in {}".format(t2-t1))