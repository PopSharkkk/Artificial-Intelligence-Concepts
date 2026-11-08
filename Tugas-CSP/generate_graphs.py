import matplotlib.pyplot as plt
import networkx as nx
import os

img_dir = r"C:\Users\Rinaltra\.gemini\antigravity\scratch\csp-kka-assignment\images"
os.makedirs(img_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. Graph Tugas 1
# -------------------------------------------------------------
plt.figure(figsize=(7, 5))
G1 = nx.Graph()
vars_t1 = ["Appetizer", "Beverage", "Main_Course", "Dessert"]
G1.add_nodes_from(vars_t1)
edges_t1 = [
    ("Appetizer", "Main_Course"), # Batasan Vegetarian
    ("Appetizer", "Beverage"),    # Batasan Total Biaya
    ("Beverage", "Dessert")       # Batasan Kalsium
]
G1.add_edges_from(edges_t1)

pos1 = {
    "Appetizer": (0, 1),
    "Main_Course": (0, 0),
    "Beverage": (1, 1),
    "Dessert": (1, 0)
}

nx.draw_networkx_nodes(G1, pos1, node_color='#4A90E2', node_size=3000, edgecolors='#1C3D5A', linewidths=2)
nx.draw_networkx_labels(G1, pos1, font_size=11, font_weight='bold', font_color='white', font_family='sans-serif')
nx.draw_networkx_edges(G1, pos1, width=2.5, edge_color='#2C3E50')

# Edge labels
edge_labels_1 = {
    ("Appetizer", "Main_Course"): "(i) Vegetarian",
    ("Appetizer", "Beverage"): "(ii) Biaya",
    ("Beverage", "Dessert"): "(iii) Kalsium"
}
nx.draw_networkx_edge_labels(G1, pos1, edge_labels=edge_labels_1, font_size=9, font_color='#D9534F', font_weight='bold', bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#D9534F', lw=1))

plt.title("Constraint Graph - Tugas 1 (Perancangan Menu Makanan)", fontsize=13, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(img_dir, "tugas1_constraint_graph.png"), dpi=300)
plt.close()

# -------------------------------------------------------------
# 2. Graph Tugas 2
# -------------------------------------------------------------
plt.figure(figsize=(8, 6))
G2 = nx.Graph()
vars_t2 = [
    "C1\n(8:00-9:00)",
    "C2\n(8:30-9:30)",
    "C3\n(9:00-10:00)",
    "C4\n(9:00-10:00)",
    "C5\n(9:30-10:30)"
]
G2.add_nodes_from(vars_t2)

# Edges based on time conflict:
# C1-C2, C2-C3, C2-C4, C3-C4, C3-C5, C4-C5
edges_t2 = [
    (vars_t2[0], vars_t2[1]),
    (vars_t2[1], vars_t2[2]),
    (vars_t2[1], vars_t2[3]),
    (vars_t2[2], vars_t2[3]),
    (vars_t2[2], vars_t2[4]),
    (vars_t2[3], vars_t2[4])
]
G2.add_edges_from(edges_t2)

pos2 = {
    vars_t2[0]: (0.5, 2.0),
    vars_t2[1]: (1.5, 2.0),
    vars_t2[2]: (1.0, 1.0),
    vars_t2[3]: (2.0, 1.0),
    vars_t2[4]: (1.5, 0.0)
}

nx.draw_networkx_nodes(G2, pos2, node_color='#27AE60', node_size=3200, edgecolors='#145A32', linewidths=2)
nx.draw_networkx_labels(G2, pos2, font_size=9, font_weight='bold', font_color='white', font_family='sans-serif')
nx.draw_networkx_edges(G2, pos2, width=2.5, edge_color='#34495E')

plt.title("Constraint Graph - Tugas 2 (Jadwal Kelas / Time Conflict)", fontsize=13, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(img_dir, "tugas2_constraint_graph.png"), dpi=300)
plt.close()

print("Graphs successfully generated in", img_dir)
