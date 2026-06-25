# mygame.py — โครงเกมเปล่าสำหรับ Capstone (คาบ 14)
#
# กฎทอง: แตะแค่โค้ดในช่อง "# N) ..." สามช่องเท่านั้น ห้ามแก้ bentogame.py
# ทุกอย่างที่ต้องใช้คือ game. call:
#   game.start()             -> ปลุกจอ + จอยสติก
#   game.Box(x,y,w,h,col)    -> กล่องที่ขยับได้
#   game.Text(msg,x,y,col)   -> ข้อความบนจอ (.set(...) เปลี่ยนได้)
#   k = game.keys()          -> k.left/.right/.up/.down/.a/.b/.start
#   game.hit(a, b)           -> True ถ้ากล่องสองอันทับกัน
#   game.run(update, fps)    -> วนเรียก update() ของเราไปเรื่อย ๆ
#
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกดปุ่ม "Program to Device"

import bentogame as game
import random

# --- ค่าเกม (ลองปรับเป็นของกลุ่มเราได้) ------------------------------------
PLAYER_SPEED = 8
GOAL = 5

game.start()

# 1) STATE — เกมของเราต้องจำอะไรบ้าง? (สร้างครั้งเดียว ก่อนลูป)
#    ใบ้: มีผู้เล่น 1 กล่อง, มีเป้า 1 กล่อง, มีคะแนน, มีป้ายคะแนน
player = game.Box(game.WIDTH // 2, game.HEIGHT // 2, 30, 30, game.CYAN)
target = ____   # เป้าสีเหลือง วางตำแหน่งสุ่ม (ขนาด 24x24)
score = 0
label = game.Text("Score: 0", 10, 10, game.WHITE)


def update():
    global score

    k = game.keys()
    if k.start:
        return False  # กด Start = จบเกม

    # 2) TICK — ทุกเฟรมอัปเดตยังไง? (ขยับผู้เล่นตามปุ่มจอย)
    if k.left:
        ____
    if k.right:
        ____
    if k.up:
        ____
    if k.down:
        ____

    # 3) WIN / LOSE — ชนแล้วเกิดอะไร? ชนะเมื่อไหร่?
    #    ใบ้: ถ้าผู้เล่นชนเป้า -> +1 คะแนน, ย้ายเป้าไปที่ใหม่, อัปเดตป้าย
    #         ถ้าคะแนนถึง GOAL -> ชนะ -> return False
    if game.hit(player, target):
        ____

    return True  # เล่นต่อ


game.run(update, fps=30)
