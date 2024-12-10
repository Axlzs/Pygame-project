def enable_push(self, lessers, enemies):

    for i, enemy in enumerate(lessers):
        for j in range(i + 1, len(lessers)):
            other = lessers[j]

            # Calculate distance between enemy and other
            dx = other.hitbox.centerx - enemy.hitbox.centerx
            dy = other.hitbox.centery - enemy.hitbox.centery
            dist = (dx**2 + dy**2) ** 0.5

            if dist < Static_variables.REPULSION_RADIUS and dist > 0:
                # Repulsion force
                force = Static_variables.REPULSION_FORCE / dist
                repulsion_dx = dx * force
                repulsion_dy = dy * force

                # Apply repulsion equally but opposite to both enemies
                enemy.rect.x -= repulsion_dx
                enemy.rect.y -= repulsion_dy
                other.rect.x += repulsion_dx
                other.rect.y += repulsion_dy

    # Push stronger enemies if close
    for enemy in lessers:
        for strong_enemy in enemies:
            dx = strong_enemy.rect.centerx - enemy.rect.centerx
            dy = strong_enemy.rect.centery - enemy.rect.centery
            dist = (dx**2 + dy**2) ** 0.5

            if dist < Static_variables.REPULSION_RADIUS and dist > 0:
                # Push the stronger enemy
                force = Static_variables.REPULSION_FORCE / dist
                push_dx = dx * force
                push_dy = dy * force

                strong_enemy.rect.x += push_dx
                strong_enemy.rect.y += push_dy