import graphviz

# Create a Graphviz Digraph for Level 2 DFD of the Progression System
progression_dfd = graphviz.Digraph("ProgressionSystemDFD", format="png")
progression_dfd.attr(rankdir="LR", size="10,7", dpi="300")

# Add nodes for processes, entities, and data stores
progression_dfd.node("P1", "Upgrade Player Stats", shape="ellipse")
progression_dfd.node("P2", "Upgrade Enemy Stats", shape="ellipse")
progression_dfd.node("P3", "Trigger Horde Spawn", shape="ellipse")
progression_dfd.node("P4", "Manage Enemy Spawn Cap/Rate", shape="ellipse")

progression_dfd.node("E1", "Player", shape="box")
progression_dfd.node("D1", "Game State", shape="cylinder")
progression_dfd.node("D2", "Progression Rules", shape="cylinder")

# Connect entities to processes
progression_dfd.edge("E1", "P1", "Trigger Upgrade")
progression_dfd.edge("E1", "P3", "Level-Up Trigger")

# Connect processes to data stores
progression_dfd.edge("P1", "D1", "Update Player Stats")
progression_dfd.edge("P2", "D1", "Update Enemy Stats")
progression_dfd.edge("P4", "D1", "Update Spawn Data")
progression_dfd.edge("P3", "D1", "Trigger Spawn Update")
progression_dfd.edge("P4", "D1", "Adjust Spawn Cap/Rate")

# Feedback loop: Data read from Game State
progression_dfd.edge("D1", "P1", "Provide Current Stats")
progression_dfd.edge("D1", "P2", "Provide Enemy Data")
progression_dfd.edge("D1", "P3", "Provide Spawn Info")
progression_dfd.edge("D1", "P4", "Provide Spawn Cap Info")

# Processes interaction
progression_dfd.edge("P1", "P3", "Notify Horde Trigger")
progression_dfd.edge("P2", "P4", "Notify Spawn Adjustments")

# Render and save the graph
file_path = "/mnt/data/ProgressionSystemDFD"
progression_dfd.render(file_path)
file_path + ".png"
