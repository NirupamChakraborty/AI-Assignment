import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

log    = []
pruned = set()     

# I will view in terminal for now
# Add matplotlib soon 
# It will have 2 optns for custom and random leaf values



def build_tree(depth, branching, leaves, idx=0):
    if depth == 0:
        val = leaves[idx % len(leaves)]
        return {"val": val, "children": [], "id": idx}, idx + 1
    children = []
    for _ in range(branching):
        child, idx = build_tree(depth - 1, branching, leaves, idx)
        children.append(child)
    return {"val": None, "children": children, "id": None}, idx


def alpha_beta(node, depth, alpha, beta, is_max, path="root"):
    if not node["children"]:
        log.append(f"leaf {path} = {node['val']}")
        return node["val"]

    layer = "MAX" if is_max else "MIN"
    log.append(f"\n{'  '*depth}[{layer}] {path}  α={alpha}  β={beta}")

    if is_max:
        value = -math.inf
        for i, child in enumerate(node["children"]):
            cp = f"{path}→{i}"
            cv = alpha_beta(child, depth+1, alpha, beta, False, cp)
            value = max(value, cv)
            alpha = max(alpha, value)
            log.append(f"{'  '*depth}  ↳ child={cv}  α={alpha}  β={beta}")
            if alpha >= beta:
                for j in range(i+1, len(node["children"])):
                    pruned.add(f"{path}→{j}")
                log.append(f"{'  '*depth}  PRUNED (α≥β: {alpha}≥{beta})")
                break
    else:
        value = math.inf
        for i, child in enumerate(node["children"]):
            cp = f"{path}→{i}"
            cv = alpha_beta(child, depth+1, alpha, beta, True, cp)
            value = min(value, cv)
            beta = min(beta, value)
            log.append(f"{'  '*depth}  ↳ child={cv}  α={alpha}  β={beta}")
            if alpha >= beta:
                for j in range(i+1, len(node["children"])):
                    pruned.add(f"{path}→{j}")
                log.append(f"{'  '*depth}  PRUNED (α≥β: {alpha}≥{beta})")
                break

    node["val"] = value
    return value


def print_tree(node, tree_depth, depth_left, prefix="", is_last=True, path="root"):
    connector = "└── " if is_last else "├── "
    ptag      = "  PRUNED" if path in pruned else ""
    # current level = tree_depth - depth_left; root (level 0) is always MAX
    level  = tree_depth - depth_left
    layer  = "MAX" if level % 2 == 0 else "MIN"
    val_str = str(node["val"]) if node["val"] is not None else "?"
    label   = f"[{val_str}] (leaf){ptag}" if not node["children"] else f"[{val_str}] ({layer}){ptag}"
    print(f"{prefix}{connector}{label}  {path}")
    child_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(node["children"]):
        print_tree(child, tree_depth, depth_left-1, child_prefix,
                   i == len(node["children"])-1, f"{path}→{i}")


def build_graph(node, G, pos, tree_depth, depth_left, x=0.0, y=0.0, dx=1.0,
                path="root", ancestor_pruned=False):
    # level 0 = root = MAX; level 1 = MIN; etc.
    level   = tree_depth - depth_left
    layer   = "MAX" if level % 2 == 0 else "MIN"
    is_leaf = not node["children"]
    label   = str(node["val"]) if node["val"] is not None else "?"

    is_pruned = ancestor_pruned or (path in pruned)
    node_type = "pruned" if is_pruned else ("leaf" if is_leaf else layer)

    G.add_node(path, label=label, layer=layer, type=node_type, depth_left=depth_left)
    pos[path] = (x, y)

    n = len(node["children"])
    for i, child in enumerate(node["children"]):
        cp           = f"{path}→{i}"
        offset       = (i - (n - 1) / 2) * dx
        child_pruned = is_pruned or (cp in pruned)
        build_graph(child, G, pos, tree_depth, depth_left-1,
                    x + offset, y - 1.4, dx / n * 1.05,
                    cp, ancestor_pruned=child_pruned)
        G.add_edge(path, cp, pruned=child_pruned)


