import graphviz

# Create the Level 2 DFD for Enemy Actions
dfd_graph = graphviz.Digraph("Level2DFD_EnemyActions_Updated", format="png")
dfd_graph.attr(rankdir="LR", size="8,5", dpi="300")

# Add nodes for sub-processes, external entities, and data stores
dfd_graph.node("EA1", "Handle Movement\n(Patrol, Chase)", shape="ellipse")
dfd_graph.node("EA2", "Handle Combat\n(Attack Player)", shape="ellipse")
dfd_graph.node("HM", "Health Manager\n(Update Health, Check Death)", shape="ellipse")
dfd_graph.node("DI", "Drop Item\n(Item Decision)", shape="ellipse")

dfd_graph.node("D1", "Game State", shape="cylinder")
dfd_graph.node("P1", "Player Actions", shape="ellipse")
dfd_graph.node("P2", "Item Management", shape="ellipse")
dfd_graph.node("P3", "Progression System", shape="ellipse")

# Connect sub-processes to data stores
dfd_graph.edge("EA1", "D1", "Update Position")
dfd_graph.edge("EA2", "D1", "Update Enemy Attack")
dfd_graph.edge("DI", "D1", "Update Item Drops")

# Connect sub-processes to other processes
dfd_graph.edge("EA1", "P1", "Retrieve Player Location")
dfd_graph.edge("EA2", "P1", "Send Attack Details")
dfd_graph.edge("DI", "P2", "Trigger Item Drop")
dfd_graph.edge("P3", "EA1", "Upgrade Enemy Attributes")
dfd_graph.edge("P3", "EA2", "Upgrade Enemy Attributes")

# Connect to Health Manager
dfd_graph.edge("P1", "HM", "Damage Enemy")
dfd_graph.edge("HM", "D1", "Update Health")
dfd_graph.edge("HM", "DI", "Trigger Item Drop (If Dead)")

# Connect data stores and processes back to sub-processes
dfd_graph.edge("D1", "EA1", "Retrieve Enemy Position")
dfd_graph.edge("D1", "EA2", "Retrieve Enemy Stats")

# Render the graph to a file and display it
file_path = "/mnt/data/Level2DFD_EnemyActions_Updated"
dfd_graph.render(file_path)
file_path + ".png"
