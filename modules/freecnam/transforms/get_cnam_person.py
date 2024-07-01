from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx import overlays
from extensions import freecnam_registry
from fake_useragent import UserAgent
import requests

@freecnam_registry.register_transform(
    display_name="Get FreeCNAM Person",
    input_entity="maltego.Phone",
    description="Get FreeCNAM Person",
    settings=[],
    output_entities=["maltego.Person"],
)

class get_cnam_person(DiscoverableTransform):
    # Initialize session with User-Agent header
    session = requests.Session()
    ua = UserAgent()
    session.headers.update({'User-Agent': ua.random})

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # Build the website URL
        input_num = request.Value
        url = f'https://freecnam.org/dip?q={input_num}'

        try:
            resp = cls.session.get(url)
            resp.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX

            cnam_response = requests.get(url)
            owner = cnam_response.text

            entity = response.addEntity('Person', owner)
            entity.addProperty('person.fullname', 'Full Name', 'strict', owner)

        except requests.exceptions.HTTPError as e:
            response.addUIMessage(f"HTTP Error: {e}", messageType="PartialError")
        except requests.exceptions.RequestException as e:
            response.addUIMessage(f"Request failed: {e}", messageType="FatalError")