def visualize(tree, depth, branching):
    BG         = "#0F1117"
    MAX_CLR    = "#3B82F6"
    MAX_RING   = "#93C5FD"
    MIN_CLR    = "#F59E0B"
    MIN_RING   = "#FCD34D"
    LEAF_CLR   = "#10B981"
    LEAF_RING  = "#6EE7B7"
    PRUNE_CLR  = "#EF4444"
    PRUNE_RING = "#FCA5A5"
    EDGE_CLR   = "#4B5563"
    TEXT_CLR   = "#F9FAFB"

    G   = nx.DiGraph()
    pos = {}

    n_leaves = branching ** depth
    dx_root  = max(2.0, n_leaves * 0.55)
    build_graph(tree, G, pos, depth, depth, x=0, y=0, dx=dx_root)

    n_pruned = sum(1 for n in G.nodes if G.nodes[n]["type"] == "pruned")

    w = min(max(9, n_leaves * 0.6), 32)
    h = depth * 1.8 + 2.5
    fig = plt.figure(figsize=(w, h), facecolor=BG)
    ax  = fig.add_axes([0.04, 0.08, 0.92, 0.82], facecolor=BG)

    fig.text(0.5, 0.97, "Alpha–Beta Pruning",
             ha="center", va="top", fontsize=16, fontweight="bold",
             color=TEXT_CLR, fontfamily="monospace")
    fig.text(0.5, 0.93,
             f"depth={depth}  ·  branching={branching}  ·  {n_pruned} node(s) pruned",
             ha="center", va="top", fontsize=9, color="#6B7280",
             fontfamily="monospace")

    face_map = {"MAX": MAX_CLR, "MIN": MIN_CLR, "leaf": LEAF_CLR, "pruned": PRUNE_CLR}
    ring_map = {"MAX": MAX_RING, "MIN": MIN_RING, "leaf": LEAF_RING, "pruned": PRUNE_RING}

    node_list   = list(G.nodes)
    node_colors = [face_map[G.nodes[n]["type"]] for n in node_list]
    node_rings  = [ring_map[G.nodes[n]["type"]] for n in node_list]

    base_size = max(300, 1400 - depth * 120 - n_leaves * 3)
    node_sizes = []
    for n in node_list:
        dl = G.nodes[n]["depth_left"]
        node_sizes.append(max(200, base_size - (depth - dl) * 80))

    solid_edges  = [e for e in G.edges if not G.edges[e]["pruned"]]
    dashed_edges = [e for e in G.edges if     G.edges[e]["pruned"]]

    nx.draw_networkx_edges(G, pos, edgelist=solid_edges, edge_color=EDGE_CLR,
                           width=1.4, style="solid", arrows=True,
                           arrowstyle="-|>", arrowsize=14, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=dashed_edges, edge_color=PRUNE_CLR,
                           width=1.2, alpha=0.5, style=(0, (4, 3)), arrows=True,
                           arrowstyle="-|>", arrowsize=12, ax=ax)

    nx.draw_networkx_nodes(G, pos, nodelist=node_list, node_color=node_rings,
                           node_size=[s * 1.4 for s in node_sizes], alpha=0.18, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=node_list, node_color=node_colors,
                           node_size=node_sizes, linewidths=2.0,
                           edgecolors=node_rings, ax=ax)

    sym_map = {"MAX": "▲", "MIN": "▼", "leaf": "◆", "pruned": "✕"}
    font_sz = max(5, 9 - depth)
    node_labels = {n: f"{G.nodes[n]['label']}\n{sym_map[G.nodes[n]['type']]}"
                   for n in node_list}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=font_sz,
                            font_color="white", font_weight="bold",
                            font_family="monospace", ax=ax)

    legend_items = [
        mpatches.Patch(facecolor=MAX_CLR,   edgecolor=MAX_RING,   linewidth=1.5, label="MAX node  ▲"),
        mpatches.Patch(facecolor=MIN_CLR,   edgecolor=MIN_RING,   linewidth=1.5, label="MIN node  ▼"),
        mpatches.Patch(facecolor=LEAF_CLR,  edgecolor=LEAF_RING,  linewidth=1.5, label="Leaf node  ◆"),
        mpatches.Patch(facecolor=PRUNE_CLR, edgecolor=PRUNE_RING, linewidth=1.5, label="Pruned  ✕"),
    ]
    leg = ax.legend(handles=legend_items, loc="lower right", fontsize=8,
                    framealpha=0.2, facecolor="#1F2937", edgecolor="#374151",
                    labelcolor=TEXT_CLR, handlelength=1.2,
                    borderpad=0.8, labelspacing=0.5)
    leg.get_frame().set_linewidth(1.0)

    # Depth sidebar — level 0 (root) is always MAX
    ys    = sorted(set(v[1] for v in pos.values()), reverse=True)
    y_min = min(v[1] for v in pos.values())
    y_max = max(v[1] for v in pos.values())
    y_span = y_max - y_min or 1
    for level_i, y_val in enumerate(ys):
        lname = "MAX" if level_i % 2 == 0 else "MIN"
        clr   = MAX_RING if level_i % 2 == 0 else MIN_RING
        frac  = (y_val - y_min) / y_span * 0.82 + 0.08
        fig.text(0.005, frac, f"d{level_i} {lname}",
                 ha="left", va="center", fontsize=7, color=clr,
                 fontfamily="monospace", alpha=0.7)

    ax.axis("off")

    out = "alpha_beta_tree.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
    print(f"\nTree diagram saved → {out}")
    plt.show()
    plt.close()


def get_int(prompt, lo=1, hi=10):
    while True:
        try:
            v = int(input(prompt))
            if lo <= v <= hi:
                return v
            print(f"Enter a value between {lo} and {hi}.")
        except ValueError:
            print("Integers only.")

def get_leaf_values(n_leaves):
    print(f"\nEnter exactly {n_leaves} leaf values (space or comma separated):")
    while True:
        raw = input("  Values: ").replace(",", " ").split()
        try:
            vals = [int(x) for x in raw]
            if len(vals) == n_leaves:
                return vals
            print(f"Need exactly {n_leaves} values, got {len(vals)}.")
        except ValueError:
            print("  Integers only.")


if __name__ == "__main__":
    print("\nALPHA-BETA PRUNING VISUALIZER")

    depth     = get_int("Depth (levels below root, 1–6): ", 1, 6)
    branching = get_int("Branching factor (children per node, 2–5): ", 2, 5)
    n_leaves  = branching ** depth
    print(f"\nThis tree will have {n_leaves} terminal (leaf) nodes.")

    print("\n1 — Enter leaf values manually")
    print("2 — Auto-fill with random values")
    mode = input("Choice (1/2): ").strip()

    if mode == "1":
        leaves = get_leaf_values(n_leaves)
    else:
        import random
        random.seed(42)
        leaves = [random.randint(1, 10) for _ in range(n_leaves)]
        print(f"Auto-generated leaves: {leaves}")

    tree, _ = build_tree(depth, branching, leaves)
    best     = alpha_beta(tree, 0, -math.inf, math.inf, True)

    print("\nSteps")
    for line in log:
        print(line)

    print("\nTree (with pruning)")
    print_tree(tree, depth, depth)

    print(f"\nOptimal value at root = {best}")
    if pruned:
        print(f"Pruned nodes: {sorted(pruned)}")
    else:
        print("No nodes pruned.")

    visualize(tree, depth, branching)