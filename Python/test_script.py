import lyricsgenius
from time import time
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
        while i < 5:
            try:
                artist_lyrics = genius.search_artist(artist, sort="title", max_songs=10 ,include_features=False, allow_name_change=False)
            except TypeError:
                print("Type error, retrying...")
                i += 1
                continue
            break
        if i < 5:
            try:
                artist_lyrics.save_lyrics("{}.json".format(artist), overwrite=True, ensure_ascii=False)
            except UnicodeEncodeError:
                print("Unicode error, saving ensuring ascii...")
                artist_lyrics.save_lyrics("{}.json".format(artist), overwrite=True, ensure_ascii=True)

t1=time()
save_artists(test_list)
t2=time()
print("saved in {}".format(t2-t1))