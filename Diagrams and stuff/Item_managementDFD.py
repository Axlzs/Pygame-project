import graphviz

# Create a Graphviz Digraph for the Item Management DFD
dfd_item_management = graphviz.Digraph("ItemManagementDFD", format="png")
dfd_item_management.attr(rankdir="LR", size="8,5", dpi="300")

# Add nodes for processes, external entities, and data stores
dfd_item_management.node("P1", "Spawn Item", shape="ellipse")
dfd_item_management.node("P2", "Grant Item Effect", shape="ellipse")

dfd_item_management.node("E1", "Enemy Actions", shape="box")
dfd_item_management.node("E2", "Player", shape="box")

dfd_item_management.node("D1", "Game State", shape="cylinder")

# Connect entities to processes
dfd_item_management.edge("E1", "P1", "Enemy Death Trigger")
dfd_item_management.edge("E2", "P2", "Player Interaction")

# Connect processes to data stores
dfd_item_management.edge("P1", "D1", "Add Item to Game World")
dfd_item_management.edge("P2", "D1", "Update Player Stats")
dfd_item_management.edge("P2", "D1", "Remove Item from Game World")

# Connect processes to each other
dfd_item_management.edge("P1", "P2", "Item Exists in Game World")

# Render the graph to a file and display it
dfd_item_management.render("/mnt/data/ItemManagementDFD")
"/mnt/data/ItemManagementDFD.png"
