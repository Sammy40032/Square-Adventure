def check_respawn(player, levels, current_level):
    starting_platform = levels[current_level][0]

    if player.y >= 670:
        player.x = starting_platform.x + (starting_platform.width / 2) - (player.size / 2)
        player.y = starting_platform.y - player.size
        player.vel_y = 0
        player.on_ground = True

    player.on_ground = False

    for platform in levels[current_level]:
        if (player.y + player.size >= platform.y and
            player.y + player.size <= platform.y + 10 and
            player.x + player.size > platform.x and
            player.x < platform.x + platform.width):
            player.y = platform.y - player.size
            player.vel_y = 0
            player.on_ground = True
            break
