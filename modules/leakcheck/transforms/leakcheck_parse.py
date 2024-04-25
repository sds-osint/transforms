from maltego_trx.entities import Email, Alias, Phrase, IPAddress
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from modules.leakcheck.extensions import leakcheck_registry, leakcheck_set


@leakcheck_registry.register_transform(
    display_name="", 
    input_entity="",
    description='',
    output_entities=[],
    transform_set=leakcheck_set,
    settings=[])

class leakcheck_parse(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        def get_property(request, property_name, default_value=""):
            value = request.getProperty(property_name)
            return value if value else default_value            

        password = get_property(request, 'password')
        username = get_property(request, 'username')
        email = get_property(request, 'email')
        profile_name = get_property(request, 'profile_name')
        ip = get_property(request, 'ip')

        if password != '':
            entity = response.addEntity(Phrase, password)
            entity.addProperty(fieldName='password', displayName='Password', value=password, matchingRule='strict')

        if username != '':
            entity = response.addEntity(Alias, username)
            entity.addProperty(fieldName='username', displayName='Username', value=username)

        if email != '':
            entity = response.addEntity(Email, email)
            entity.addProperty(fieldName='email_address', displayName='Email Address', value=email)

        if profile_name != '':
            entity = response.addEntity(Alias, profile_name)
            entity.addProperty(fieldName='profile_name', displayName='Profile Name', value=profile_name)

        if ip != '':
            entity = response.addEntity(IPAddress, ip)
            entity.addProperty(fieldName='ip', displayName='IP Address', value=ip, matchingRule='strict')