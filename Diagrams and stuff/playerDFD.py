import graphviz

# Recreate the Level 2 DFD for Player Actions with Health Manager replacing Handle Death
dfd_graph = graphviz.Digraph("Level2DFD_PlayerActions", format="png")
dfd_graph.attr(rankdir="LR", size="8,5", dpi="300")

# Add nodes for sub-processes, external entities, and data stores
dfd_graph.node("PA1", "Handle Movement\n(Stand, Walk)", shape="ellipse")
dfd_graph.node("PA2", "Handle Combat\n(Attack)", shape="ellipse")
dfd_graph.node("PA3", "Handle Item Use\n(Use Item, Despawn Item)", shape="ellipse")
dfd_graph.node("PA4", "Handle Level-Up\n(Level-Up, Trigger Upgrade)", shape="ellipse")
dfd_graph.node("HM", "Health Manager\n(Damage, Heal, Check Death)", shape="ellipse")

dfd_graph.node("E1", "Player", shape="box")
dfd_graph.node("D1", "Game State", shape="cylinder")
dfd_graph.node("P1", "Progression System", shape="ellipse")
dfd_graph.node("P2", "Enemy Actions", shape="ellipse")
dfd_graph.node("P3", "Item Management", shape="ellipse")
dfd_graph.node("P4", "Game Over", shape="ellipse")

# Connect entities to sub-processes
dfd_graph.edge("E1", "PA1", "Movement Commands")
dfd_graph.edge("E1", "PA2", "Attack Command")
dfd_graph.edge("E1", "PA3", "Use Item Command")

# Connect sub-processes to data stores
dfd_graph.edge("PA1", "D1", "Update Position")
dfd_graph.edge("PA3", "D1", "Update Health/XP")

# Connect sub-processes to other processes
dfd_graph.edge("PA2", "P2", "Send Attack Details")
dfd_graph.edge("PA3", "P3", "Trigger Item Despawn")
dfd_graph.edge("PA4", "P1", "Trigger Upgrade and Horde Spawn")

# Connect to Health Manager
dfd_graph.edge("PA2", "HM", "Deal Damage")
dfd_graph.edge("PA3", "HM", "Heal Player")
dfd_graph.edge("HM", "D1", "Update Health")
dfd_graph.edge("HM", "P4", "Trigger Game Over (If Dead)")

# Connect data stores and processes back to sub-processes if needed
dfd_graph.edge("D1", "PA1", "Retrieve Position Data")
dfd_graph.edge("D1", "PA3", "Retrieve Item Info")
dfd_graph.edge("D1", "PA4", "Check XP for Level-Up")

# Render the graph to a file and display it
file_path = "/mnt/data/Level2DFD_PlayerActions_HealthManager"
dfd_graph.render(file_path)
file_path + ".png"

