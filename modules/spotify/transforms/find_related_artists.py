from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx import overlays
from extensions import spotify_registry
from settings import spotify_client_id, spotify_client_secret
import requests
import json

@spotify_registry.register_transform(
    display_name="Find Related Artists",
    input_entity="maltego.Person",
    description="Searches Spotify for Related Artists",
    settings=[],
    output_entities=[],
)


class find_related_artists(DiscoverableTransform):
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        artist_id = request.getProperty("Artist ID")
        
        if not artist_id:
            response.addUIMessage("Error: 'Artist ID' property not found in the request.")
            return
        
        try:
            related_artists_data = cls.request_related_artist_data(artist_id)
            
            for artist_data in related_artists_data['artists']:
                entity = response.addEntity("maltego.Person", artist_data['name'])
                entity.addProperty(fieldName="Artist ID", displayName="Artist ID", value=artist_data['id'])
                entity.addProperty(fieldName="Popularity", displayName="Popularity", value=artist_data['popularity'])
                entity.addProperty(fieldName="Genres", displayName="Genres", value=", ".join(artist_data['genres']))
                entity.addProperty(fieldName="Spotify URL", displayName="Spotify URL", value=artist_data['external_urls']['spotify'])
                if artist_data['images']:
                    entity.setIconURL(artist_data['images'][0]['url'])

        except Exception as e:
            response.addUIMessage(f"Error: {str(e)}")
        
    @staticmethod
    def request_access_token():
        
        client_id = MaltegoMsg.getTransformSetting(spotify_client_id.id)
        client_secret = MaltegoMsg.getTransformSetting(spotify_client_secret.id)

        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }

        response = requests.post('https://accounts.spotify.com/api/token', data=data)
        response.raise_for_status()
        json_data = response.json()
        
        access_token = json_data["access_token"]
        
        return access_token

    @classmethod
    def request_related_artist_data(cls, artist_id):
        access_token = cls.request_access_token()

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/related-artists', headers=headers)
        response.raise_for_status() 

        json_data = response.json()

        return json_data


if __name__ == "__main__":
    import sys
    msg = MaltegoMsg(sys.stdin.read())
    find_related_artists.create_entities(msg, MaltegoTransform())
