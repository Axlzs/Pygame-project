import graphviz

# Create a Graphviz Digraph for the Level 2 DFD: Progression System
dfd_graph = graphviz.Digraph("Level2DFD_ProgressionSystem", format="png")
dfd_graph.attr(rankdir="LR", size="8,5", dpi="300")

# Add nodes for sub-processes, external entities, and data stores
dfd_graph.node("PS1", "Upgrade Player Stats\n(Health, Attack, Speed)", shape="ellipse")
dfd_graph.node("PS2", "Upgrade Enemy Stats\n(Health, Attack, Speed)", shape="ellipse")
dfd_graph.node("PS3", "Trigger Horde Spawn", shape="ellipse")
dfd_graph.node("PS4", "Manage Spawn Cap\nand Spawn Rate", shape="ellipse")

dfd_graph.node("E1", "Player", shape="box")
dfd_graph.node("E2", "System Environment", shape="box")
dfd_graph.node("D1", "Game State", shape="cylinder")
dfd_graph.node("D2", "Configuration Settings", shape="cylinder")

# Connect entities to sub-processes
dfd_graph.edge("E1", "PS1", "Select Upgrade")
dfd_graph.edge("E2", "PS4", "Provide Environment Info")

# Connect sub-processes to data stores
dfd_graph.edge("PS1", "D1", "Update Player Stats")
dfd_graph.edge("PS2", "D1", "Update Enemy Stats")
dfd_graph.edge("PS3", "D1", "Trigger Horde Details")
dfd_graph.edge("PS4", "D1", "Update Spawn Data")

# Inter-process connections
dfd_graph.edge("PS1", "PS2", "Balance Difficulty")
dfd_graph.edge("PS2", "PS3", "Provide Enemy Strength")
dfd_graph.edge("PS3", "PS4", "Set Spawn Rate/Cap")

# Data feedback
dfd_graph.edge("D1", "PS1", "Retrieve Player Level")
dfd_graph.edge("D1", "PS2", "Retrieve Enemy Stats")
dfd_graph.edge("D1", "PS4", "Retrieve Spawn Data")
dfd_graph.edge("D2", "PS4", "Retrieve Settings")

# Render the graph to a file and display it
file_path = "/mnt/data/Level2DFD_ProgressionSystem"
dfd_graph.render(file_path)
file_path + ".png"
