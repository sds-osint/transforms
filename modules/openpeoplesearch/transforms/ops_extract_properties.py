from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_DEBUG
from maltego_trx.entities import Location, Person, Email, PhoneNumber, Company, Phrase
from extensions import openpeoplesearch_registry

@openpeoplesearch_registry.register_transform(
    display_name="Extract Results from Properties [OPS]", 
    input_entity="",
    description="Extract Results from Properties",
    settings=[],
    output_entities=["maltego.PhoneNumber", "maltego.Email", "maltego.Person", "maltego.Location", "maltego.Company"]
)

class ops_extract_properties(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):

        def get_property(request, property_name, default_value=""):
            value = request.getProperty(property_name)
            return value if value else default_value     
        
        phonenumber = get_property(request, 'phonenumber')
        lineType = get_property(request, 'linetype')
        streetaddress = get_property(request, 'streetaddress')
        city = get_property(request, 'city')
        state = get_property(request, 'state')
        zipcode = get_property(request, 'zipcode')
        email = get_property(request, 'email')
        occupation = get_property(request, 'occupation')
        employer = get_property(request, 'employer')

        if phonenumber != '':
            entity = response.addEntity(PhoneNumber, phonenumber)
            entity.addProperty(fieldName='phone', displayName='Phone Number', value=phonenumber)
            entity.addProperty(fieldName='linetype', displayName='Line Type', value=lineType)

        if email != '':
            entity = response.addEntity(Email, email)
            entity.addProperty(fieldName='email', displayName='Email Address', value=email)

        #if any((streetaddress, city, state, zipcode)):
        if streetaddress != '':
            # full_address = f'{streetaddress}, {city}, {state} {zipcode}'
            # entity = response.addEntity(Location, full_address)
            entity = response.addEntity(Location, streetaddress)
            entity.addProperty(fieldName="streetaddress", displayName="Address", value=streetaddress)
            entity.addProperty(fieldName="city", displayName="City", value=city)
            entity.addProperty(fieldName="location.area", displayName="State", value=state)
            entity.addProperty(fieldName="zipcode", displayName="Zip Code", value=zipcode)   

        if any ((occupation, employer)):
            entity = response.addEntity(Company, employer)
            entity.addProperty(fieldName="occupation", displayName="Occupation", value=occupation)
            entity.addProperty(fieldName="employer", displayName="Employer", value=employer)
