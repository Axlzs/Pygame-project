import graphviz

# Create a Graphviz Digraph for Game Initialization DFD
dfd_graph = graphviz.Digraph("GameInitializationDFD", format="png")
dfd_graph.attr(rankdir="LR", size="10,7", dpi="300")

# Add nodes for processes, external entities, and data stores
dfd_graph.node("GI1", "Start Game", shape="ellipse")
dfd_graph.node("GI2", "Set Up Display", shape="ellipse")
dfd_graph.node("GI3", "Show Main Menu", shape="ellipse")
dfd_graph.node("GI4", "Choose Character", shape="ellipse")

dfd_graph.node("E1", "Player", shape="box")
dfd_graph.node("E2", "System Environment", shape="box")

dfd_graph.node("D1", "Game State", shape="cylinder")
dfd_graph.node("D2", "Configuration Settings", shape="cylinder")

# Connect entities to processes
dfd_graph.edge("E1", "GI1", "Start Game Command")
dfd_graph.edge("E1", "GI3", "Input for Menu Navigation")
dfd_graph.edge("E1", "GI4", "Character Selection")
dfd_graph.edge("E2", "GI2", "Platform Details")

# Connect processes to data stores
dfd_graph.edge("GI1", "D2", "Load Configuration Settings")
dfd_graph.edge("GI4", "D1", "Save Selected Character")
dfd_graph.edge("GI2", "D2", "Update Display Settings")

# Connect processes to each other
dfd_graph.edge("GI1", "GI2", "Trigger Display Setup")
dfd_graph.edge("GI2", "GI3", "Show Main Menu")
dfd_graph.edge("GI3", "GI4", "Trigger Character Selection")

# Connect processes to external entities
dfd_graph.edge("GI2", "E1", "Display Settings Options")
dfd_graph.edge("GI3", "E1", "Display Main Menu")
dfd_graph.edge("GI4", "E1", "Confirm Selection")

# Render the graph to a file
file_path = "/mnt/data/GameInitializationDFD"
dfd_graph.render(file_path)
file_path + ".png"
