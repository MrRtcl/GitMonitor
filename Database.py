import sqlite3
import Config
from Utils import Repo


db = sqlite3.connect('data.db')
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS repos (
        id INTEGER PRIMARY KEY,
        name TEXT,
        url TEXT UNIQUE,
        description TEXT,
        keyword TEXT
    )
''')
db.commit()


def insert_repo(repo: Repo):
    try:
        cursor.execute('''
            INSERT INTO repos (name, url, description, keyword)
            VALUES (?, ?, ?, ?)
        ''', (repo.name, repo.url, repo.description, repo.keyword))
        db.commit()
    except sqlite3.IntegrityError:
        pass

def get_reops_by_keyword(keyword):
    cursor.execute('''
        SELECT name, url, description, keyword FROM repos WHERE keyword = ?
    ''', (keyword,))
    return [Repo(*row) for row in cursor.fetchall()]

def get_repos():
    repos = {}
    for keyword in Config.KEYWORDS + ['default']:
        repos[keyword] = get_reops_by_keyword(keyword)
    return repos
