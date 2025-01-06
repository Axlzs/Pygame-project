import graphviz

# Create a Graphviz Digraph for the Level 2 DFD for Map Generation
dfd_graph = graphviz.Digraph("Level2DFD_MapGeneration", format="png")
dfd_graph.attr(rankdir="LR", size="8,5", dpi="300")

# Add nodes for sub-processes, external entities, and data stores
dfd_graph.node("MG1", "Seed Generation\n(Random Seed or Predefined)", shape="ellipse")
dfd_graph.node("MG2", "Generate Layout\n(Tiles, Obstacles, Pathways)", shape="ellipse")
dfd_graph.node("MG3", "Render Map\n(Visual Representation)", shape="ellipse")

dfd_graph.node("E1", "System Environment", shape="box")
dfd_graph.node("E2", "Player", shape="box")

dfd_graph.node("D1", "Map Data", shape="cylinder")
dfd_graph.node("D2", "Configuration Settings", shape="cylinder")

# Connect entities to sub-processes
dfd_graph.edge("E1", "MG1", "Provides Platform Details")
dfd_graph.edge("E2", "MG1", "Provides Game Start Trigger")

# Connect sub-processes to data stores
dfd_graph.edge("MG1", "D1", "Save Generated Seed")
dfd_graph.edge("MG2", "D1", "Save Layout Data")
dfd_graph.edge("MG3", "D1", "Read Layout Data")

# Connect data stores back to processes
dfd_graph.edge("D2", "MG1", "Retrieve Configurations")
dfd_graph.edge("D1", "MG3", "Retrieve Map Data")

# Connect sub-processes to each other
dfd_graph.edge("MG1", "MG2", "Provide Seed")
dfd_graph.edge("MG2", "MG3", "Provide Layout Details")

# Render the graph to a file and display it
file_path = "/mnt/data/Level2DFD_MapGeneration"
dfd_graph.render(file_path)
file_path + ".png"
