import requests
import json

BASE_URL = "https://anime.k1mch1.space"
def get_search_results(search_query:str) -> dict:
    """
    Gets the search results from the query.

    It simply fetches the search results from the anime info api, while also handling errors.

    Args:
        search_query: simply what you'd search from the search bar.

    Returns:
        A dictionary of the search results.
    """
    return dict

def get_episodes(anime_id:str) -> dict:
    """
    Sends a GET request to the api.

    Args:
        anime_id: the id of the anime based on the api (you get get it by searching for it through `get_search_results`

    Returns:
        A dictionary of the episodes of the anime.
    """
    return dict

def get_servers(episode_id:str) -> dict:
    """
    Gets the available servers (which also specifies whether it's SUB or DUB)

    Args:
        episode_id: the id of the episode based on the api (you get get it by searching for it through `get_search_results`
    Returns:
        A dictionary of the available servers
    """

    return dict

def get_stream(episode_id:str, server:str, type:str) -> dict:
    """
    Gets the m3u8 stream and also the referrer with a list of subtitles too.

    Args:
        episode_id: the id of the episode based on the api (you get get it by searching for it through `get_search_results`
        server: the server name (sth like HD-1, HD-2, etc...)
        type: whether it's sub or dub

    Returns:
        A dictionary of the stream information
    """

    return dict

if __name__ == "__main__":
    pass
