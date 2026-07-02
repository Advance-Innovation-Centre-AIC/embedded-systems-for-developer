# mygame.py (เฉลย MVP) — โครงเกมเปล่าที่ "เติม 3 ช่องครบแล้ว" สำหรับคาบ 13 Showcase
#
# เป้าหมาย: ผู้เล่นกล่อง cyan วิ่งด้วย joystick ไปชนเป้า yellow ให้ครบ 5 แต้มแล้วชนะ
#           ใช้เป็น "ตัวอย่างเต็ม" ให้น้อง ๆ เทียบหลังเติม practise_codes/mygame.py เอง
#
# วิธีรันบนบอร์ดจริง: เปิดไฟล์นี้ใน BENTO IDE แล้วกด Program to Device
#   (เราไม่ใช้ exec(open(...)) — IDE ส่งโค้ดลงบอร์ดแล้วรันให้เอง)
#
# กฎทอง: ห้ามแก้ bentogame.py (70% core) — เขียนจริงแค่ 3 ช่องในไฟล์นี้เท่านั้น

import bentogame as game

PLAYER_SPEED = 8          # ขยับทีละกี่พิกเซลต่อเฟรม
FPS = 30                  # ความถี่ของลูป
WIN_SCORE = 5             # ชนเป้าครบเท่านี้ = ชนะ

game.title("MY GAME")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

# 1) STATE — เกมต้องจำอะไรบ้าง (สร้างครั้งเดียว ก่อนลูป)
score = 0
player = game.Box(game.WIDTH // 2, game.HEIGHT // 2, 32, 32, game.CYAN)
target = game.Box(120, 120, 28, 28, game.YELLOW)
label = game.Text("Score: 0", 12, 10, game.WHITE)


def _move_target():
    # สุ่มตำแหน่งเป้าใหม่แบบเบา ๆ (ใช้ตัวแปร score เป็นเมล็ดสุ่มแบบง่าย)
    nx = (target.x * 7 + 113) % (game.WIDTH - target.w)
    ny = (target.y * 5 + 71) % (game.HEIGHT - target.h)
    target.move_to(nx, ny)


def update():
    """ถูกเรียกทุกเฟรม. return False = จบเกม."""
    global score

    # 2) TICK — กติกาทุกเฟรม: อ่านปุ่มแล้วขยับผู้เล่น
    k = game.keys()
    if k.left:
        player.move(-PLAYER_SPEED, 0)
    if k.right:
        player.move(PLAYER_SPEED, 0)
    if k.up:
        player.move(0, -PLAYER_SPEED)
    if k.down:
        player.move(0, PLAYER_SPEED)
    # BACK = ออกเกม, START = เริ่มใหม่ — game.run() จัดการให้อัตโนมัติ
    # update() จึง return False เฉพาะตอน "ชนะ/แพ้จริง" เท่านั้น

    # 3) WIN / LOSE — ชนเป้า = +1 แต้ม, ครบ WIN_SCORE = ชนะ
    if game.hit(player, target):
        score += 1
        label.set("Score: %d" % score)
        game.sfx("point")
        _move_target()
        if score >= WIN_SCORE:
            game.Text("YOU WIN!", game.WIDTH // 2 - 70, game.HEIGHT // 2, game.GREEN)
            game.sfx("win")
            return False

    return True  # เล่นต่อ


game.run(update, fps=FPS)
