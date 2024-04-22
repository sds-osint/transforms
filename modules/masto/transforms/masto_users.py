from maltego_trx.entities import Alias, URL
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from modules.masto.extensions import masto_registry, masto_set
import time
import json
import requests
from tqdm import tqdm
from w3lib.html import remove_tags
from bs4 import BeautifulSoup


@masto_registry.register_transform(
    display_name="Search Mastodon Users", 
    input_entity="maltego.Alias",
    description='Searches Mastodon instances for the username.',
    output_entities=["maltego.Alias"],
    transform_set=masto_set)

class masto_users(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        username = request.Value
        url = f"https://mastodon.social/api/v2/search?q={username}"
        site_response = requests.request("GET", url)
        data = json.loads(site_response.text)
        for _ in tqdm(range(10)):
            time.sleep(0.03)

        if site_response.text == ('{"accounts":[],"statuses":[],"hashtags":[]}'):
            response.addUIMessage(f"\nTarget username: [{username}] NOT found using the Mastodon API!")

        time.sleep(1)

        data = filter(
            lambda x: x.get("username").lower() == username.lower(), data["accounts"]
        )

        entity = response.addEntity(Alias, username)

        for index, intelligence in enumerate(list(data), start=1):
            identity = intelligence["id"]
            lock = intelligence["locked"]
            pro_url = intelligence["url"]
            target_username = intelligence["username"]
            account = intelligence["acct"]
            display = intelligence["display_name"]
            creation_date = intelligence["created_at"]
            bot = intelligence["bot"]
            discov = intelligence["discoverable"]
            fwers = intelligence["followers_count"]
            fwing = intelligence["following_count"]
            posts = intelligence["statuses_count"]
            laststatus = intelligence["last_status_at"]
            group = intelligence["group"]
            note = intelligence["note"]
            note = remove_tags(note)
            avatar = intelligence["avatar"]

            entity.addProperty("user ID:\033[32m\033[1m", identity)
            entity.addProperty("\033[0mprofile url:", pro_url)
            entity.addProperty("account locked:", lock)
            entity.addProperty("username:", target_username)
            entity.addProperty("\033[0maccount:\033[32m\033[1m", account)
            entity.addProperty("\033[0mdisplay Name:\033[32m\033[1m", display)
            entity.addProperty("\033[0mprofile creation date:", creation_date)
            entity.addProperty("user is a bot:", bot)
            entity.addProperty("user opted to be listed on the profile directory:", discov)
            entity.addProperty("followers:", fwers)
            entity.addProperty("following:", fwing)
            entity.addProperty("number of posts:", posts)
            entity.addProperty("user last message date:", laststatus)
            entity.addProperty("user is a group:", group)
            entity.addProperty("user bio:\033[32m\033[1m", note)

            fields = []
            for field in intelligence.get("fields", []):
                name = field.get("name")
                value = field.get("value")

                if value and "</" not in value:
                    continue

                soup = BeautifulSoup(value, "html.parser")
                a = soup.find("a")
                if a:
                    fields.append(f'--> {name}: {a.get("href")}')
                    response.addUIMessage(f"sites found :\033[32m\033[1m")

                else:
                    continue

                for field in fields:
                    response.addUIMessage(f"\t {field}")

            # response.addUIMessage("\033[0muser's avatar link:", avatar)





    # def username_search(self, username):

    #     headers = {
    #         "Accept": "text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    #         "accept-language": "en-US;q=0.9,en;q=0,8",
    #         "accept-encoding": "gzip, deflate",
    #         "user-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) "
    #         "Chrome/104.0.0.0 Safari/537.36",
    #     }

    #     response = requests.get(
    #         "https://raw.githubusercontent.com/C3n7ral051nt4g3ncy/Masto/master/fediverse_instances.json"
    #     )
    #     sites = response.json()["sites"]
    #     is_any_site_matched = False
    #     for site in sites:
    #         uri_check = site["uri_check"]
    #         site_name = site["name"]
    #         uri_check = uri_check.format(account=username)

    #         try:
    #             res = requests.get(uri_check, headers=headers)
    #             estring_pos = res.text.find(site["e_string"]) > 0

    #         except Exception as e:
    #             continue

    #         if res.status_code == 200 and estring_pos:
    #             is_any_site_matched = True
    #             # print(f"[+] Target found ✓ on: \033[32m\033[1m{site_name}\033[0m")
    #             # Add a URL to profile
    #             print(f"Profile URL: {uri_check}")

    #     if not is_any_site_matched:
    #         response.addUIMessage(f"\nTarget username: [{username}] NOT found on the Masto OSINT Tool servers database!")

    #     return is_any_site_matched


