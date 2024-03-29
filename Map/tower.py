from math import sqrt
import pygame
import G
from GUI.button import isInside
import Mobs.enemies as enemies


pygame.font.init()
font = pygame.font.Font('bruh_font.ttf', 22)

icon_tr = 80
archer_icon = pygame.transform.scale(pygame.image.load("Assets/GUI/upgrade/archer_icon_lvl1.png"), (icon_tr, icon_tr))
support_icon = pygame.transform.scale(pygame.image.load('Assets/GUI/upgrade/support_icon.png'), (icon_tr, icon_tr))
magic_icon = pygame.transform.scale(pygame.image.load('Assets/GUI/upgrade/magic_icon_stone.png'), (icon_tr, icon_tr))

build_gui = pygame.transform.scale(pygame.image.load('Assets/Towers/archer/build_gui.png'), (180, 180))
lable = pygame.transform.scale(pygame.image.load('Assets/GUI/upgrade/window_1.png'), (47, 28))

towerType = {"archer": [{"damage": 5, "cooldown": 30, "radius": 200, "cost": 70},
                        {"damage": 10, "cooldown": 30, "radius": 240, "cost": 110},
                        {"damage": 7, "cooldown": 20, "radius": 280, "cost": 150}],

             "magic": [{"damage": 15, "cooldown": 50, "radius": 250, "cost": 100},
                       {"damage": 20, "cooldown": 50, "radius": 350, "cost": 160},
                       {"damage": 25, "cooldown": 45, "radius": 450, "cost": 220}],
             "support": [{"damage": 10, "cooldown": 50, "radius": 160, "shiftX": 0.0, "shiftY": 0.19, "cost": 70},
                         {"damage": 10, "cooldown": 50, "radius": 160, "shiftX": 0.0, "shiftY": 0.19, "cost": 110},
                         {"damage": 10, "cooldown": 50, "radius": 160, "shiftX": 0.0, "shiftY": 0.19, "cost": 150}]}


frameLength = 2
magicStrikeLength = 5


