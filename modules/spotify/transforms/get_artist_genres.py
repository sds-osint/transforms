from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx import overlays
from extensions import spotify_registry
from settings import spotify_client_id, spotify_client_secret
import requests
import json

@spotify_registry.register_transform(
    display_name="Get Artist Genres",
    input_entity="maltego.Person",
    description="Extracts the Artist's Genres",
    settings=[],
    output_entities=[],
)

class get_artist_genres(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        genres = request.getProperty("Genres")
        
        if genres:
            genre_list = [genre.strip() for genre in genres.split(",")]
            for genre in genre_list:
                response.addEntity('maltego.Phrase', genre)
        else:
            response.addUIMessage("Error: 'Genres' property not found or is empty.")

# if __name__ == "__main__":
#     import sys
#     msg = MaltegoMsg(sys.stdin.read())
#     get_artist_genres.create_entities(msg, MaltegoTransform())
