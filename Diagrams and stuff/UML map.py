import graphviz

# Simplify and correct the UML class diagram labels
uml = graphviz.Digraph("UML_ProceduralMapGeneration", format="png")
uml.attr(rankdir="TB", size="8,5", dpi="300")

# Add WorldMap class with corrected formatting
uml.node("WorldMap", '''{
    WorldMap|
    - tile_width: int\\l
    - tile_height: int\\l
    - background_tiles: List[Image]\\l
    - tile_grid: Dict[Tuple[int, int], int]\\l
    |
    + __init__(tile_width, tile_height)\\l
    + load_background_tiles()\\l
    + select_tile_index()\\l
    + get_background_tiles(target_rect, screen_width, screen_height)\\l
    + render(screen, tiles, camera_offset)\\l
}''', shape="record")

# Add Static_variables class with corrected formatting
uml.node("Static_variables", '''{
    Static_variables|
    - TOTAL_BG: int\\l
    - BG_CHANCE: List[int]\\l
}''', shape="record")

# Add pygame module with corrected formatting
uml.node("pygame", '''{
    pygame|
    + image.load(file)\\l
    + transform.scale(image, size)\\l
}''', shape="record")

# Add relationships
uml.edge("WorldMap", "Static_variables", "Uses", arrowhead="vee")
uml.edge("WorldMap", "pygame", "Uses", arrowhead="vee")

# Render the UML diagram
file_path = "/mnt/data/UML_ProceduralMapGeneration_Simplified"
uml.render(file_path)
file_path + ".png"
