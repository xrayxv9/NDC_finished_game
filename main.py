import pyxel
import json


class Enemy:
    def __init__(self,x, y, u, v, type: str):
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.speed = 30
        self.sens = 'TOP'
        self.type = type
        self.score = 0
        self.tir_list = []
        pyxel.load('univers/1.pyxres')

    def update(self):
        self.depla()
        if pyxel.frame_count % 30 == 0:
            self.tirs_creation(self.x, self.y)

        self.tirs_deplacement()

    def tirs_deplacement(self):
        if self.type == 'RIGHT':
            for tir in self.tir_list:
                tir[0] -= 1
                if tir[0] < 0:
                    self.tir_list.remove(tir)
                    self.score += 1
            return self.tir_list

        if self.type == 'LEFT':
            for tir in self.tir_list:
                tir[0] += 1
                if tir[0] > 128:
                    self.tir_list.remove(tir)
                    self.score += 1
            return self.tir_list

        if self.type == 'TOP':
            for tir in self.tir_list:
                tir[1] += 1
                if tir[1] > 128:
                    self.tir_list.remove(tir)
                    self.score += 1
            return self.tir_list

        if self.type == 'BOT':
            for tir in self.tir_list:
                tir[1] -= 1
                if tir[1] < 0:
                    self.tir_list.remove(tir)
                    self.score += 1
            return self.tir_list
    def depla(self):

        if self.type == 'RIGHT' or self.type == 'LEFT':

            if 24 <= self.y <= 96:
                if self.sens == 'TOP':
                    self.y += 1
                    if self.y == 96:
                        self.sens = 'BAS'
                if self.sens == 'BAS':
                    self.y -= 1
                    if self.y == 24:
                        self.sens = 'TOP'

        if self.type == 'TOP' or self.type == 'BOT':

            if 24 <= self.x <= 96:
                if self.sens == 'TOP':
                    self.x += 1
                    if self.x == 96:
                        self.sens = 'BAS'
                if self.sens == 'BAS':
                    self.x -= 1
                    if self.x == 24:
                        self.sens = 'TOP'



    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, 8, 8)
        if self.tir_list:
            for x in self.tir_list:
                pyxel.rect(x[0], x[1], 1, 1, 8)

    def tirs_creation(self, x, y):
        if self.type == 'RIGHT':
            self.tir_list.append([x - 4, y - 4])

        if self.type == 'LEFT':
            self.tir_list.append([x + 4, y + 4])

        if self.type == 'TOP':
            self.tir_list.append([x + 4, y + 4])

        if self.type == 'BOT':
            self.tir_list.append([x - 4, y - 4])




class Player:
    def __init__(self):
        self.x = 64
        self.y = 64
        self.v = 0
        self.alive = True

    def draw(self):
        pyxel.camera(0, 0)
        pyxel.load('univers/1.pyxres')
        pyxel.blt(self.x, self.y, 0, 8, self.v, 8, 8)
        pyxel.camera(0, 0)

    def depla(self):
        if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_UP):
            if self.y > 24:
                self.y -= 1
            else:
                self.y -= 10
                self.alive = False
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_UP):
            if self.x < 98:
                self.x += 1
                self.v = 0
            else:
                self.x += 10
                self.alive = False

        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_UP):
            if self.y < 98:
                self.y += 1

            else:
                self.y += 10
                self.alive = False
        if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_UP):
            if self.x > 24:
                self.x -= 1
                self.v = 8
            else:
                self.x -= 10
                self.alive = False


class App:
    def __init__(self):
        pyxel.init(128, 128, title='OUI')
        self.player = Player()
        self.ennemie = Enemy(112, 24, 8, 24, 'RIGHT')
        self.ennemie2 = Enemy(8, 24, 0, 24, 'LEFT')
        self.ennemie3 = Enemy(24, 8, 8, 16, 'TOP')
        self.ennemie4 = Enemy(24, 112, 0, 16, 'BOT')
        self.data = []


        self.liste = [
            self.ennemie,
            self.ennemie2,
            self.ennemie3,
            self.ennemie4
        ]


        pyxel.run(self.update, self.draw)


    def update(self):

        self.player.depla()
        self.ennemie.update()
        if self.ennemie.score >= 5:
            self.ennemie2.update()
        if self.ennemie2.score >= 5:
            self.ennemie3.update()
        if self.ennemie3.score >= 5:
            self.ennemie4.update()
        self.ennemis_suppression()

        if not self.player.alive:
            self.game_over()


    def draw(self):

        pyxel.load('univers/1.pyxres')
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
        with open('json/data.json', 'r', encoding='UTF-8') as f:
            self.data = json.load(f)
        pyxel.text(10, 10,
                   f"score: {self.ennemie.score + self.ennemie2.score + self.ennemie3.score + self.ennemie4.score}", 5)
        pyxel.text(10, 114, f"cooldown bullets {self.ennemie.speed}", 5)
        pyxel.text(60, 10, f"best score {self.data[0]}", 5)
        self.player.draw()
        self.ennemie.draw()

        if self.ennemie.score >= 5:
            self.ennemie2.draw()
        if self.ennemie2.score >= 5:
            self.ennemie3.draw()
        if self.ennemie3.score >= 5:
            self.ennemie4.draw()

        if self.ennemie.score + self.ennemie2.score + self.ennemie3.score + self.ennemie4.score > 90:
            for x in self.liste:
                x.speed = 20

        if self.ennemie.score + self.ennemie2.score + self.ennemie3.score + self.ennemie4.score > 180:
            for x in self.liste:
                x.speed = 10


    def ennemis_suppression(self):
        for x in self.liste:
            for tir in x.tir_list:
                if tir[0] > self.player.x > tir[0] - 8 and tir[1] > self.player.y > tir[1] - 8:
                    self.game_over()

    def game_over(self):
        self.player.x = 64
        self.player.y = 64
        self.player.alive = True
        with open('json/data.json', 'w', encoding='UTF-8') as f:
            if self.data[0] < self.ennemie.score + self.ennemie2.score + self.ennemie3.score + self.ennemie4.score:
                json.dump([self.ennemie.score + self.ennemie2.score + self.ennemie3.score + self.ennemie4.score], f, indent=4)
            else:
                json.dump([self.data[0]], f, indent=4)
        for x in self.liste:
            x.score = 0
            x.tir_list.clear()
            x.speed = 30


App()