from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_DEBUG
from maltego_trx.entities import Location, Person, Email, PhoneNumber, Company, Phrase
from extensions import openpeoplesearch_registry
from settings import ops_auth, city_input, state_input
import requests
from ..helpers.record_processor import RecordProcessor


@openpeoplesearch_registry.register_transform(
    display_name="Search Phone Number [OPS]", 
    input_entity="maltego.PhoneNumber",
    description="Search OpenPeopleSearch for a Phone Number",
    settings=[],
    output_entities=["maltego.PhoneNumber", "maltego.Phrase"]
)

class ops_phone(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # Get Bearer Token
        bearer_token = request.getTransformSetting(ops_auth.id)
        url = 'https://api.openpeoplesearch.com/api/v1/Consumer/PhoneSearch'
        json_data = {
            'phoneNumber': request.getProperty("phonenumber"),
        }

        if url:
            headers = {
                'accept': '*/*',
                'Authorization': f'Bearer {bearer_token}',
                'Content-Type': 'application/json'
            }

            api_response = requests.post(url, headers=headers, json=json_data)
            if api_response.status_code == 200:
                data = api_response.json()
                results = data.get("results", [])

                for record in results:
                    RecordProcessor.process_record(record, response)

            else:
                response.addUIMessage(f"API call failed with status code {api_response.status_code}: {api_response.text}", messageType="PartialError")

        else:
            response.addUIMessage("Unsupported entity type for this transform.", messageType="FatalError")