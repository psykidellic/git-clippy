import networkx as nx

def recommend(commit, graph):
    edges = [{'weight': graph[fn_1][fn_2]['weight'], 'file': fn_2} \
        for fn_1 in commit.stats.files for fn_2 in graph[fn_1]]
    edges.sort(key=lambda x: x['weight'])
    if len(edges) > 5:
        return [e['file'] for e in edges[:5]]
    else:
        return [e['file'] for e in edges]
