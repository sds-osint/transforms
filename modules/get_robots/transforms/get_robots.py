from extensions import get_robots_registry
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.overlays import OverlayPosition, OverlayType
import requests
from fake_useragent import UserAgent

@get_robots_registry.register_transform(
    display_name="Get Robots.txt", 
    input_entity="maltego.Website",
    description='Finds which addresses are mentioned in the robots.txt',
    output_entities=["maltego.URL"])

class get_robots(DiscoverableTransform):

    session = requests.Session()
    ua = UserAgent()
    session.headers.update({'User-Agent': ua.random})
    
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        website_url = request.Value  
        scheme = 'https://'
        robots_path = '/robots.txt'
        url = f'{scheme}{website_url}{robots_path}'

        try:
            resp = cls.session.get(url)
            resp.raise_for_status()
            site_text = resp.text
            # response.addUIMessage("Test")

            for line in site_text.strip().split('\n'):
                if ': ' in line:
                    directive, value = line.split(': ', 1)
                    path_url = f'{scheme}{website_url}{value}'
                    entity = response.addEntity('maltego.URL')

                    if 'Disallow' in directive:
                        entity.addProperty(fieldName='url', displayName='URL', value=path_url)
                        entity.addProperty(fieldName='short-title', displayName='Short Title', value=value)
                        entity.addProperty(fieldName='status', displayName='Status', value='Disallowed')
                        entity.addOverlay('#f44336', OverlayPosition.NORTH_WEST, OverlayType.COLOUR)
                        # entity.setBookmark(4)

                    elif 'Allow' in directive:
                        entity.addProperty(fieldName='url', displayName='URL', value=path_url)
                        entity.addProperty(fieldName='short-title', displayName='Short Title', value=value)
                        entity.addProperty(fieldName='status', displayName='Status', value='Allowed')
                        entity.addOverlay('#45e06f', OverlayPosition.NORTH_WEST, OverlayType.COLOUR)
                        # entity.setBookmark(1)

                    elif 'Sitemap' in directive:
                        entity.addProperty(fieldName='short-title', displayName='Short Title', value=value)
                        entity.addProperty(fieldName='status', displayName='Status', value='Sitemap')
                        entity.addProperty(fieldName='url', displayName='URL', value=value)

        except requests.exceptions.HTTPError as e:
            response.addUIMessage(f"HTTP Error: {e}", messageType="PartialError")
        except requests.exceptions.RequestException as e:
            response.addUIMessage(f"Request failed: {e}", messageType="FatalError")