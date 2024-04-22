from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.entities import Location, Person, Email, PhoneNumber, Company, Phrase
from extensions import openpeoplesearch_registry
from settings import ops_auth, city_input, state_input
import requests

@openpeoplesearch_registry.register_transform(
    display_name="", 
    input_entity="",
    description='',
    settings=[],
    output_entities=[] 
)

class openpeoplesearch(DiscoverableTransform):
    """
    Returns search records from OpenPeopleSearch using the name.
    """ 
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # Get Bearer Token
        bearer_token = request.getTransformSetting(ops_auth.id)
        json_data = {}
        url = ''

        # Get entity type for search
        entityType = str(request.Type)

        if entityType == 'maltego.Location': 
            url = 'https://api.openpeoplesearch.com/api/v1/Consumer/AddressSearch'
            json_data = {
                'address': request.getProperty("properties.street_address"),
                'city': request.getProperty("city"),
                'state': request.getProperty("location.area")
            }

        elif entityType == 'maltego.Person':
            url = 'https://api.openpeoplesearch.com/api/v1/Consumer/NameSearch'
            json_data = {
                "firstName": request.getProperty("person.firstnames"),
                "lastName": request.getProperty("person.lastname"),
                "city": request.getTransformSetting(city_input.id),
                "state": request.getTransformSetting(state_input.id)
            }

        elif entityType == 'maltego.PhoneNumber':
            url = 'https://api.openpeoplesearch.com/api/v1/Consumer/PhoneSearch'
            json_data = {
                'phoneNumber': request.getProperty("properties.phonenumber"),
            }

        elif entityType == 'maltego.Email':
            url = 'https://api.openpeoplesearch.com/api/v1/Consumer/EmailAddressSearch'
            json_data = {
                'emailAddress': request.getProperty("properties.email"),
            }

        elif entityType == 'maltego.Company':
            url = 'https://api.openpeoplesearch.com/api/v1/Consumer/BusinessSearch'
            json_data = {
                "businessName": request.getProperty("properties.title"),
                "city": request.getTransformSetting(city_input.id),
                "state": request.getTransformSetting(state_input.id)
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
                    cls.process_record(record, response, entityType)

            else:
                response.addUIMessage(f"API call failed with status code {api_response.status_code}: {api_response.text}", messageType="PartialError")
        else:
            response.addUIMessage("Unsupported entity type for this transform.", messageType="FatalError")

    @staticmethod
    def process_record(record, response, entityType):
        reportedDate = record.get("reportedDate", "")
        firstName = record.get("firstName", "")
        middleName = record.get("middleName", "")
        lastName = record.get("lastName", "")
        address = record.get("address", "")
        city = record.get("city", "")
        state = record.get("state", "")
        zipCode = record.get("zip", "")
        email_address = record.get("email", "")
        phone_number = record.get("phone", "")
        lineType = record.get("lineType", "")
        dob = record.get("dob", "")
        occupation = record.get("occupation", "")
        employer = record.get("employer", "")
        associatedDomain = record.get("associatedDomain", "")
        dataTypeName = record.get("dataTypeName", "")
        dataCategoryName = record.get("dataCategoryName", "")
        webVerificationLink = record.get("webVerificationLink", "")
        vol = record.get("vol", "")
        recordId = record.get("recordId", "")

        if entityType == 'maltego.Location': 
            entity = response.addEntity(Location, address)

        elif entityType == 'maltego.Person':
            entity = response.addEntity(Person, firstName + " " + lastName)

        elif entityType == 'maltego.PhoneNumber':
            entity = response.addEntity(PhoneNumber, phone_number)

        elif entityType == 'maltego.Email':
            entity = response.addEntity(Email, email_address)

        elif entityType == 'maltego.Company':
            entity = response.addEntity(Company, record.get("businessName", ""))

        # Add properties
        ## Add personal data
        entity.addProperty(fieldName="firstName", displayName="First Name", value=firstName)
        entity.addProperty(fieldName="middleName", displayName="Middle Name", value=middleName)
        entity.addProperty(fieldName="lastName", displayName="Last Name", value=lastName)
        entity.addProperty(fieldName="dob", displayName="Date of Birth", value=dob)

        ## Add selectors
        entity.addProperty(fieldName='email', displayName='Email Address', value=email_address)
        entity.addProperty(fieldName='phone', displayName='Phone Number', value=phone_number)
        entity.addProperty(fieldName='linetype', displayName='Line Type', value=lineType)

        ## Add location
        entity.addProperty(fieldName="address", displayName="Address", value=address)
        entity.addProperty(fieldName="city", displayName="City", value=city)
        entity.addProperty(fieldName="state", displayName="State", value=state)
        entity.addProperty(fieldName="zipcode", displayName="Zip Code", value=zipCode)        

        ## Add employment
        entity.addProperty(fieldName="occupation", displayName="Occupation", value=occupation)
        entity.addProperty(fieldName="employer", displayName="Employer", value=employer)

        ## Add record metadata
        entity.addProperty(fieldName="record_id", displayName="OPS Record ID", value=recordId, matchingRule='strict')
        entity.addProperty(fieldName="reportedDate", displayName="Reported Date", value=reportedDate)
        entity.addProperty(fieldName='associated_domain', displayName='Associated Domain', value=associatedDomain)
        entity.addProperty(fieldName='data_type_name', displayName='Data Type', value=dataTypeName)
        entity.addProperty(fieldName='data_category_name', displayName='Data Category', value=dataCategoryName)
        entity.addProperty(fieldName='web_verification_link', displayName='Verification Link', value=webVerificationLink)
        entity.addProperty(fieldName='vol', displayName='Vol', value=vol)