def loadTypes(transformation, level):
    """Загружает текстуры соответствующие карте level, умножает каждую на коэффициент transformation"""
    archerShifts = {"leaf": [{"towerShiftX": 0.035, "towerShiftY": 0.22, "topShiftX": 0.06, "topShiftY": -0.76, "archerShiftX": 0.29, "archerShiftY": -0.85},
                             {"towerShiftX": 0.035, "towerShiftY": 0.22, "topShiftX": 0.07, "topShiftY": -0.73, "archerShiftX": 0.35, "archerShiftY": -0.85},
                             {"towerShiftX": 0.0, "towerShiftY": 0.2, "topShiftX": 0.14, "topShiftY": -0.73, "archerShiftX": 1.06, "archerShiftY": -0.79, "archer2ShiftX": 0.99, "archer2ShiftY": -0.79}],
                    "sand": [{"towerShiftX": 0.03, "towerShiftY": 0.2, "archerShiftX": 0.29, "archerShiftY": -0.45},
                             {"towerShiftX": 0.03, "towerShiftY": 0.2, "archerShiftX": 0.39, "archerShiftY": -0.45},
                             {"towerShiftX": 0.0, "towerShiftY": 0.2, "archerShiftX": 0.90, "archerShiftY": -0.47, "archer2ShiftX": 0.80, "archer2ShiftY": -0.47}],
                    "stone": [{"towerShiftX": 0.035, "towerShiftY": 0.22, "archerShiftX": 0.35, "archerShiftY": -0.335},
                              {"towerShiftX": 0.035, "towerShiftY": 0.22, "archerShiftX": 0.35, "archerShiftY": -0.335},
                              {"towerShiftX": 0.0, "towerShiftY": 0.2, "archerShiftX": 0.90, "archerShiftY": -0.35, "archer2ShiftX": 0.80, "archer2ShiftY": -0.34}],
                    "fire": [{"towerShiftX": 0.035, "towerShiftY": 0.22, "archerShiftX": 0.35, "archerShiftY": -0.335},
                             {"towerShiftX": 0.035, "towerShiftY": 0.22, "archerShiftX": 0.35, "archerShiftY": -0.335},
                             {"towerShiftX": 0.0, "towerShiftY": 0.2, "archerShiftX": 0.90, "archerShiftY": -0.35, "archer2ShiftX": 0.80, "archer2ShiftY": -0.34}]}

    magic = {"leaf": [{"shiftX": 0.03, "shiftY": 0.2, "finalHeight": 0.7, "towerShiftY": 0.2, "topShiftX": 0.34, "topShiftY": 0.0},
                      {"shiftX": 0.03, "shiftY": 0.145, "finalHeight": 0.8, "towerShiftY": 0.17, "topShiftX": 0.33, "topShiftY": 0.0},
                      {"shiftX": 0.025, "shiftY": 0.145, "finalHeight": 0.8, "towerShiftY": 0.17, "topShiftX": 0.34, "topShiftY": 0.0, "top2ShiftX": 0.01, "top2ShiftY": 0.137, "top3ShiftX": 0.64, "top3ShiftY": 0.137}],
             "sand": [{"shiftX": 0.02, "shiftY": 0.215, "finalHeight": 0.39, "towerShiftY": 0.11, "topShiftX": 0.36, "topShiftY": 0.0},
                      {"shiftX": 0.02, "shiftY": 0.185, "finalHeight": 0.7, "towerShiftY": 0.175, "topShiftX": 0.38, "topShiftY": 0.0},
                      {"shiftX": 0.02, "shiftY": 0.17, "finalHeight": 0.7, "towerShiftY": 0.168, "topShiftX": 0.38, "topShiftY": 0.0}],
             "fire": [{"shiftX": 0.0, "shiftY": 0.18, "finalHeight": 0.65, "towerShiftY": 0.10, "topShiftX": 0.35, "topShiftY": 0.0},
                      {"shiftX": 0.02, "shiftY": 0.14, "finalHeight": 1, "towerShiftY": 0.1, "topShiftX": 0.35, "topShiftY": 0.0},
                      {"shiftX": 0.02, "shiftY": 0.12, "finalHeight": 0.1, "towerShiftY": 0.01, "topShiftX": 0.285, "topShiftY": 0.0}],
             "stone": [{"shiftX": 0.02, "shiftY": 0.18, "finalHeight": 0.1, "towerShiftY": 0.018, "topShiftX": 0.315, "topShiftY": 0.0},
                       {"shiftX": 0.02, "shiftY": 0.16, "finalHeight": 0.8, "towerShiftY": 0.158, "topShiftX": 0.307, "topShiftY": 0.0},
                       {"shiftX": 0.02, "shiftY": 0.14, "finalHeight": 0.8, "towerShiftY": 0.215, "topShiftX": 0.394, "topShiftY": 0.0, "top1ShiftX": 0.2, "top1ShiftY": 0.015, "top2ShiftX": 0.58, "top2ShiftY": 0.015, "top3ShiftX": 0.15, "top3ShiftY": 0.23, "top4ShiftX": 0.63, "top4ShiftY": 0.23}]}
    if (level == "volcano" or level == "cursedlands" or level == "wastes"):
        level = "fire"
    if (level == "forest" or level == "jungle"):
        level = "leaf"
    if (level == "desert"):
        level = "sand"
    if (level == "snow" or level == "deathlands"):
        level = "stone"
    for lvl in range(0, 3):

        #  Archer

        towerType["archer"][lvl]["top"] = False
        towerType["archer"][lvl]["assets"] = {}
        tower = pygame.image.load("Assets/Towers/Archer/lvl" + str(lvl + 1) + "_" + level + "_tower.png")
        width = int(tower.get_width() * transformation)
        height = int(tower.get_height() * transformation)
        tower = pygame.transform.scale(tower, (int(width), int(height)))
        towerType["archer"][lvl]["assets"]["tower"] = tower
        towerType["archer"][lvl]["towerShiftX"] = int(-width / 2 + width * archerShifts[level][lvl]["towerShiftX"])
        towerType["archer"][lvl]["towerShiftY"] = int(-height + height * archerShifts[level][lvl]["towerShiftY"])

        towerType["archer"][lvl]["assets"]["archer"] = []
        for i in range(0, 6):
            archer = pygame.image.load("Assets/Towers/Archer/" + level + "_archer_" + str(i) + ".png")
            archer = pygame.transform.scale(archer, (int(archer.get_width() * transformation), int(archer.get_height() * transformation)))
            towerType["archer"][lvl]["assets"]["archer"].append(archer)

        if (level == "leaf"):
            top = pygame.image.load("Assets/Towers/archer/lvl" + str(lvl + 1) + "_" + level + "_top.png")
            top = pygame.transform.scale(top, (int(top.get_width() * transformation), int(top.get_height() * transformation)))
            towerType["archer"][lvl]["assets"]["top"] = top
            towerType["archer"][lvl]["topShiftX"] = int(towerType["archer"][lvl]["towerShiftX"] + int(top.get_width()) * archerShifts["leaf"][lvl]["topShiftX"])
            towerType["archer"][lvl]["topShiftY"] = int(towerType["archer"][lvl]["towerShiftY"] + int(top.get_height()) * archerShifts["leaf"][lvl]["topShiftY"])
            towerType["archer"][lvl]["top"] = True

        width = towerType["archer"][lvl]["assets"]["archer"][0].get_width()
        height = towerType["archer"][lvl]["assets"]["archer"][0].get_height()
        towerType["archer"][lvl]["archerShiftX"] = int(towerType["archer"][lvl]["towerShiftX"] / 2 + width * archerShifts[level][lvl]["archerShiftX"])
        towerType["archer"][lvl]["archerShiftY"] = int(towerType["archer"][lvl]["towerShiftY"] + height * archerShifts[level][lvl]["archerShiftY"])
        if (lvl == 2):
            towerType["archer"][lvl]["archer2ShiftX"] = int(towerType["archer"][lvl]["towerShiftX"] / 2 + width * archerShifts[level][lvl]["archer2ShiftX"])
            towerType["archer"][lvl]["archer2ShiftY"] = int(towerType["archer"][lvl]["towerShiftY"] + height * archerShifts[level][lvl]["archer2ShiftY"])

        towerType["archer"][lvl]["height"] = towerType["archer"][lvl]["assets"]["tower"].get_height() + towerType["archer"][lvl]["assets"]["archer"][0].get_height()
        towerType["archer"][lvl]["clearShiftY"] = towerType["archer"][lvl]["archerShiftY"]
        if (lvl == 2):
            towerType["archer"][lvl]["width"] = towerType["archer"][2]["assets"]["archer"][3].get_width() * 2.07
            towerType["archer"][lvl]["clearShiftX"] = towerType["archer"][2]["archer2ShiftX"] - towerType["archer"][2]["assets"]["archer"][3].get_width()
        else:
            towerType["archer"][lvl]["width"] = towerType["archer"][lvl]["assets"]["tower"].get_width()
            towerType["archer"][lvl]["clearShiftX"] = towerType["archer"][lvl]["towerShiftX"]

        #  Magic

        tower = pygame.image.load("Assets/Towers/magic/lvl" + str(lvl + 1) + "_" + level + "_tower.png")
        width = int(tower.get_width() * transformation)
        height = int(tower.get_height() * transformation)
        tower = pygame.transform.scale(tower, (width, height))
        towerType["magic"][lvl]["assets"] = {}

        if (level != "stone" and level != "fire"):
            top = pygame.image.load("Assets/Towers/magic/" + level + "_tower_top.png")
            top = pygame.transform.scale(top, (int(top.get_width() * transformation), int(top.get_height() * transformation)))
            height += int(top.get_height() * magic[level][lvl]["finalHeight"])
            towerType["magic"][lvl]["assets"]["tower"] = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
            towerType["magic"][lvl]["assets"]["tower"].blit(tower, (0, height * magic[level][lvl]["towerShiftY"]))
            towerType["magic"][lvl]["assets"]["tower"].blit(top, (width * magic[level][lvl]["topShiftX"], height * magic[level][lvl]["topShiftY"]))
            if (level == "leaf" and lvl == 2):
                towerType["magic"][lvl]["assets"]["tower"].blit(pygame.transform.rotate(top, 27), (width * magic[level][lvl]["top2ShiftX"], height * magic[level][lvl]["top2ShiftY"]))
                towerType["magic"][lvl]["assets"]["tower"].blit(pygame.transform.rotate(pygame.transform.flip(top, True, False), -27), (width * magic[level][lvl]["top3ShiftX"], height * magic[level][lvl]["top3ShiftY"]))

        else:
            if (lvl != 2):
                top = pygame.image.load("Assets/Towers/magic/" + level + "_tower_top_lvl1-2.png")
            else:
                top = pygame.image.load("Assets/Towers/magic/" + level + "_tower_top_lvl3.png")
            top = pygame.transform.scale(top, (int(top.get_width() * transformation), int(top.get_height() * transformation)))
            height += int(top.get_height() * magic[level][lvl]["finalHeight"])
            towerType["magic"][lvl]["assets"]["tower"] = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
            towerType["magic"][lvl]["assets"]["tower"].blit(tower, (0, height * magic[level][lvl]["towerShiftY"]))
            towerType["magic"][lvl]["assets"]["tower"].blit(top, (width * magic[level][lvl]["topShiftX"], height * magic[level][lvl]["topShiftY"]))
            if (lvl == 2 and level == "stone"):
                towerType["magic"][lvl]["assets"]["tower"].blit(top, (width * magic[level][lvl]["top1ShiftX"], height * magic[level][lvl]["top1ShiftY"]))
                towerType["magic"][lvl]["assets"]["tower"].blit(top, (width * magic[level][lvl]["top2ShiftX"], height * magic[level][lvl]["top2ShiftY"]))
                towerType["magic"][lvl]["assets"]["tower"].blit(top, (width * magic[level][lvl]["top3ShiftX"], height * magic[level][lvl]["top3ShiftY"]))
                towerType["magic"][lvl]["assets"]["tower"].blit(top, (width * magic[level][lvl]["top4ShiftX"], height * magic[level][lvl]["top4ShiftY"]))

        towerType["magic"][lvl]["assets"]["strike"] = []
        strike = pygame.image.load("Assets/Towers/magic/" + level + "_strike_1.png")
        strike = pygame.transform.scale(strike, (int(strike.get_width() * transformation), int(strike.get_height() * transformation)))
        towerType["magic"][lvl]["assets"]["strike"].append(strike)
        strike = pygame.image.load("Assets/Towers/magic/" + level + "_strike_2.png")
        strike = pygame.transform.scale(strike, (int(strike.get_width() * transformation), int(strike.get_height() * transformation)))
        towerType["magic"][lvl]["assets"]["strike"].append(strike)

        towerType["magic"][lvl]["shiftX"] = int(-width / 2 + width * magic[level][lvl]["shiftX"])
        towerType["magic"][lvl]["shiftY"] = int(-height + height * magic[level][lvl]["shiftY"])

        towerType["magic"][lvl]["width"] = width
        towerType["magic"][lvl]["height"] = height
        towerType["magic"][lvl]["clearShiftX"] = towerType["magic"][lvl]["shiftX"]
        towerType["magic"][lvl]["clearShiftY"] = towerType["magic"][lvl]["shiftY"]
        towerType["magic"][lvl]["strikeWidth"] = towerType["magic"][lvl]["assets"]["strike"][0].get_width()
        towerType["magic"][lvl]["strikeHeight"] = towerType["magic"][lvl]["assets"]["strike"][0].get_height()

        #  Support

        tower = pygame.image.load("Assets/Towers/support/lvl" + str(lvl + 1) + "_" + level + "_tower.png")
        width = int(tower.get_width() * transformation)
        height = int(tower.get_height() * transformation)
        tower = pygame.transform.scale(tower, (width, height))

        towerType["support"][lvl]["asset"] = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        towerType["support"][lvl]["asset"].blit(tower, (0, 0))
        towerType["support"][lvl]["shiftX"] = int(-width / 2 + width * towerType["support"][lvl]["shiftX"])
        towerType["support"][lvl]["shiftY"] = int(-height + height * towerType["support"][lvl]["shiftY"])

        towerType["support"][lvl]["width"] = width
        towerType["support"][lvl]["height"] = height
        towerType["support"][lvl]["clearShiftX"] = towerType["support"][lvl]["shiftX"]
        towerType["support"][lvl]["clearShiftY"] = towerType["support"][lvl]["shiftY"]


