import networkx as nx

def recommend(commit, graph, amt=5):
    edges = [{'weight': graph[fn_1][fn_2]['weight'], 'file': fn_2} \
        for fn_1 in commit.stats.files for fn_2 in graph[fn_1]]
    edges.sort(key=lambda x: x['weight'], reverse=True)
    if len(edges) > amt:
        return [e['file'] for e in edges[:amt]]
    else:
        return [e['file'] for e in edges]
