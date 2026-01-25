import fetch_info
import iterfzf
import json
from colorama import init, Fore, Back, Style
import re

init(autoreset=True)

def strip_ansi(text):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

def format_search_results(search_results:list) -> dict:
    """
    Formats the search results into a key that can be chosen, and all the info stored in the value.

    Args:
        search_results: a list of search results

    Return:
        A dictionary with keys that work well with `iterfzf`
    """

    # this will be displayed in the fzf interface
    get_display_info = lambda result: f"{Fore.CYAN} {result['title']} {Style.RESET_ALL} {Fore.YELLOW} ({result['id']})"

    ret_dict = dict()
    for result in search_results:
        to_display = get_display_info(result)
        # strip it because iterfzf will strip all the ansi code
        ret_dict[strip_ansi(to_display)] = result | {"display":to_display}
    return ret_dict

INPUT_PROMPT = f"""{Fore.CYAN}Watch anime from the terminal {Fore.RED}(no ads, no bullshit){Fore.CYAN}
┃
┗━❯ {Fore.YELLOW}Enter an anime: {Style.RESET_ALL}"""

def pretty_print_dict(input_dict:dict) -> None:
    """return a string represention of a depth 1 dictionary in a presentable way"""
    for k, v in input_dict.items():
        print(f"{Fore.YELLOW} {k}{Style.RESET_ALL}: {v}")

def format_episodes(episode_list:list) -> dict:
    """
    Formats the lists of episodes such that the key can be displayed in iterfzf

    Args:
        episode_list: the list in the "episodes" parameter in the response from the API
    Return:
        A dictionary of episodes with keys that can be looked up after using `iterfzf`
    """

    is_filler = lambda episode: bool(episode["is_filler"])
    ret_dict = dict()
    get_display_info = lambda episode: f"{Fore.CYAN}{episode['title']} {Fore.YELLOW}(#{episode['number']}) {Back.BLUE + Fore.RED+ Style.BRIGHT + 'filler' if is_filler(episode) else ''}{Style.RESET_ALL}"
    for episode in episodes_list:
        to_display = get_display_info(episode)
        ret_dict[strip_ansi(to_display)] = episode|{"display":to_display}
    return ret_dict

if __name__ == "__main__":
    anime_name = input(INPUT_PROMPT)
    search_results = fetch_info.get_all_search_results(anime_name)
    formatted_search_results = format_search_results(search_results)
    choice = iterfzf.iterfzf(map(lambda result: result["display"],formatted_search_results.values()),
                             ansi=True,
                             prompt="Choose anime: ")

    chosen_anime = formatted_search_results[choice]
    #
    #print(f"{Fore.MAGENTA} You've chosen: ")
    #pretty_print_dict(formatted_search_results[choice])

    # now we have the anime, we need to get episodes now
    episodes_dict = fetch_info.get_episodes(chosen_anime["id"])
    episodes_list = episodes_dict["episodes"]
    lookup_episodes_list = format_episodes(episodes_list)
    #print(lookup_episodes_list.keys())
    choice = iterfzf.iterfzf(map(lambda episode: episode["display"],
                                lookup_episodes_list.values()),
                             ansi=True,
                             prompt="Choose episodes: "
                             )
    chosen_episode = lookup_episodes_list[choice]

    print(f"{Fore.MAGENTA} You've chosen: ")
    pretty_print_dict(chosen_episode)
