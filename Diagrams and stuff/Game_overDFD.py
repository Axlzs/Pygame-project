import graphviz

# Create a Graphviz Digraph for the Level 2 DFD: Game Over

dfd_graph = graphviz.Digraph("Level2DFD_GameOver", format="png")
dfd_graph.attr(rankdir="LR", size="8,5", dpi="300")

# Add nodes for sub-processes, external entities, and data stores
dfd_graph.node("GO1", "Handle Restart\n(Reset State, Load Map)", shape="ellipse")
dfd_graph.node("GO2", "Handle End Game\n(Return to Main Menu)", shape="ellipse")
dfd_graph.node("GO3", "Display Final Stats\n(Summary, Player Performance)", shape="ellipse")

dfd_graph.node("E1", "Player", shape="box")
dfd_graph.node("D1", "Game State", shape="cylinder")
dfd_graph.node("D2", "Player Stats", shape="cylinder")

dfd_graph.node("P1", "Game Initialization", shape="ellipse")

dfd_graph.node("UI", "User Interface", shape="parallelogram")

# Connect entities to sub-processes
dfd_graph.edge("E1", "GO1", "Select Restart Option")
dfd_graph.edge("E1", "GO2", "Select End Game Option")

dfd_graph.edge("D2", "GO3", "Retrieve Stats")

# Connect sub-processes to data stores and processes
dfd_graph.edge("GO1", "D1", "Reset Game State")
dfd_graph.edge("GO1", "P1", "Trigger Initialization")
dfd_graph.edge("GO2", "UI", "Return to Main Menu")
dfd_graph.edge("GO3", "UI", "Show Final Stats")

# Render the graph to a file and display it
file_path = "/mnt/data/Level2DFD_GameOver"
dfd_graph.render(file_path)
file_path + ".png"