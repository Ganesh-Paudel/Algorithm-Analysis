import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

stats_df = pd.read_csv('performance.csv')
path_df = pd.read_csv('data/testCases.csv') 

fig, ax1 = plt.subplots(figsize=(15, 10))

ax1.set_xlabel('Run Number')
ax1.set_ylabel('Total Time (s)', color='tab:blue')
ax1.bar(stats_df.index, stats_df['Total Time'], color='tab:blue', alpha=0.6, label='Time')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Nodes Explored', color='tab:red')
ax2.plot(stats_df.index, stats_df['Nodes Explored'], color='tab:red', marker='o', label='Nodes')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.title('Performance: Time vs Nodes Explored')
plt.savefig('performance_chart.png')
plt.close()

plt.figure(figsize=(8, 6))
G = nx.from_pandas_edgelist(path_df, source='source', target='target')

pos = nx.spring_layout(G) 
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', 
        node_size=800, font_size=8, font_weight='bold', arrows=True)

plt.title('Path Visualization (Source -> Target)')
plt.savefig('path_visualization.png')
plt.close()

print("Visualizations saved as 'performance_chart.png' and 'path_visualization.png'")
