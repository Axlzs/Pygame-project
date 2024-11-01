def load_background_tiles():
    """
    Loads and scales all background tile images from the 'images' directory.
    Populates the global 'background_tiles' list with each tile image.
    Images 'bg-1.png' to 'bg-10.png' are loaded in that order.

    Global variables:
        background_tiles: List of loaded background tile images.
    """
    global background_tiles
    background_tiles = []
    for i in range(1, 11):
        image = pygame.image.load(f'images/bg-{i}.png').convert()
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        background_tiles.append(image)

def select_tile_index():
    """
    Randomly selects an index for a background tile based on predefined probabilities.
    Uses weighted random selection to choose an index, corresponding to a specific background tile.

    Returns:
        integer: The selected tile index.
    """
    chances = [40] + [10] * 4 + [7] * 2 + [3] * 3 # Change probabilities for each image if needed!
    tiles = list(range(10))  # Tile indices from 0 to 9
    return random.choices(tiles, weights=chances, k=1)[0]

tile_grid = {} # Dictionary to keep track of which tiles are loaded
load_background_tiles()

def get_background_tiles():
    """
    Calculates which background tiles are needed based on the player's position.
    The function creates a list of tiles to be drawn, each with its position and
    randomly selected index.
    Ensures that the same tile is not redrawn and maintains a grid of loaded tiles.

    Global variables:
        tile_grid: Dictionary tracking the loaded tiles on the grid.

    Returns:
        list: List of tuples, where each tuple contains the x and y coordinates of the tile
        and the index of the tile image to be used.
    """
    global tile_grid
    tiles = []
    start_x = int(player.x // WIDTH) * WIDTH
    start_y = int(player.y // HEIGHT) * HEIGHT

    for x in range(start_x - WIDTH, start_x + 2 * WIDTH, WIDTH):
        for y in range(start_y - HEIGHT, start_y + 2 * HEIGHT, HEIGHT):
            grid_x, grid_y = x // WIDTH, y // HEIGHT

            # If the tile is not already in the grid, select a new tile
            if (grid_x, grid_y) not in tile_grid:
                tile_index = select_tile_index()
                tile_grid[(grid_x, grid_y)] = tile_index

            tiles.append((x, y, tile_grid[(grid_x, grid_y)]))

    return tiles

tiles = get_background_tiles()
for tile in tiles:
    x, y, tile_index = tile
    screen.blit(background_tiles[tile_index], (x - camera_x, y - camera_y))