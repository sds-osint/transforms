import asyncio
import logging
import sys

try:
    from mock import Mock
except ImportError:
    from unittest.mock import Mock

from maltego_trx.entities import Alias, URL
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import LINK_STYLE_DASHED, UIM_TYPES, MaltegoMsg, MaltegoTransform

import maigret
from maigret.result import QueryStatus

logging.getLogger('asyncio').setLevel(logging.WARNING)


MAIGRET_DB_FILE = 'https://raw.githubusercontent.com/soxoj/maigret/main/maigret/resources/data.json'
TOP_SITES_COUNT = 500
TIMEOUT = 10


def setup_logger(log_level, name):
    for lib in ['requests', 'urllib3']:
        logging.getLogger(lib).setLevel(logging.WARNING) # change to debug
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger


async def maigret_search(username):

    logger = setup_logger(logging.ERROR, 'maigret')
    db = maigret.MaigretDatabase().load_from_path(MAIGRET_DB_FILE)
    sites = db.ranked_sites_dict(top=TOP_SITES_COUNT)

    results = await maigret.search(username=username,
                                   site_dict=sites,
                                   timeout=TIMEOUT,
                                   logger=logger,
                                   no_progressbar=False,
                                   query_notify=None, 
                                   )
    return results


class Maigret(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        person_name = request.Value

        for site, data in Maigret.get_maigret_data(person_name).items():
            url_main = data['url_main']
            url_user = data['url_user']

            entity = response.addEntity(Alias, site)
            entity.setLinkLabel('found by username')
            entity.addDisplayInformation(content=f'{person_name} profile at {site}')
            # entity.setWeight(100)
            entity.setIconURL('https://www.google.com/s2/favicons?domain='+url_main)

            entity.addProperty('Title', 'Title', 'strict', site)
            entity.addProperty('Social Network', 'SocialNetwork', 'strict', site)

            entity.addProperty('Url', 'Url', 'strict', url_user)

    @staticmethod
    def get_maigret_data(username):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(maigret_search(username))
        finally:
            loop.close()

        res = {}
        for site, data in results.items():
            if data['status'].status != QueryStatus.CLAIMED:
                continue
            res[site] = data

        return res


if __name__ == '__main__':
    print(Maigret().get_maigret_data('soxoj'))