from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx import overlays
from extensions import spotify_registry
from settings import spotify_client_id, spotify_client_secret
import requests
import json

@spotify_registry.register_transform(
    display_name="Search Spotify for Artist",
    input_entity="maltego.Person",
    description="Searches Spotify for Artist information",
    settings=[],
    output_entities=[],
)
class find_artist(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        artist_name = request.getProperty("person.fullname")
        
        try:
            artist_data = cls.request_artist_data(request, artist_name)
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
    def request_access_token(request: MaltegoMsg):
        client_id = request.getTransformSetting(spotify_client_id.id)
        client_secret = request.getTransformSetting(spotify_client_secret.id)

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

    @staticmethod
    def request_artist_id(access_token, artist_name):
        params  = {
            'q': artist_name,
            'type': 'artist',
            'market': 'US',
            'limit': '10',
            'offset': '0',
            'include_external': ''
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers)
        response.raise_for_status()

        json_data = response.json()
        artists = json_data['artists']['items']

        if not artists:
            raise ValueError(f"No artist found for {artist_name}")

        artist_id = artists[0]['id']

        return artist_id

    @classmethod
    def request_artist_data(cls, request: MaltegoMsg, artist_name):
        access_token = cls.request_access_token(request)
        artist_id = cls.request_artist_id(access_token, artist_name)

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}', headers=headers)
        response.raise_for_status() 

        json_data = response.json()

        return json_data


if __name__ == "__main__":
    import sys
    msg = MaltegoMsg(sys.stdin.read())
    transform = MaltegoTransform()
    find_artist.create_entities(msg, transform)
    print(transform.returnOutput())
