import requests
import Config
from Utils import Repo

def get_keyword_repos(keyword):
    github_api = "https://api.github.com/search/repositories?q="+keyword+"&sort=updated"
    response = requests.get(
        github_api, 
        headers=Config.HEADERS,
        proxies=Config.PROXY,
        timeout=Config.TIMEOUT,
        verify=False
    )
    if response.status_code != 200:
        return []
    json_res = response.json()
    iterms = json_res.get('items')
    repos = []
    for iter in iterms:
        repo = Repo(
            iter.get('full_name'),
            iter.get('html_url'),
            iter.get('description'),
            keyword
        )
        repos.append(repo)
    return repos