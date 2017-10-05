from itertools import combinations, islice

from clize import run
from git import Repo
import networkx as nx


def file_assoc_iter(repo_path, branch='master'):
    repo = Repo(repo_path)
    for commit in repo.iter_commits(branch):
        for comb in combinations(commit.stats.files.keys(), 2):
            yield comb


def update_graph(assoc_iter, g=None):
    g = g or nx.Graph()
    for f1, f2 in assoc_iter:
        if g.has_edge(f1, f2):
            g[f1][f2]['weight'] += 1
        else:
            g.add_weighted_edges_from([(f1, f2, 1)])

    return g


def main(repo_path, *, graph_filename='./g.pkl', branch='master', limit=-1):
    if limit <= 0:
        limit = None

    assoc_iter = islice(file_assoc_iter(repo_path, branch), limit)
    graph = update_graph(assoc_iter)
    nx.write_gpickle(graph, graph_filename)


if __name__ == "__main__":
    run(main)

