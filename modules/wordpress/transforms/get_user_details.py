from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from extensions import wordpress_registry


@wordpress_registry.register_transform(
    display_name="Get WordPress Users Details from Properties",
    input_entity="maltego.Person",
    description="Get WordPress Users Details from Properties",
    settings=[],
    output_entities=["maltego.Phrase", "maltego.Alias", "maltego.URL"],
)

class get_user_details(DiscoverableTransform):
    """
    Gets WordPress Users using WP API.
    """
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):

        def get_property(request, property_name, default_value=""):
            value = request.getProperty(property_name)
            return value if value else default_value    
        
        user_alias = get_property(request, "slug")
        user_description = get_property(request, "description")
        author_link = get_property(request, "link")

        user_alias_entity = response.addEntity("maltego.Alias", user_alias)
        user_alias_entity.addProperty(fieldName='alias', displayName='Alias', value=user_alias)

        user_description_entity = response.addEntity("maltego.Phrase", user_description)
        user_description_entity.addProperty(fieldName='test', displayName='Description', value=user_description)

        author_link_entity = response.addEntity("maltego.URL", author_link)
        author_link_entity.addProperty(fieldName='url', displayName='Author Link', value=author_link)
