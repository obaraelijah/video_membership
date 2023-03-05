from algoliasearch.search_client import SearchClient

from app import config


settings = config.get_settings()

ALGOLIA_APP_ID = settings.algoria_app_id
ALGOLIA_API_KEY = settings.algoria_api_key
ALGOLIA_INDEX_NAME = settings.algoria_index_name


def get_index(name=ALGOLIA_INDEX_NAME):
    client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
    index = client.init_index(name)
    return index

def update_index():
    index = get_index()
    #
    return

def search_index(query):
    index = get_index()
    return index.search(query)