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

class get_wp_posts(DiscoverableTransform):
    session = requests.Session()
    ua = UserAgent()
    session.headers.update({'User-Agent': ua.random})

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        og_website = request.Value
        page_count = int(request.getTransformSetting(pagination_count.id))
        page_number = 1
        request_type = 'posts'

        while page_number <= page_count:    
            
            api_link = f'/wp-json/wp/v2/{request_type}?per_page=100&page={page_number}'
            url = f'https://{og_website}{api_link}'

            try:
                resp = cls.session.get(url)
                resp.raise_for_status()  
                
                results = resp.json()  

                if not results:
                    break

                for result in results:
                    name = result.get("title", {}).get("rendered")
                    entity = response.addEntity("maltego.Phrase", name)
                    entity_properties = [
                        ("date_gmt", "Date (GMT)", result.get("date_gmt", "")),
                        ("modified_gmt", "Modified Date (GMT)", result.get("modified_gmt", "")),
                        ("link", "Link", result.get("link", "")),
                        ("title", "Title", result.get("title", {}).get("rendered", "")),
                        ("content", "Content", result.get("content", {}).get("rendered", "")),
                        ("author", "Author", result.get("author", 0)),
                        ("tags", "Tags", result.get("tags", [])),
                        ("self_link", "Self Link", result.get("_links", {}).get("self", [{}])[0].get("href", "")),
                        ("author_link", "Author Link", result.get("_links", {}).get("author", [{}])[0].get("href", ""))
                    ]

                    for field_name, display_name, value in entity_properties:
                        entity.addProperty(fieldName=field_name, displayName=display_name, value=value)

            except requests.exceptions.HTTPError as e:
                response.addUIMessage(f"HTTP Error: {e}", messageType="PartialError")
            except requests.exceptions.RequestException as e:
                response.addUIMessage(f"Request failed: {e}", messageType="FatalError")
            
            page_number = page_number + 1