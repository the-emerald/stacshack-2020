# Import Modules
from collections import defaultdict

import pygame as pg
import random

from sprites.hud import HUD
from sprites.player import Player
from sprites.potion import Potion
from sprites.wall import Wall
from util.spawning import chance_spawn


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pg.init()
    screen_width = 800
    screen_height = 600
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Bullet Hell Thing")
    pg.mouse.set_visible(0)

    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Put Text On The Background, Centered
    # if pg.font:
    #     font = pg.font.Font(None, 36)
    #     text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
    #     textpos = text.get_rect(centerx=background.get_width() / 2)
    #     background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    # pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()
    player = Player(screen_width, screen_height)
    hud = HUD(player)
    invisible_top_wall = Wall(0, -35, screen_width, 10)
    invisible_bottom_wall = Wall(0, screen_height + 25, screen_width, 10)
    invisible_left_wall = Wall(-35, 0, 10, screen_height)
    invisible_right_wall = Wall(screen_width + 25, 0, 10, screen_height)
    invisible_middle_wall = Wall(screen_width/2-15, screen_height/2-15, 30, 30)
    top_wall = Wall(0, 0, screen_width, 10)
    bottom_wall = Wall(0, screen_height - 10, screen_width, 10)
    left_wall = Wall(0, 0, 10, screen_height)
    right_wall = Wall(screen_width-10, 0, 10, screen_height)
    middle_wall = Wall(screen_width/2-50, screen_height/2-50, 100, 100)
    walls = pg.sprite.RenderPlain(top_wall, bottom_wall, left_wall, right_wall, middle_wall)
    collision_walls = pg.sprite.RenderPlain(invisible_top_wall, invisible_bottom_wall, invisible_left_wall, invisible_right_wall, invisible_middle_wall)
    allsprites = pg.sprite.RenderPlain(player, walls, collision_walls, hud)
    player.walls = collision_walls.sprites()

    # Tracker
    item_count = defaultdict(lambda: 0)

    # Main Loop
    going = True
    while going:
        # draw the background
        screen.blit(background, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False

            # player attack
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                player.start_attack()

            if event.type == pg.KEYDOWN and event.key == pg.K_0:  # TODO: Replace me with
                player.health -= 1

        if random.random() < chance_spawn(item_count[Potion]):  # TODO: Replace me with actual logic!
            allsprites.add(Potion())
            item_count[Potion] = item_count[Potion] + 1

        # update player (movement, attack frame, health)
        player.update()

        # draw
        # screen.fill((255, 255, 255))
        allsprites.update()

        # Draw Everything
        allsprites.draw(screen)
        pg.display.flip()

        clock.tick(60)

    pg.quit()


if __name__ == '__main__':
    main()
