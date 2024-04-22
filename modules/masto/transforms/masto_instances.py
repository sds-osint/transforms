from maltego_trx.entities import Domain
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import json
import requests
from w3lib.html import remove_tags
from modules.masto.extensions import masto_registry, masto_set

@masto_registry.register_transform(
    display_name="Get information about a Mastodon instance", 
    input_entity="maltego.Domain",
    description='Adds information is a Mastodon instance entity',
    output_entities=["maltego.Domain"],
    transform_set=masto_set)


class masto_instances(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        instance_address = request.Value

        headers = {
            "Accept": "text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US;q=0.9,en;q=0,8",
            "accept-encoding": "gzip, deflate",
            "user-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) "
            "Chrome/104.0.0.0 Safari/537.36",
        }

        inst_url = f"https://{instance_address}/api/v1/instance"

        try:
            data_response = requests.request("GET", inst_url, headers=headers)
            inst_data = json.loads(data_response.text)
        
        except Exception as e:
            inst_data = {}

        if not inst_data:
            response.addUIMessage(f"\nMastodon instance [{instance_address}] NOT found!")

        name = inst_data["uri"]
        title = inst_data["title"]
        s_description = inst_data["short_description"]
        s_description = remove_tags(s_description)
        det_descript = inst_data["description"]
        det_descript = remove_tags(det_descript)
        e_mail = inst_data["email"]
        thumb = inst_data["thumbnail"]
        lang = inst_data["languages"]
        reg = inst_data["registrations"]
        reg_approve = inst_data["approval_required"]
        admin_data = inst_data["contact_account"]

        entity = response.addEntity(Domain, instance_address)

        for key, value in inst_data.items():
            entity.addProperty(fieldName=key, displayName=key, value=value)

        # for key in [
        #     "id",
        #     "username",
        #     "acct",
        #     "display_name",
        #     "followers_count",
        #     "following_count",
        #     "statuses_count",
        #     "last_status_at",
        #     "locked",
        #     "bot",
        #     "discoverable",
        #     "group",
        #     "created_at",
        #     "url",
        #     "avatar",
        #     "header",
        # ]:
        #     entity.addProperty(key, admin_data[key])
