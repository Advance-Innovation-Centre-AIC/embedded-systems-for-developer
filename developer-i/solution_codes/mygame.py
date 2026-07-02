# mygame.py (เฉลย) — โครงเกม MVP สำหรับ Capstone (คาบ 14)
#
# เฉลยนี้เติมครบทั้ง 3 ช่องของไฟล์เว้นช่อง practise_codes/mygame.py
# กฎทองยังเหมือนเดิม: แตะแค่ 3 ช่อง ห้ามแก้ bentogame.py
#
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกดปุ่ม "Program to Device"

import bentogame as game
import random

# --- ค่าเกม ----------------------------------------------------------------
PLAYER_SPEED = 8
GOAL = 5


def random_spot():
    """สุ่มตำแหน่งเป้าให้อยู่ในจอ (เผื่อขอบ)"""
    x = random.randint(0, game.WIDTH - 24)
    y = random.randint(0, game.HEIGHT - 24)
    return x, y


game.title("MY GAME")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

# 1) STATE — สิ่งที่เกมต้องจำ
player = game.Box(game.WIDTH // 2, game.HEIGHT // 2, 30, 30, game.CYAN)
tx, ty = random_spot()
target = game.Box(tx, ty, 24, 24, game.YELLOW)
score = 0
label = game.Text("Score: 0", 10, 10, game.WHITE)


def update():
    global score

    k = game.keys()
    # (Back=ออก / Start=เริ่มใหม่ — game.run() จัดการให้)

    # 2) TICK — ขยับผู้เล่นตามปุ่มจอย (Box.move clamp ขอบให้เองแล้ว)
    if k.left:
        player.move(-PLAYER_SPEED, 0)
    if k.right:
        player.move(PLAYER_SPEED, 0)
    if k.up:
        player.move(0, -PLAYER_SPEED)
    if k.down:
        player.move(0, PLAYER_SPEED)

    # 3) WIN / LOSE — ชนเป้าได้คะแนน ครบ GOAL แล้วชนะ
    if game.hit(player, target):
        score += 1
        label.set("Score: %d" % score)
        game.sfx("point")
        nx, ny = random_spot()
        target.move_to(nx, ny)
        if score >= GOAL:
            label.set("YOU WIN!")
            game.sfx("win")
            return False

    return True  # เล่นต่อ


game.run(update, fps=30)
