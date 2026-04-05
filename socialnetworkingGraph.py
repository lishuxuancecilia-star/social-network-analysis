import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 读取 CSV 文件
file_path = "CommentDataset.csv"
df = pd.read_csv(file_path)

df = df[['Your Class ID', 'Target Class ID']].copy()
df.columns = ['from', 'to']

# =========================
# 数据清洗函数
# 规则：
# 1. 清洗非纯数字节点
# 2. 清洗以 1155 开头且数值 > 200 的节点
# =========================
def is_valid_node(x):
    # 空值直接删
    if pd.isna(x):
        return False

    # 统一转字符串并去空格
    x = str(x).strip()

    # 处理空字符串和 nan
    if x == "" or x.lower() == "nan":
        return False

    # 非纯数字直接删
    if not x.isdigit():
        return False

    # 以 1155 开头且数值 > 200 的节点删掉
    if x.startswith("1155") and int(x) > 200:
        return False

    return True

# 保留 from 和 to 都合法的边
df = df[df['from'].apply(is_valid_node) & df['to'].apply(is_valid_node)].copy()

# 再次统一成字符串，防止后面节点类型不一致
df['from'] = df['from'].astype(str).str.strip()
df['to'] = df['to'].astype(str).str.strip()

# 使用 NetworkX 构建有向图 G
G = nx.DiGraph()
# 每个 directed edge 代表一个 “comment-to” 关系
G.add_edges_from(zip(df['from'], df['to']))

# 3. 设置节点 ID
your_node = "58"

# 4. 打印要求的四个值
if your_node not in G.nodes():
    print(f"Error: Node {your_node} not found in the dataset. Please check your ID.")
else:

    print("In-degree:", G.in_degree(your_node))
    print("Out-degree:", G.out_degree(your_node))

    # 计算中心度
    closeness = nx.closeness_centrality(G)
    betweenness = nx.betweenness_centrality(G)

    print("Closeness Centrality:", closeness.get(your_node))
    print("Betweenness Centrality:", betweenness.get(your_node))

plt.figure(figsize=(8, 6))

pos = nx.circular_layout(G)

#画边
nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    width=0.3,
    edge_color="gray"
)

# 所有节点
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=60,
    node_color="lightgreen"
)

#高亮自己节点（红色）
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[your_node],
    node_size=100,
    node_color="red"
)

#只标自己
nx.draw_networkx_labels(
    G,
    pos,
    labels={your_node: your_node},
    font_size=4,
    font_color="black"
)

nx.draw_networkx_labels(G, pos, font_size=4)

# =========================
#在图上写指标
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
        fontsize=8,
        verticalalignment='top',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
    )

plt.title("Circular Layout of the Class Blog Network")
plt.axis("off")

plt.show()