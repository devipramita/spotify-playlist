import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

import numpy as np
import pandas as pd

CREDS = {
            "client_id": "a3762c103e23466a97dd23afab5fdcff",
            "client_secret": "e8091f92cfc04c7c89d1bc55e9ea754c"
        }
PLAYLIST_URI = {
                                    
                }

if __name__ == "__main__":

    # setup the credentials
    print("Credentials Manager")
    client_credentials_manager = SpotifyClientCredentials(
                                    client_id=CREDS["client_id"],
                                    client_secret=CREDS["client_secret"],
                                )
    # make the connection
    print("Making Connection")
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # choose playlist
    print("Choosing Playlist")
    playlist_uri = "spotify:playlist:5kYyGXB5ZhHlo03PkmM6rN"
    like = "true"
    username = "e547ja77k0ez557n0kbes9pur"
    playlist_id = playlist_uri.split(":")[2]
    
    # get the playlist
    print("Getting Playlist")
    results = sp.user_playlist(username, playlist_id, "tracks")
    with open('results.json', 'w') as f:
        json.dump(results, f)
    print("keys of TRACKS:", results["tracks"].keys())
    print("keys of TRACKS-ITEMS:", results["tracks"]["items"][0]["track"]["album"]["release_date"])
    
    # fetching the gotten playlist
    print("Fetching Playlist")
    playlist_tracks_data = results["tracks"]
    playlist_tracks_id = []
    playlist_tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []
    playlist_tracks_popularity = []
    playlist_tracks_genre = []
    playlist_tracks_release_date = []

    for track in playlist_tracks_data["items"]:
        playlist_tracks_id.append(track["track"]["id"])
        playlist_tracks_titles.append(track["track"]["name"])
        artist_list = []
        for artist in track["track"]["artists"]:
            artist_list.append(artist["name"])
        playlist_tracks_artists.append(artist_list)
        playlist_tracks_first_artists.append(artist_list[0])
        playlist_tracks_popularity.append(track["track"]["popularity"])
        playlist_tracks_release_date.append(track["track"]["album"]["release_date"])

    # get the audio features
    print("Getting Audio Features")
    features = sp.audio_features(playlist_tracks_id)
    with open('features.json', 'w') as f:
        json.dump(features, f)

    # data into dataframe
    print("Into Dataframe")
    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    features_df["title"] = playlist_tracks_titles
    features_df["first_artist"] = playlist_tracks_first_artists
    features_df["all_artists"] = playlist_tracks_artists
    features_df["release_date"] = playlist_tracks_release_date
    features_df["popularity"] = playlist_tracks_popularity
    
    features_df = features_df[["id", "title", "first_artist", "all_artists",
                                "danceability", "energy", "key", "loudness",
                                "mode", "speechiness", "acousticness", 
                                "instrumentalness", "liveness", "valence", 
                                "tempo", "duration_ms", "time_signature", 
                                "release_date", "popularity"]]
    
    features_df.tail()

    print("Saving to CSV")
    features_df.to_csv("playlist_beat_beat_slow.csv", index=False)