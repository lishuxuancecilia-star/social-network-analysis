import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 1. 读取 CSV 文件
file_path = "CommentDataset.csv"
df = pd.read_csv(file_path)

df = df[['Your Class ID', 'Target Class ID']].copy()
df.columns = ['from', 'to']

# 数据清洗：转为字符串并去除空格
df['from'] = df['from'].astype(str).str.strip()
df['to'] = df['to'].astype(str).str.strip()

# 2. 使用 NetworkX 构建有向图 G (Task 1 & 2)
G = nx.DiGraph()
# 每个 directed edge 代表一个 “comment-to” 关系
G.add_edges_from(zip(df['from'], df['to']))

# 3. 设置你自己的节点 ID (请将 "58" 修改为你实际的学号)
your_node = "58"

# 4. 打印要求的四个值 (Task 2)
if your_node not in G.nodes():
    print(f"Error: Node {your_node} not found in the dataset. Please check your ID.")
else:
    # 按照 PPT 要求的格式输出
    print("In-degree:", G.in_degree(your_node))
    print("Out-degree:", G.out_degree(your_node))

    # 计算中心度
    closeness = nx.closeness_centrality(G)
    betweenness = nx.betweenness_centrality(G)

    print("Closeness Centrality:", closeness.get(your_node))
    print("Betweenness Centrality:", betweenness.get(your_node))

plt.figure(figsize=(20, 20))

pos = nx.circular_layout(G)

# 1️⃣ 画边（保留箭头！！）
nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,          # ✅ 保留箭头（关键）
    #arrowstyle='-|>',
    #arrowsize=10,
    #alpha=0.05,           # 淡一点，不然太乱
    width=0.3,
    edge_color="gray"
)

# 2️⃣ 所有节点
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=50,
    node_color="lightgreen"
)

# 3️⃣ 高亮你的节点（红色）
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[your_node],
    node_size=100,
    node_color="red"
)

# 4️⃣ 只标你自己
nx.draw_networkx_labels(
    G,
    pos,
    labels={your_node: your_node},
    font_size=7,
    font_color="black"
)

nx.draw_networkx_labels(G, pos, font_size=6)

# =========================
# 5️⃣ 在图上写指标
# =========================
if your_node in G.nodes():
    info_text = (
        f"Node: {your_node}\n"
        f"In-degree: {G.in_degree(your_node)}\n"
        f"Out-degree: {G.out_degree(your_node)}\n"
        f"Closeness: {closeness[your_node]:.4f}\n"
        f"Betweenness: {betweenness[your_node]:.4f}"
    )

    plt.text(
        0.02, 0.98,
        info_text,
        transform=plt.gca().transAxes,
        fontsize=14,
        verticalalignment='top',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
    )

plt.title("Circular Layout of the Class Blog Network")
plt.axis("off")

plt.show()