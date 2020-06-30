import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import argparse


def getSpotifyIdsFromFile(file_name):
    with open(file_name, encoding="utf-8") as file:
        urls = []
        for line in file:
            found_items = re.findall(
                'https?://open\.spotify\.com/track/([\w]+)\?', line)
            if len(found_items) > 0:
                urls.append(found_items[0])

    return urls


def show_tracks(tracks):
    for i, item in enumerate(tracks["items"]):
        track = item["track"]
        print(
            "   %2d %s: %s | %s"
            % (i, track["artists"][0]["name"], track["name"], track["uri"])
        )


def listAllTracksInPlaylist(sp, playlist):
    print("total tracks", playlist["tracks"]["total"])
    results = sp.playlist(playlist["id"], fields="tracks,next")
    tracks = results["tracks"]
    show_tracks(tracks)
    while tracks["next"]:
        tracks = sp.next(tracks)
        show_tracks(tracks)


def getLastTrackId(sp, playlist):
    items = sp.playlist_tracks(playlist["id"])["items"]
    return items[len(items) - 1]["track"]["id"]


parser = argparse.ArgumentParser(
    description="Parse links from text and add them to a playlist")
parser.add_argument('--input', required=True)
parser.add_argument('--playlistName', required=True)
parser.add_argument('--append', action='store_true')
args = parser.parse_args()

scope = "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"
track_ids_from_file = getSpotifyIdsFromFile(args.input)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope))
playlists = sp.current_user_playlists()
for playlist in playlists["items"]:
    print(playlist["name"])

    if playlist["name"] == args.playlistName:
        if playlist["tracks"]["total"] == len(track_ids_from_file):
            print("playlist is up to date!")
        else:
            # check for empty playlist
            if playlist["tracks"]["total"] == 0 or args.append:
                print("add all tracks from text")
                index_to_start_from = 0
            else:
                # if playlist is not empty, get last id currently in the playlist
                last_track_id = getLastTrackId(sp, playlist)
                print("last track id is", last_track_id)
                # find this id in the list of id pulled from file, and get its last index (last because it may be here more than once)
                all_matches = [i for i, e in enumerate(
                    track_ids_from_file) if e == last_track_id]
                if len(all_matches) < 1:
                    # last track in text not found in plist, this is a different set of tracks
                    # should be appended instead
                    raise Exception(
                        "parsed links don't match playlist contents. use --append option to add new set of tracks")
                last_index = all_matches[len(all_matches) - 1]
                print(last_index)
                # continue adding tracks to the playlist based on this index
                index_to_start_from = last_index + 1
                if index_to_start_from == len(track_ids_from_file):
                    # there are no new tracks to add, don't bother trying
                    print("no new tracks to add!")
                    exit()
            # check for track limit 100; if exceeded, split into multiple calls
            sp.trace = False
            user_id = sp.me()['id']
            tracks_to_add = track_ids_from_file[index_to_start_from:]
            if len(tracks_to_add) >= 100:
                chunks = [tracks_to_add[x:x+100]
                          for x in range(0, len(tracks_to_add), 100)]
                for chunk in chunks:
                    results = sp.user_playlist_add_tracks(
                        user_id, playlist["id"], chunk)
                    print(results)
            else:
                results = sp.user_playlist_add_tracks(
                    user_id, playlist["id"], tracks_to_add)
                print(results)

        break
