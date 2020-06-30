# AddLinksToSpotifyPlaylist
Parse text for Spotify track links, and add them to a playlist.
## Background
My friends and I have a Whatsapp chat where we share music with each other. I thought it would be a good idea to create a playlist from all the links shared in the chat. Since bot support is lacking on Whatsapp, an external solution was required. I found out that Whatsapp lets you export the contents of a chat into a text file (the chat is encrypted otherwise); from here, it was just a matter of parsing out the links in order to add them to Spotify.

After implementing this code, I was able to add all the links from the chat to a Spotify playlist.
I run this code periodically to add any new music that has been shared.

## Usage
```
addToSpotify.py --input <inputTextFile.txt> --playlistName <name> --append
```

The `--append` parameter is optional and should be included when adding a new set of links from a new source (text file).

The typical use case is parsing the same text file and adding any additional links that were not added previously (see background); however, if adding different sets of links from different text files is desired, use the `--append` option.

### How it works
This code makes use of the [Spotipy library](https://github.com/plamere/spotipy). Before using, ensure you have registered an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login) and set up environment variables for your app credentials, as shown in the [Spotipy docs](https://spotipy.readthedocs.io/en/2.13.0/#).
