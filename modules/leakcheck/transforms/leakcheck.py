from maltego_trx.entities import Email, Alias, Phrase
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from settings import leakcheck_api
from modules.leakcheck.extensions import leakcheck_registry, leakcheck_set
import requests


@leakcheck_registry.register_transform(
    display_name="", 
    input_entity="",
    description='',
    output_entities=[],
    transform_set=leakcheck_set,
    settings=[])

class leakcheck(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        target = request.Value
        api_key = request.getTransformSetting(leakcheck_api.id)
        url = f'https://leakcheck.io/api/v2/query/{target}'
        headers = {
                "Accept": "application/json",
                "X-API-Key": f"{api_key}"
            }
        
        api_response = requests.get(url, headers=headers)
        response.addUIMessage(f'Request object: {request}. Request properties: {request.Properties}')
        if api_response.status_code == 200:
            data = api_response.json()

            if data.get('success') and data.get('found', 0) > 0:
                found_count = data["found"]
                quota_count = data["quota"]    
                response.addUIMessage(f'{found_count} results found. {quota_count} searches remaining.\n')

                for record in data.get('result', []):
                    source_info = record.get('source', {})
                    breach_info = f"{source_info.get('name', 'Unknown Source')}"
                    entity = response.addEntity(Phrase, breach_info)
                    
                    for key, value in record.items():
                        if key != 'fields' and key != 'source':  # Skip 'fields' as it is a list
                            entity.addProperty(fieldName=key, displayName=key, value=str(value), matchingRule='strict')
                            
                    for source_key, source_value in source_info.items():
                        entity.addProperty(fieldName=source_key, displayName=source_key, value=str(source_value))

            else:
                response.addUIMessage("No results found or error in response.")

        else: 
            error_info = api_response.json()
            error_message = error_info.get('error', 'Unknown error')
            response.addUIMessage(f"API Error: {api_response.status_code} - {error_message}")