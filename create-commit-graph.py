from collections import Counter
from itertools import combinations, islice
import os

from clize import run
from pygit2 import (
    Repository,
    GIT_SORT_TIME,
    GIT_STATUS_CURRENT,
    GIT_STATUS_IGNORED
)
import networkx as nx


def find_start(repo, branch=None):
    if branch:
        start = repo.branches.get(branch).target
    else:
        start = repo.head.target

    return start


def file_assoc_iter(repo, start, end_sha=None, max_commit_size=100):
    prev = None
    for cur in repo.walk(start):
        print(cur.hex)
        print(cur.message)
        if cur.hex == end_sha:
            break

        if prev is not None:
            if len(cur.parents) > 1:
                print("Merge commit: {} parents".format(cur.parents))
                print("Merge commit message: {}".format(cur.message))
            else:
                diff = cur.tree.diff_to_tree(prev.tree)
                files = {p.delta.new_file.path for p in diff}
                if len(files) > max_commit_size:
                    print("Skipping large commit with {} files"
                          .format(len(files)))
                else:
                    print(files)
                    for comb in combinations(files, 2):
                        yield comb

        if cur.parents:
            prev, cur = cur, cur.parents[0]


def increment_edge(g, f1, f2):
    if g.has_edge(f1, f2):
        g[f1][f2]['weight'] += 1
    else:
        g.add_weighted_edges_from([(f1, f2, 1)])


def update_graph(assoc_iter, graph):
    for f1, f2 in assoc_iter:
        increment_edge(graph, f1, f2)

    return graph


def recommend(graph, files, amt):
    file_counts = Counter()
    for f1 in enumerate(files):
        for _, f, data in graph.edges_iter([f1], data=True):
            file_counts[f] += data['weight']

    return file_counts.most_common(amt)


def main(
        repo_path, *,
        branch='master',
        end_sha="",
        num_recommended=10,
        commit_limit=-1):
    if commit_limit <= 0:
        commit_limit = None

    graph_filename = os.path.join(repo_path, '.git', 'file_assoc_graph.pkl')
    sha_filename = os.path.join(repo_path, '.git', 'end_sha.txt')

    if not end_sha:
        try:
            with open(sha_filename) as sha_file:
                end_sha = sha_file.read().strip()
        except IOError:
            pass

    try:
        graph = nx.read_gpickle(graph_filename)
    except IOError:
        graph = nx.Graph()

    repo = Repository(repo_path)
    start = find_start(repo, branch)
    assoc_iter = islice(file_assoc_iter(repo, start, end_sha), commit_limit)
    graph = update_graph(assoc_iter, graph)
    nx.write_gpickle(graph, graph_filename)
    with open(sha_filename, 'w') as sha_file:
        sha_file.write(start.hex)

    changed_files = [
        filename for filename, status in repo.status().items()
        if status not in (GIT_STATUS_CURRENT, GIT_STATUS_IGNORED)
    ]
    for item, count in recommend(graph, changed_files, num_recommended):
        print("{} with co-occurence {}".format(item, count))


if __name__ == "__main__":
    run(main)

