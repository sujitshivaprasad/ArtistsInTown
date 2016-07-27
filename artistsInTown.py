# export SPOTIPY_CLIENT_ID='1b06efc1ba9442d29cd627e3104b2647'
# export SPOTIPY_CLIENT_SECRET='2b5b918bd415413e8b1b3470f29b7199'
# export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

# shows artist info for a URN or URL
import pprint
import sys

import spotipy
import spotipy.util as util
import simplejson as json
import bandsintown

bandsintown.app_id = "artistsInTown_python"

#Lets use the spotipy (spotify python API wrapper) to get my favorite artists!

#This part works to get the users top artists (short, medium and long term)
def favSpotifyArtists():
	shortArtists, medArtists, longArtists = [], [], []

	if len(sys.argv) > 1:
		username = sys.argv[1]
	else:
		print("Usage: %s username" % (sys.argv[0],))
		sys.exit()

	scope = 'user-top-read'
	token = util.prompt_for_user_token(username, scope)

	if token:
		sp = spotipy.Spotify(auth=token)
		sp.trace = False
		ranges = ['short_term', 'medium_term', 'long_term']
		for range in ranges:
			#print "range:", range
			results = sp.current_user_top_artists(time_range=range, limit=50)
			for i, item in enumerate(results['items']):
				#print i, item['name']
				name = item['name']
				if name == 'short_term':
					shortArtists.append(name.encode("utf-8"))
					return shortArtists
				elif name == 'medium_term':
					medArtists.append(name.encode("utf-8"))
					return medArtists
		 		else:
					longArtists.append(name.encode("utf-8"))
					return longArtists
			print
	else:
		print("Can't get token for", username)



#Lets use the bandsintown API to find the bands in my town!

def check_events(events):
	artists, venue, datetime= [], [], []
	for e in events:
		#print "%s %s (%s %s)" % (e.venue.name, e.datetime, e.venue.city, e.venue.country)
		#print "  %s" % (", ".join([a.name for a in e.artists]), )
		for a in e.artists:
			artists.append(a.name)
			venue.append(e.venue.name)
			datetime.append(e.datetime)
	return artists, venue, datetime


def compare(spotify, bandsintown, venue, datetime):
	found = []
	for band in spotify:
		for near in bandsintown:
			if band == near:
				found.append(band)
	if len(found) > 0:
		print 'The following bands are coming to town: %s and they will play at %s at %s' % (found, venue, datetime)
	else:
		print 'Sorry, none of your favorite artists are in town soon.'


#events = bandsintown.Artist.events(mbid="65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab")
#print_events(events)
if __name__ == '__main__':
	events = bandsintown.Event.search(location="Cincinnati", per_page=50)
	artist, venue, datetime = check_events(events)
	fav = favSpotifyArtists()
	compare(fav, artists, venue, datetime)


#events = bandsintown.Event.recommended(mbids=["65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab"], location="Cincinnati", per_page=10)
#print_events(events)
