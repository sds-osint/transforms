from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx import overlays
from extensions import spotify_registry
from settings import spotify_client_id, spotify_client_secret
import requests
import json

@spotify_registry.register_transform(
    display_name="Get Artists Albums",
    input_entity="maltego.Person",
    description="Extracts the Artist's Albums",
    settings=[],
    output_entities=[],
)

class get_artist_albums(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        artist_id = request.getProperty("Artist ID")
        
        if not artist_id:
            response.addUIMessage("Error: 'Artist ID' property not found in the request.")
            return
        
        try:
            album_data = cls.get_artist_albums(artist_id)
            
            for album in album_data['items']:
                entity = response.addEntity("maltego.Alias", album['name'])
                entity.addProperty(fieldName="release_date", displayName="Release Date", value=album['release_date'])
                entity.addProperty(fieldName="total_tracks", displayName="Total Tracks", value=str(album['total_tracks']))
                entity.addProperty(fieldName="album_id", displayName="Album ID", value=album['id'])
                entity.addProperty(fieldName="Spotify URL", displayName="Spotify URL", value=album['external_urls']['spotify'])
                if album['images']:
                    entity.setIconURL(album['images'][0]['url'])

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
    def get_artist_albums(cls, artist_id):
        access_token = cls.request_access_token()

        params = {
            'include_groups': 'album,single,appears_on,compilation',
            'market': 'US',
            'limit': '20',
            'offset': '0'
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/albums', params=params, headers=headers)
        response.raise_for_status() 

        json_data = response.json()

        return json_data


if __name__ == "__main__":
    import sys
    msg = MaltegoMsg(sys.stdin.read())
    get_artist_albums.create_entities(msg, MaltegoTransform())
