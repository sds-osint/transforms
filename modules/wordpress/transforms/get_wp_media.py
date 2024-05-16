from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx import overlays
from extensions import wordpress_registry
from settings import pagination_count
from fake_useragent import UserAgent
import requests

@wordpress_registry.register_transform(
    display_name="Get WordPress Media",
    input_entity="maltego.Website",
    description="Get WordPress Media",
    settings=[],
    output_entities=["maltego.Image"],
)

class get_wp_media(DiscoverableTransform):
    session = requests.Session()
    ua = UserAgent()
    session.headers.update({'User-Agent': ua.random})

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        og_website = request.Value
        page_count = int(request.getTransformSetting(pagination_count.id))
        page_number = 1
        request_type = 'media'

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
                    name = result.get("slug", "")
                    entity = response.addEntity("maltego.Image", name)

                    basic_properties =[
                        ("description", "Description", result.get("slug")),
                        ("source_description", "Source Description", result.get("description", {}).get("rendered")),
                        ("date_gmt", "Date (GMT)", result.get("date_gmt", "")),
                        ("modified_gmt", "Modified Date (GMT)", result.get("modified_gmt", "")),
                        ("title", "Title", result.get("title", {}).get("rendered", "")),
                        ("url", "URL", result.get("guid", {}).get("rendered", "")),
                        ("caption", "Caption", result.get("caption", {}).get("rendered")),
                        ("alt_text", "Alt Text", result.get("alt_text", "")),
                        ("author", "Author", result.get("_links", {}).get("author", [{}])[0].get("href"))
                    ]
                    
                    # Media Details
                    media_details_properties = [
                        ("width", "Width", result.get("media_details", {}).get("width")),
                        ("height", "Height", result.get("media_details", {}).get("height"))
                    ]
                    
                    # Image Metadata
                    image_metadata_properties = [
                        ("aperture", "Aperture", result.get("media_details", {}).get("image_meta", {}).get("aperture")),
                        ("credit", "Credit", result.get("media_details", {}).get("image_meta", {}).get("credit")),
                        ("camera", "Camera", result.get("media_details", {}).get("image_meta", {}).get("camera")),
                        ("caption", "Caption", result.get("media_details", {}).get("image_meta", {}).get("caption")),
                        ("created_timestamp", "Created At", result.get("media_details", {}).get("image_meta", {}).get("created_timestamp")),
                        ("copyright", "Copyright", result.get("media_details", {}).get("image_meta", {}).get("copyright")),
                        ("focal_length", "Focal Length", result.get("media_details", {}).get("image_meta", {}).get("focal_length")),
                        ("iso", "ISO", result.get("media_details", {}).get("image_meta", {}).get("iso")),
                        ("shutter_speed", "Shutter Speed", result.get("media_details", {}).get("image_meta", {}).get("shutter_speed")),
                        ("title", "Title", result.get("media_details", {}).get("image_meta", {}).get("title")),
                        ("orientation", "Orientation", result.get("media_details", {}).get("image_meta", {}).get("orientation")),
                        ("keywords", "Keywords", result.get("media_details", {}).get("image_meta", {}).get("keywords"))
                    ]
                    
                    media_url = result.get("guid", {}).get("rendered", "")

                    # Add the first 8 items
                    for field_name, display_name, value in basic_properties:
                        entity.addProperty(fieldName=field_name, displayName=display_name, value=value)

                    # Add non-empty Media Details items
                    for field_name, display_name, value in media_details_properties:
                        if value and value != '0':
                            entity.addProperty(fieldName=field_name, displayName=display_name, value=value)
                    
                    # Add non-empty Image Metadata items
                    for field_name, display_name, value in image_metadata_properties:
                        if value and value != '0':
                            entity.addProperty(fieldName=field_name, displayName=display_name, value=value)
                    
                    entity.setIconURL(media_url)

            except requests.exceptions.HTTPError as e:
                response.addUIMessage(f"HTTP Error: {e}", messageType="PartialError")
            except requests.exceptions.RequestException as e:
                response.addUIMessage(f"Request failed: {e}", messageType="FatalError")
            
            page_number = page_number + 1
