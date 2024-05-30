from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx import overlays
from extensions import wordpress_registry
from settings import pagination_count
from fake_useragent import UserAgent
import requests

@wordpress_registry.register_transform(
    display_name="Get WordPress Users",
    input_entity="maltego.Website",
    description="Get WordPress Users",
    settings=[],
    output_entities=["maltego.Person"],
)

class get_wp_users(DiscoverableTransform):
    session = requests.Session()
    ua = UserAgent()
    session.headers.update({'User-Agent': ua.random})

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        og_website = request.Value
        page_count = int(request.getTransformSetting(pagination_count.id))
        page_number = 1
        request_type = 'users'

        while page_number <= page_count:    
            
            api_link = f'/wp-json/wp/v2/{request_type}?per_page=100&page={page_number}'
            url = f'https://{og_website}{api_link}'

            try:
                resp = cls.session.get(url)
                resp.raise_for_status() 

                # Debugging: print the status code and the URL being requested
                print(f"Requesting URL: {url}")
                print(f"Status Code: {resp.status_code}")

                results = resp.json()

                # Debugging: print the JSON response length
                print(f"Response length: {len(results)}")

                if not results:
                    break

                for result in results:
                    name = result.get("name", "")
                    entity = response.addEntity("maltego.Person", name)
                    wp_link = result.get('_links', {}).get('self', [{}])[0].get('href', '')
                    entity_properties = [
                        ("FullName", "Full Name", name),
                        ("id", "ID", result.get("id", "")),
                        ("url", "URL", result.get("url", "")),
                        ("description", "Description", result.get("description", "")),
                        ("link", "Link", result.get("link", "")),
                        ("slug", "Slug", result.get("slug", "")),
                        ("avatar_url", "Avatar", result.get("avatar_urls", {}).get("96", "")),
                        ("wp_link", "WP Link", wp_link)
                    ]

                    avatar_url = result.get("avatar_urls", {}).get("96", "")

                    for field_name, display_name, value in entity_properties:
                        entity.addProperty(fieldName=field_name, displayName=display_name, value=value)
                        entity.setIconURL(avatar_url)

            except requests.exceptions.HTTPError as e:
                response.addUIMessage(f"HTTP Error: {e}", messageType="PartialError")
                print(f"HTTP Error: {e}")
            except requests.exceptions.RequestException as e:
                response.addUIMessage(f"Request failed: {e}", messageType="FatalError")
                print(f"Request failed: {e}")
            except ValueError as e:
                response.addUIMessage(f"JSON decode error: {e}", messageType="FatalError")
                print(f"JSON decode error: {e}")

            page_number = page_number + 1
