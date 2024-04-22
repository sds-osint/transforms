from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx import overlays
from extensions import wordpress_registry
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
    """
    Gets WordPress Users using WP API.
    """

    # Initialize session with User-Agent header
    session = requests.Session()
    ua = UserAgent()
    session.headers.update({'User-Agent': ua.random})

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # Build the website URL
        og_website = request.Value
        api_link = '/wp-json/wp/v2/users'
        url = f'https://{og_website}{api_link}'

        try:
            resp = cls.session.get(url)
            resp.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX

            users = resp.json()  # Directly use the returned list of users

            for user in users:
                name = user.get("name", "")
                entity = response.addEntity("maltego.Person", name)
                wp_link = user.get('_links', {}).get('self', [{}])[0].get('href', '')
                entity_properties = [
                    ("FullName", "Full Name", name),
                    ("id", "ID", user.get("id", "")),
                    ("url", "URL", user.get("url", "")),
                    ("description", "Description", user.get("description", "")),
                    ("link", "Link", user.get("link", "")),
                    ("slug", "Slug", user.get("slug", "")),
                    ("avatar_url", "Avatar", user.get("avatar_urls", {}).get("96", "")),
                    ("wp_link", "WP Link", wp_link)
                ]

                avatar_url = user.get("avatar_urls", {}).get("96", "")

                for field_name, display_name, value in entity_properties:
                    entity.addProperty(fieldName=field_name, displayName=display_name, value=value)
                    entity.setIconURL(avatar_url)

        except requests.exceptions.HTTPError as e:
            response.addUIMessage(f"HTTP Error: {e}", messageType="PartialError")
        except requests.exceptions.RequestException as e:
            response.addUIMessage(f"Request failed: {e}", messageType="FatalError")


