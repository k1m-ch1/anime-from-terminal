import requests
import json

BASE_URL = "https://anime.k1mch1.space"
# max retries for problematic endpoints
MAX_RETRIES = 5
def get_search_results(search_query:str, page:int) -> dict:
    """
    Gets the search results from the query only on a specifc page.

    It simply fetches the search results from the anime info api, while also handling errors.

    Args:
        search_query: simply what you'd search from the search bar.
        page: the page number we're trying to reach for.

    Returns:
        A dictionary of the search results.
    """
    res = requests.get(
        f"{BASE_URL}/search",
        params={
            'q':search_query,
            'page':page
        }
    )
    return res.json()

def get_all_search_results(search_query:str) -> list:
    """
    Gets all of the search results from the query.

    It simply fetches the search results from the anime info api, while also handling errors.

    Args:
        search_query: simply what you'd search from the search bar.

    Returns:
        A dictionary of the search results.
    """
    result_list = []
    page_number = 1
    while True:
        result_dict = get_search_results(search_query, page_number)
        if "detail" in result_dict.keys():
            break
        result_list += result_dict["results"]
        page_number += 1
    return result_list

def get_episodes(anime_id:str) -> dict:
    """
    Sends a GET request to the api.

    Args:
        anime_id: the id of the anime based on the api (you get get it by searching for it through `get_search_results`

    Returns:
        A dictionary of the episodes of the anime.
    """

    res =  requests.get(
        f"{BASE_URL}/episodes/{anime_id}"
    )

    return res.json()

def get_servers(episode_id:str) -> dict:
    """
    Gets the available servers (which also specifies whether it's SUB or DUB)

    Args:
        episode_id: the id of the episode based on the api (you get get it by searching for it through `get_search_results`
    Returns:
        A dictionary of the available servers
    """

    res = requests.get(
        f"{BASE_URL}/servers/{episode_id}"
    )

    return res.json()

def get_stream(episode_id:str, server_name:str, type:str) -> dict:
    """
    Gets the m3u8 stream and also the referrer with a list of subtitles too.

    Args:
        episode_id: the id of the episode based on the api (you get get it by searching for it through `get_search_results`
        server: the server name (sth like HD-1, HD-2, etc...)
        type: whether it's sub or dub

    Returns:
        A dictionary of the stream information
    """

    # TODO this isn't quite reliable (might send an error)
    res = requests.Response()
    for _ in range(MAX_RETRIES):
        res = requests.get(
            f"{BASE_URL}/watch/{episode_id}",
            params={
                "server":server_name,
                "type":type
            }
        )
        if "detail" not in res.json():
            break

    return res.json()

if __name__ == "__main__":
    #print(get_search_results("boruto", 1))
    print(get_all_search_results("to-love-ru"))
    #ANIME_ID = "boruto-naruto-next-generations-8143"
    #EPISODE_ID = get_episodes(ANIME_ID)["episodes"][0]["id"]
    #SERVERS  = get_servers(EPISODE_ID)
    #SERVER = SERVERS["servers"]["sub"][0]
    #print(json.dumps(get_stream(EPISODE_ID, SERVER["name"], SERVER["type"]), indent=2))
