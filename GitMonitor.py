import Database
import Github
import time
from Utils import *

init_repos = []

def build_msg(repos):
    #json格式化发送的数据信息
    local_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    msgs = []
    if len(repos) == 0:
        return []
    res = f"# GitHub情报{len(repos)}条 {formatted_time}\n"
    msgs.append((res,[]))

    res = ''
    i = 0
    tmp_repos = []
    while i < len(repos):
        repo: Repo = repos[i]
        tmp_res = f"{res}\n{i+1}. {str(repo)}\n"
        if (len(tmp_res) > 4096):
            msgs.append((res,tmp_repos))
            res = ''
            tmp_repos = []
        else:
            res = tmp_res
            tmp_repos.append(repo)
            i += 1
    msgs.append((res,tmp_repos))

    local_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    res = f'  END {formatted_time}'

    msgs.append((res,[]))

    return msgs

def main():
    init_repos = Database.get_repos()
    for keyword in Config.KEYWORDS:
        repos = Github.get_keyword_repos(keyword)
        new_repos = []
        for repo in repos:
            if repo not in init_repos[keyword]:
                new_repos.append(repo)
        msgs = build_msg(new_repos)
        for msg, repos in msgs:
            resp = WXWork(msg)
            if resp.get('errcode') == 0:
                for repo in repos:
                    Database.insert_repo(repo)
                print("发送成功")
            else:    
                print("发送失败")
                print(resp)

if __name__ == '__main__':
    main()
