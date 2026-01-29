from mcp.server.fastmcp import FastMCP
from . import fetch_info
from .main import open_video as main_open_video

mcp = FastMCP("Anime From Terminal", 
              json_response=True,
              host="0.0.0.0",
              port=6969)

@mcp.resource("fetch://search/{search_query}")
def get_search_results(search_query: str) -> list:
    """
    Searches for anime that matches the search_query. This may return a lot of results so please use your best judgement to filter out the results.
    """
    return fetch_info.get_all_search_results(search_query)

@mcp.resource("fetch://anime/{anime_id}")
def get_episodes(anime_id: str) -> dict:
    """
    Gets the list of episodes given an anime_id (can be found via search)
    """
    return fetch_info.get_episodes(anime_id)

@mcp.resource("fetch://anime/episode/{episode_id}")
def get_servers(episode_id: str) -> dict:
    """
    Gets the server names given the episode id.
    """
    return fetch_info.get_servers(episode_id)

@mcp.resource("fetch://{episode_id}/{server_type}/{server_name}")
def get_stream(episode_id: str, server_name: str, server_type: str):
    """
    Gets the stream given the episode id, server type (sub or dub) and server name (HD-1, HD-2, etc).
    """
    return fetch_info.get_stream(episode_id=episode_id,
                                 server_name=server_name,
                                 server_type=server_type
                                 )

@mcp.tool()
def open_video(video:dict) -> None:
    """
    Opens the video using mpv while handling all the subtitles and referrer.
    
    Args:
        video: a video dictionary containing the stream, the referrer, and the subtitles

    Return:
        None
    """
    main_open_video(video)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
