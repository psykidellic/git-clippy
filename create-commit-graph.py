from itertools import combinations

import networkx as nx
from git import Repo


def file_assoc_iter(repo_path, branch='master'):
    repo = Repo(repo_path)
    for commit in repo.iter_commits(branch):
        for comb in combinations(commit.stats.files.keys(), 2):
            yield comb

