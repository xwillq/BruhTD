import pygame
from GUI.button import Button
from GUI.button import isInside
import Mobs.enemies as enemies
from Map.tower import Tower as Tower
import Map.tower as tower
import G

pygame.font.init()
font = pygame.font.Font('bruh_font.otf', 32)
death_button = Button(15, 325, 40, pygame.image.load('Assets/GUI/interface_game/skull.png'))


def draw(turns, background, start, Idirection, mobs, player, towers):

    G.win.blit(background, (0, 0))

    playerHealth = font.render(str(player.hp), True, (255, 0, 0), 0)
    playerGold = font.render(str(player.gold), True, (255, 255, 0), 0)

    updates = tower.clearAll(towers, G.win, background)
    updates += enemies.clearAll(mobs, G.win, background)

    if G.event.type is pygame.MOUSEBUTTONUP and G.wave_trigger is False:
        mouse_pos = pygame.mouse.get_pos()
        if G.condition == 10:
            if isInside(mouse_pos[0], mouse_pos[1], 15 + 20, 325 + 20, 50) is True:
                G.wave_trigger = True

    if G.wave_trigger is False:
        death_button.draw(G.win)

    if G.wave_trigger is True:
        enemies.updatePositions(mobs, turns, 1920, 1080, player)

        for i in range(len(towers)):
            if towers[i].level == 0:
                continue
            if towers[i].isReady():
                for j in range(len(mobs)):
                    if (towers[i].isInside(mobs[j].x, mobs[j].y) and mobs[j].state != "dying" and mobs[j].state != "dead"):
                        towers[i].attack(mobs[j])
                        mobs[j].hurt(towers[i].damage)
                        break
            else:
                towers[i].reduceCooldown()

        for mob in mobs:
            if (mob.state == "dead"):
                mobs.remove(mob)
                player.gold_add(mob)
            else:
                mob.draw(G.win)

    if G.event.type is pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        for i in range(len(towers)):
            if isInside(mouse_pos[0], mouse_pos[1], towers[i].x, towers[i].y, 120):
                towers[i].gui_opened = True
                Tower.gui_close(towers, i)
            if towers[i].gui_opened:
                Tower.gui_level_up(towers[i], player, mouse_pos)
                Tower.gui_type_change(towers[i], player, mouse_pos)

    for i in range(len(towers)):
        if towers[i].level != 0:
            # pygame.draw.circle(G.win, (0, 55, 255), (towers[i].x, towers[i].y), round(towers[i].radius), 1)
            towers[i].draw(G.win)
        if towers[i].gui_opened is True:
            Tower.draw_gui(towers[i])
        if player.hp <= 0 and towers[i].level != 0:
            towers[i].level = 0

    if player.hp <= 0:
        G.condition = 2
        G.level_number = 0
        G.online = False
        G.wave_trigger = False

    if len(mobs) == 0 and player.hp > 0:
        G.condition = 3
        G.level_number = 0
        G.online = False
        G.wave_trigger = False

    G.win.blit(playerHealth, (15, 1000))
    G.win.blit(playerGold, (15, 1030))
    pygame.display.update(updates)
    G.event = G.event_N
