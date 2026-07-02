# shooter_step4.py — สร้าง Shooter #4 (คาบ 16): ศัตรู + ชน + คะแนน + ชีวิต = เกมเต็ม
# ------------------------------------------------------------------------------
# step นี้คือตอนที่เกมเล่นจบได้จริง (beginner-complete) และเทียบกันได้ว่า MicroPython == C
# ไอเดียคือ เราใส่ศัตรูที่ตกลงมาจากฟ้า, ยิงโดน = ระเบิด + ได้คะแนน, ปล่อยให้หลุดถึงพื้น
# = เสียชีวิต, พอชีวิตหมดก็ GAME OVER. ครบองค์ประกอบของเกมยิงจริง เล่นเอาชนะกันได้แล้ว
# Core 70% ที่เพิ่งได้ใช้: game.hit(a, b) (ตรวจชนแบบ AABB) แล้วอัปเดต HUD
# ฝั่ง C ทำงานเหมือนกันบนจอ: ยิงโดน=ระเบิด+คะแนน, หลุดล่าง=เสียชีวิต, หมด=จบเกม
#   (เทียบกับ shooter_step4.c ได้ — shooter_step() ใช้ตรรกะชน/คะแนน/ชีวิตเดียวกัน)
# อ้างอิงเกมจริง: reference/shooter_full.py:22-24,32-34,61-76 ; page_game_shooter.c:358-420
# ------------------------------------------------------------------------------
import bentogame as game
import random

ACCEL, MAX_SPEED, FRICTION = 1.4, 13.0, 0.80
MAX_BULLETS, MAX_ENEMIES = 6, 6                 # บ่อกระสุน 6, บ่อศัตรู 6
ENEMY_COLORS = [game.RED, game.ORANGE, game.PINK]

game.title("SHOOTER")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

ship = game.Box(365, 352, 62, 24, game.GREEN)
ship_x, ship_speed = 365.0, 0.0
score, lives, fire_cooldown = 0, 3, 0
hud = game.Text("Score: 0   Lives: 3", 10, 8, game.WHITE)

bullets = [game.Box(0, -50, 6, 14, game.CYAN) for _ in range(MAX_BULLETS)]
for bullet in bullets:
    bullet.hide()

# ----- เติมส่วนนี้เอง (1): บ่อศัตรู ตกจากบนด้วยความเร็วสุ่ม -----
enemies = [game.Box(random.randint(0, game.WIDTH - 30), -random.randint(40, 400),
                    30, 24, random.choice(ENEMY_COLORS)) for _ in range(MAX_ENEMIES)]
enemy_speed = [random.uniform(2.5, 4.5) for _ in range(MAX_ENEMIES)]

def find_free_bullet():
    for bullet in bullets:
        if bullet.y < -20:
            return bullet
    return None

# ----- เติมส่วนนี้เอง (2): รีไซเคิลศัตรู ส่งกลับขึ้นบนสุด -----
def respawn_enemy(index):
    enemies[index].move_to(random.randint(0, game.WIDTH - 30), -random.randint(20, 200))
    enemies[index].set_color(random.choice(ENEMY_COLORS))

def on_frame():
    global ship_x, ship_speed, score, lives, fire_cooldown
    keys = game.keys()
    # (Back=ออก / Start=เริ่มใหม่ — game.run() จัดการให้)

    # ยาน (step2)
    if keys.left:    ship_speed -= ACCEL
    elif keys.right: ship_speed += ACCEL
    else:            ship_speed *= FRICTION
    ship_speed = max(-MAX_SPEED, min(MAX_SPEED, ship_speed))
    ship_x = max(0, min(game.WIDTH - ship.w, ship_x + ship_speed))
    ship.move_to(ship_x, 352)

    # ยิง (step3)
    fire_cooldown = max(0, fire_cooldown - 1)
    if (keys.a or keys.up) and fire_cooldown == 0:
        bullet = find_free_bullet()
        if bullet:
            bullet.show(); bullet.move_to(ship_x + ship.w // 2 - 3, 340); game.sfx("fire"); fire_cooldown = 8

    for bullet in bullets:
        if bullet.y >= -20:
            bullet.move_to(bullet.x, bullet.y - 9)
            if bullet.y < -20: bullet.hide()

    # ----- เติมส่วนนี้เอง (3+4): ศัตรูตก, ชน, คะแนน, ชีวิต, จบเกม -----
    for index, enemy in enumerate(enemies):
        enemy.move_to(enemy.x, enemy.y + enemy_speed[index])
        if enemy.y > game.HEIGHT:              # ศัตรูหลุดถึงล่าง = เสีย 1 ชีวิต
            lives -= 1
            hud.set("Score: %d   Lives: %d" % (score, lives))
            respawn_enemy(index)
            if lives <= 0:
                game.sfx("gameover")
                game.Text("GAME OVER", 320, 180, game.RED)
                return False
            continue
        for bullet in bullets:                 # กระสุนโดนศัตรู?
            if bullet.y >= -20 and game.hit(bullet, enemy):
                score += 1
                game.sfx("hit")
                hud.set("Score: %d   Lives: %d" % (score, lives))
                bullet.move_to(0, -50); bullet.hide()    # กระสุนกลับบ่อ
                respawn_enemy(index)            # ศัตรูเกิดใหม่
                break
    # -----------------------------------------------------------------------

game.run(on_frame, fps=30)
