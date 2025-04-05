def check_respawn(
        player, ground_y, respawn_x=200, respawn_y=450
    ):
    if (
        player.y + player.size >= ground_y
    ):
        player.x = respawn_x
        player.y = respawn_y
        player.vel_y = 0
        player.on_ground = False
