from tkinter import *
from random import *
import math
import time
import 秀娟

class Ball:
    def __init__(self, canvas,  x, y, dx, dy, w, color):
        self.canvas = canvas
        self.id = canvas.create_oval(x - w/2, y - w/2, x + w/2, y + w/2, fill=color)  # 建立球物件
        self.x = x        # 球心x座標
        self.y = y        # 球心y座標
        self.w = w        # 球半徑
        self.dx = dx      # 球的x方向速度
        self.dy = dy      # 球的y方向速度
        self.collid = 0   #檢查球是否剛發生玩碰撞(避免沾黏) 0是沒發生碰撞

    def ballMove(self, ballList):
        if self.canvas.coords(self.id)[0] < 0:
            self.dx = abs(self.dx)
        if self.canvas.coords(self.id)[2] > 800:
            self.dx = -abs(self.dx)
        if self.canvas.coords(self.id)[1] < 0:
            self.dy = abs(self.dy)
        if self.canvas.coords(self.id)[3] > 600:
            self.dy = -abs(self.dy)
        if self.collid == 0:               #沒發生碰撞才檢查碰撞
            for item in ballList:
                if item.id != self.id:
                    dis = math.sqrt(pow(abs(self.x - item.x), 2) + pow(abs(self.y - item.y), 2))
                    if dis <= (self.w / 2 + item.w / 2):
                        #計算兩個球的質量
                        m1 = math.pi * pow(self.w/2,2)
                        m2 = math.pi * pow(item.w/2,2)
                        #避免計算時將原始數值洗掉
                        #所以先暫存兩球的xy方向速度
                        tempdx1 = self.dx
                        tempdy1 = self.dy
                        tempdx2 = item.dx
                        tempdy2 = item.dy
                        #彈性碰撞公式
                        self.dx = (tempdx1 * (m1 - m2) + 2 * m2 * tempdx2) / (m1 + m2)
                        self.dy = (tempdy1 * (m1 - m2) + 2 * m2 * tempdy2) / (m1 + m2)
                        item.dx = (tempdx2 * (m2 - m1) + 2 * m1 * tempdx1) / (m1 + m2)
                        item.dy = (tempdy2 * (m2 - m1) + 2 * m1 * tempdy1) / (m1 + m2)
                        self.collid = 2
                        item.collid = 2
        else:                                                  #剛發生玩碰撞就等後幾輪再檢查
            self.collid -= 1
        self.canvas.move(self.id, self.dx, self.dy)            # 球移動
        self.x += self.dx                                      # 紀錄球圓心移動
        self.y += self.dy                                      # 紀錄球圓心移動

tk1 = Tk()
tk1.title("Bouncing Ball")                       # 遊戲視窗標題
tk1.wm_attributes('-topmost', 1)                 # 確保遊戲視窗在螢幕最上層

winW = 800                                      # 定義畫布寬度
winH = 600                                      # 定義畫布高度

canvas1 = Canvas(tk1, width=winW, height=winH, bg = 'skyblue')
canvas1.pack()

balls = 8                                 #設定球的數量
ballList = []                              #球物件串列

while len(ballList) < balls:               #產生指定數量的球物
    if len(ballList) == 0:                 #產生第一個球物件
        ballList.append(Ball(canvas1, randint(100, 700), randint(100, 500), randint(1, 4), randint(1, 4), randint(100,101), choice(秀娟.COLORS)))
    else:                                  #產生第二個球物件開始要避免球發生重疊
        iniX = randint(100, 700)
        iniY = randint(100, 500)
        iniW = randint(100,101)
        overlap = False
        for item in ballList:              #與產生過的球物件比較是否有重疊
            dist = math.sqrt(pow(abs(iniX - item.x), 2) + pow(abs(iniY - item.y), 2))
            if dist <= (iniW / 2 + item.w / 2):
                overlap = True
                continue
        if overlap == False:               #如果沒有重疊才產生新的球物件
            ballList.append(Ball(canvas1, iniX, iniY, randint(1, 4), randint(1, 4), iniW,choice(秀娟.COLORS)))

while True:
    for item in ballList:
        item.ballMove(ballList)
    time.sleep(0.001)
    tk1.update()
