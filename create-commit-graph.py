from heapq import nlargest
from itertools import combinations, islice
from operator import itemgetter
import os

from clize import run
from pygit2 import Repository, GIT_SORT_TIME
import networkx as nx


def find_start(repo, branch=None):
    if branch:
        start = repo.branches.get(branch).target
    else:
        start = repo.head.target

    return start


def file_assoc_iter(repo, start, end_sha=None):
    for commit in repo.walk(start, GIT_SORT_TIME):
        if commit.hex == end_sha:
            break

        files = [x.name for x in commit.tree]
        for comb in combinations(files, 2):
            yield comb


def update_graph(assoc_iter, g=None):
    g = g or nx.Graph()
    for f1, f2 in assoc_iter:
        if g.has_edge(f1, f2):
            g[f1][f2]['weight'] += 1
        else:
            g.add_weighted_edges_from([(f1, f2, 1)])

    return g


# def recommend(commit, graph, amt=5):
#
#     recommended = nlargest(
#         amt,
#         ((graph.get_edge_data(f1, f2, {'weight': 0})['weight'], (f1, f2))
#          for f1, f2 in combinations(commit.stats.files.keys(), 2)),
#         key=itemgetter[0]
#     )
#
#     edges = [
#         {'weight': graph[fn_1][fn_2]['weight'], 'file': fn_2} \
#         for fn_1 in commit.stats.files for fn_2 in graph[fn_1]]
#     edges.sort(key=lambda x: x['weight'], reverse=True)
#     if len(edges) > amt:
#         return [e['file'] for e in edges[:amt]]
#     else:
#         return [e['file'] for e in edges]


def main(repo_path, *, branch='master', end_sha="", limit=-1):
    if limit <= 0:
        limit = None

    graph_filename = os.path.join(repo_path, '.git', 'file_assoc_graph.pkl')
    sha_filename = os.path.join(repo_path, '.git', 'end_sha.txt')

    if not end_sha:
        try:
            with open(sha_filename) as sha_file:
                end_sha = sha_file.read().strip()
        except IOError:
            pass

    repo = Repository(repo_path)
    start = find_start(repo, branch)
    assoc_iter = islice(file_assoc_iter(repo, start, end_sha), limit)
    graph = update_graph(assoc_iter)
    nx.write_gpickle(graph, graph_filename)
    with open(sha_filename, 'w') as sha_file:
        sha_file.write(start.hex)


if __name__ == "__main__":
    run(main)

