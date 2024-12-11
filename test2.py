def highlight_active_cells(grid):
    """Highlight cells that contain enemies."""
    for cell, enemies in grid.items():
        if enemies:  # If the cell has enemies
            # Calculate cell top-left corner
            cell_x = cell[0] * Static_variables.GRID_SIZE
            cell_y = cell[1] * Static_variables.GRID_SIZE

            # Draw a semi-transparent rectangle
            highlight_color = (255, 0, 0, 100)  # Red with transparency
            s = pygame.Surface((Static_variables.GRID_SIZE, Static_variables.GRID_SIZE), pygame.SRCALPHA)  # Create a transparent surface
            s.fill(highlight_color)
            GameManager.screen.blit(s, (cell_x, cell_y))