def clearAll(towers, win, background):
    """Стирает все башни из массива towers с поверхности win, заменяя соответствующей частью изображения background"""
    cleared = []
    for tower in towers:
        if (tower.level != 0):
            currX = tower.x + towerType[tower.typeName][tower.level - 1]["clearShiftX"] - 40
            currY = tower.y + towerType[tower.typeName][tower.level - 1]["clearShiftY"] - 20
            cleared.append(pygame.Rect(int(currX), int(currY), towerType[tower.typeName][tower.level - 1]["width"] + 100, towerType[tower.typeName][tower.level - 1]["height"] + 100))
            win.blit(background, (currX, currY), cleared[len(cleared) - 1])
            if (tower.typeName == "magic" and tower.attacking):
                currX = tower.target[0]
                currY = tower.target[1]
                cleared.append(pygame.Rect(int(currX), int(currY), towerType[tower.typeName][tower.level - 1]["strikeWidth"], towerType[tower.typeName][tower.level - 1]["strikeHeight"]))
                win.blit(background, (currX, currY), cleared[len(cleared) - 1])
                if (tower.frame == 0):
                    tower.attacking = False
    return cleared


class Tower():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gui_opened = False
        self.level = 0

    def isInside(self, x, y):
        return (sqrt((x - self.x)**2 + (y - self.y)**2) <= self.radius)

    def attack(self, mob):
        """Устанавливает кулдаун и начинает анимацию атаки"""
        if (self.typeName == "archer" and self.level == 3):
            if (self.cooldown == 0):
                self.cooldown = towerType[self.typeName][self.level - 1]["cooldown"]
                self.frame = 1
            else:
                self.cooldown2 = towerType[self.typeName][self.level - 1]["cooldown"]
                self.frame2 = 1
        else:
            self.cooldown = towerType[self.typeName][self.level - 1]["cooldown"]
            self.frame = 1
            if (self.typeName == "magic"):
                self.attacking = True
        self.target = (mob.x + enemies.enemyType[mob.typeName]["shiftX"] * 0.2, mob.y + enemies.enemyType[mob.typeName]["shiftY"] * 1.5)

    def isReady(self):
        """Возвращает True, если башня может стрелять"""
        if (self.cooldown == 0):
            return True
        if (self.typeName == "archer" and self.level == 3):
            if (self.cooldown2 == 0):
                return True
        return False

    def reduceCooldown(self):
        """Уменьшает кулдаун на 1"""
        if (self.cooldown != 0):
            self.cooldown -= 1
        if (self.typeName == "archer" and self.level == 3):
            if (self.cooldown2 != 0):
                self.cooldown2 -= 1

    def setType(self, player, typeName):
        """Устанавливает уровень на 1. Заполняет атрибуты башни согласно towerType"""
        if player.gold >= towerType[typeName][0]["cost"]:
            self.typeName = typeName
            self.cost = towerType[self.typeName][0]["cost"]
            self.level = 1
            self.damage = towerType[self.typeName][self.level - 1]["damage"]
            self.radius = towerType[self.typeName][self.level - 1]["radius"]
            self.frame = 0
            self.cooldown = 0
            self.target = None
            if (typeName == "magic"):
                self.attacking = False
            self.cost = towerType[self.typeName][0]["cost"]
            player.gold -= self.cost

    def upgrade(self, player):
        """Увеличивает уровень на 1, но не выше 3. Обновляет атрибуты башни согласно towerType"""
        if (self.level == 3):
            return
        elif player.gold >= towerType[self.typeName][self.level]["cost"]:
            self.level += 1
            self.damage = towerType[self.typeName][self.level - 1]["damage"]
            self.radius = towerType[self.typeName][self.level - 1]["radius"]
            if (self.typeName == "archer" and self.level == 3):
                self.frame2 = 0
                self.cooldown2 = 0

            self.cost = towerType[self.typeName][self.level - 1]["cost"]
            player.gold -= self.cost

    def draw(self, win):
        """Выводит башню на поверхность win и переходит на следующий кадр"""
        if (self.typeName == "archer"):
            if (towerType["archer"][self.level - 1]["top"]):
                win.blit(towerType[self.typeName][self.level - 1]["assets"]["top"], (self.x + towerType[self.typeName][self.level - 1]["topShiftX"], self.y + towerType[self.typeName][self.level - 1]["topShiftY"]))
            else:
                win.blit(towerType[self.typeName][self.level - 1]["assets"]["tower"], (self.x + towerType[self.typeName][self.level - 1]["towerShiftX"], self.y + towerType[self.typeName][self.level - 1]["towerShiftY"]))
            win.blit(towerType[self.typeName][self.level - 1]["assets"]["archer"][self.frame // frameLength], (self.x + towerType[self.typeName][self.level - 1]["archerShiftX"], self.y + towerType[self.typeName][self.level - 1]["archerShiftY"]))
            if (self.frame != 0):
                self.frame += 1
                if (self.frame >= 6 * frameLength):
                    self.frame = 0
            if (self.level == 3):
                width = towerType[self.typeName][self.level - 1]["assets"]["archer"][self.frame2 // frameLength].get_width()
                win.blit(pygame.transform.flip(towerType[self.typeName][self.level - 1]["assets"]["archer"][self.frame2 // frameLength], True, False), (self.x + towerType[self.typeName][self.level - 1]["archer2ShiftX"] - width, self.y + towerType[self.typeName][self.level - 1]["archer2ShiftY"]))
                if (self.frame2 != 0):
                    self.frame2 += 1
                    if (self.frame2 >= 6 * frameLength):
                        self.frame2 = 0
            if (towerType["archer"][self.level - 1]["top"]):
                win.blit(towerType[self.typeName][self.level - 1]["assets"]["tower"], (self.x + towerType[self.typeName][self.level - 1]["towerShiftX"], self.y + towerType[self.typeName][self.level - 1]["towerShiftY"]))
        elif (self.typeName == "magic"):
            win.blit(towerType[self.typeName][self.level - 1]["assets"]["tower"], (self.x + towerType[self.typeName][self.level - 1]["shiftX"], self.y + towerType[self.typeName][self.level - 1]["shiftY"]))
            if (self.attacking):
                win.blit(towerType[self.typeName][self.level - 1]["assets"]["strike"][(self.frame - 1) // magicStrikeLength], (self.target[0], self.target[1]))
                self.frame += 1
                if (self.frame >= 2 * magicStrikeLength):
                    self.frame = 0
        else:
            win.blit(towerType[self.typeName][self.level - 1]["asset"], (self.x + towerType[self.typeName][self.level - 1]["shiftX"], self.y + towerType[self.typeName][self.level - 1]["shiftY"]))
        # pygame.draw.circle(win, (255, 0, 0), (round(self.x), round(self.y)), self.radius, 1)

    def draw_gui(tower):

        if tower.level == 0:

            archer_tower_cost = font.render(str(towerType["archer"][0]["cost"]), True, (255, 255, 0), 0)
            magic_tower_cost = font.render(str(towerType["magic"][0]["cost"]), True, (255, 255, 0), 0)
            # support_tower_cost = font.render(str(towerType["support"][0]["cost"]), True, (255, 255, 0), 0)

            G.win.blit(build_gui, (tower.x - 90, tower.y - 90))

            G.win.blit(archer_icon, (tower.x - 100, tower.y - 90))
            G.win.blit(lable, (tower.x - 85, tower.y - 110))
            G.win.blit(archer_tower_cost, (tower.x - 80, tower.y - 110))

            # G.win.blit(support_icon, (tower.x - 100, tower.y + 20))
            # G.win.blit(lable, (tower.x - 85, tower.y))
            # G.win.blit(support_tower_cost, (tower.x - 80, tower.y))

            G.win.blit(magic_icon, (tower.x + 20, tower.y - 90))
            G.win.blit(lable, (tower.x + 35, tower.y - 110))
            G.win.blit(magic_tower_cost, (tower.x + 40, tower.y - 110))

        if tower.level != 0 and tower.level != 3:

            G.win.blit(build_gui, (tower.x - 90, tower.y - 90))
            if tower.level != 3:
                archer_tower_cost = font.render(str(towerType["archer"][tower.level]["cost"]), True, (255, 255, 0), 0)
                magic_tower_cost = font.render(str(towerType["magic"][tower.level]["cost"]), True, (255, 255, 0), 0)
                # support_tower_cost = font.render(str(towerType["support"][tower.level]["cost"]), True, (255, 255, 0), 0)

                if tower.typeName == "magic":
                    G.win.blit(magic_icon, (tower.x + 20, tower.y - 90))
                    G.win.blit(lable, (tower.x + 35, tower.y - 110))
                    G.win.blit(magic_tower_cost, (tower.x + 40, tower.y - 110))

                if tower.typeName == "archer":
                    G.win.blit(archer_icon, (tower.x - 100, tower.y - 90))
                    G.win.blit(lable, (tower.x - 85, tower.y - 110))
                    G.win.blit(archer_tower_cost, (tower.x - 80, tower.y - 110))

                # if tower.typeName == "support":
                    # G.win.blit(support_icon, (tower.x - 100, tower.y + 20))
                    # G.win.blit(lable, (tower.x - 85, tower.y))
                    # G.win.blit(support_tower_cost, (tower.x - 80, tower.y))

    def gui_level_up(tower, player, mouse_pos):

        if tower.level != 0:

            if tower.typeName == "archer":
                if isInside(mouse_pos[0], mouse_pos[1], tower.x - 60, tower.y - 50, 70):
                    tower.upgrade(player)
                    tower.gui_opened = False

            if tower.typeName == "magic":
                if isInside(mouse_pos[0], mouse_pos[1], tower.x + 60, tower.y - 50, 70):
                    tower.upgrade(player)
                    tower.gui_opened = False

            # if tower.typeName == "support":
            #     if isInside(mouse_pos[0], mouse_pos[1], tower.x - 60, tower.y + 50, 70):
            #         tower.upgrade(player)
            #         tower.gui_opened = False

    def gui_close(towers, exc):

        for i in range(len(towers)):
            if i != exc:
                towers[i].gui_opened = False

    def gui_type_change(tower, player, mouse_pos):

        if tower.level == 0:

            if isInside(mouse_pos[0], mouse_pos[1], tower.x - 60, tower.y - 50, 70):
                tower.setType(player, "archer")
                tower.gui_opened = False
            if isInside(mouse_pos[0], mouse_pos[1], tower.x + 60, tower.y - 50, 70):
                tower.setType(player, "magic")
                tower.gui_opened = False
            # if isInside(mouse_pos[0], mouse_pos[1], tower.x - 60, tower.y + 60, 70):
            #     tower.setType(player, "support")
            #     tower.gui_opened = False
