import networkx as nx
import matplotlib.pyplot as plt

gr = nx.Graph()
dict = {
    'word1': [0.5, 0.1],
    'word2': [0.5, 0],
    'word3': [0.1, 0]
}
keys = list(dict.keys())
for key in dict:
    i = 0
    values = dict[key]
    while i < len(values):
        if keys[i] == key:
            buf = 1
        else:
            print('%s - %s: %f' % (key, keys[i], values[i]))
            gr.add_edge(key, keys[i], weight=values[i])
        i += 1
edges = [d['weight'] for (u,v,d) in gr.edges(data=True)]
pos = nx.spring_layout(gr)
nx.draw_networkx_nodes(gr, pos, node_color='gray', node_size=100)
nx.draw_networkx_edges(gr, pos, edge_color='black', width=edges)
nx.draw_networkx_labels(gr, pos, font_size=10, font_family='Arial')
plt.axis('off')
plt.show()