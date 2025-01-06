import graphviz

# Create a Function Block Diagram for Procedural Map Generation
fbd_graph = graphviz.Digraph("ProceduralMapGenerationFBD", format="png")
fbd_graph.attr(rankdir="LR", size="8,5", dpi="300")

# Add nodes for inputs, processes, and outputs
fbd_graph.node("Input1", "Player Position", shape="parallelogram")
fbd_graph.node("Input2", "Screen Dimensions", shape="parallelogram")
fbd_graph.node("Input3", "Camera Offset", shape="parallelogram")

fbd_graph.node("P1", "Load Background Tiles", shape="box")
fbd_graph.node("P2", "Calculate Visible Tiles", shape="box")
fbd_graph.node("P3", "Select Tile Index", shape="box")
fbd_graph.node("P4", "Update Tile Grid", shape="box")
fbd_graph.node("P5", "Render Tiles", shape="box")

fbd_graph.node("Output1", "Rendered Map Tiles", shape="parallelogram")

# Connect inputs to processes
fbd_graph.edge("Input1", "P2", "Player Position")
fbd_graph.edge("Input2", "P2", "Screen Dimensions")
fbd_graph.edge("Input3", "P2", "Camera Offset")

# Connect processes to each other
fbd_graph.edge("P1", "P2", "Loaded Tiles")
fbd_graph.edge("P2", "P3", "Visible Tile Coordinates")
fbd_graph.edge("P3", "P4", "Tile Index")
fbd_graph.edge("P4", "P5", "Updated Tile Grid")

# Connect the final process to output
fbd_graph.edge("P5", "Output1", "Rendered Map Tiles")

# Render the graph to a file and display it
file_path = "/mnt/data/ProceduralMapGenerationFBD"
fbd_graph.render(file_path)
file_path + ".png"
