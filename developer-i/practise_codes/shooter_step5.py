# โครงเว้น 30% — ช่องที่เราเว้นไว้ให้คุณเติมเอง / เฉลย: starter/shooter_step5.py / ใบ้: ในใบงาน session
# ------------------------------------------------------------------------------
# shooter_step5.py — สร้าง Shooter #5 (คาบ 16+): ระดับความยาก + คลื่นศัตรู (wave spawn)
# ------------------------------------------------------------------------------
# *** หมายเหตุ parity (สำคัญ — ตาม MASTER_PLAN.md §2.4) ***
# ฝั่งอ้างอิง reference/shooter_full.py "จบที่ step4" โดยตั้งใจ. step5 (ตารางโหมด,
# คลื่นศัตรู, ระเบิด-pool, sprites, music, scanlines) = "ของแถมฝั่ง C console".
# ไฟล์นี้คือ Python ที่ขยับ "ตรรกะ" ให้ตรงกับ C step5 เท่าที่ Python ทำได้:
#   - ตารางโหมด (FREE/EASY/DIFFICULT) แบบเดียวกับ C (:85-89)
#   - spawn timer ปล่อยศัตรูเป็น "คลื่น" ตามจังหวะของโหมด (:362-368)
# สิ่งที่ "ไม่มี" ใน Python (C-native, flagged): ระเบิด-pool, sprites pixel-art,
#   backing music, scanline skin, เมนูเลือกโหมดบนจอ (เลือกผ่านตัวแปร MODE แทน).
#
# step นี้เราทำอะไร: เกมเดิม แต่คราวนี้ "ปรับความยากได้" โหมดต่างกันเปลี่ยนจังหวะ
# ปล่อยศัตรู ความเร็วตก และกติกาเสียชีวิต. ศัตรูทยอยมาเป็น "คลื่น" ไม่ตกพร้อมกัน
# หมดทีเดียว เกมเลยมีจังหวะเหมือนเกมยิงจริง. ลองเปลี่ยน MODE เป็น 0/1/2 ดูความต่างกันนะ
#
# ส่วนที่คุณจะเขียนเองใน step นี้ (ต่อจาก step4):
#   1) ตารางโหมด + เลือกค่า spawn_delay / speed_mul / lives / lose_when_pass / lose_when_hit
#   2) spawn timer: ปล่อยศัตรูทีละตัวจาก "บ่อจอด" ตามจังหวะ (ไม่ใช่ตกพร้อมกันหมด)
#   3) ยานชนศัตรู -> เสียชีวิต (ยกเว้นโหมด FREE) + hitbox หดเท่ากับ C
# Core 70% ที่เรียกใช้: (เดิมทั้งหมด) game.start/Box/Text/keys/hit/sfx/run
# C step == Python step บนจอ: ความยากเปลี่ยนจังหวะ+ความเร็วศัตรู, ตรรกะเสียชีวิตเดียวกัน
# อ้างอิงเกมจริง: page_game_shooter.c:85-89 (modes), :249-268 (spawn), :358-454 (step)
# ------------------------------------------------------------------------------
import bentogame as game
import random

ACCEL, MAX_SPEED, FRICTION = 1.4, 13.0, 0.80
MAX_BULLETS, MAX_ENEMIES = 6, 8                 # บ่อกระสุน 6, บ่อศัตรู 8 (เท่า C :38)
ENEMY_COLORS = [game.RED, game.ORANGE, game.PINK]

# hitbox "หด" ให้ตรงกับ C step5 (bp_hit ใช้ขนาดเล็กกว่ากล่องจริง): กระสุน 4x10,
# ศัตรู 26x16 — ยานใช้ขนาดเต็ม 62x24 (page_game_shooter.c:415-416, :437)
BULLET_HITBOX = (4, 10)
ENEMY_HITBOX  = (26, 16)

def boxes_overlap(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    """ชน AABB ด้วยขนาดที่กำหนดเอง (เท่ากับ bp_hit ฝั่ง C) — เพื่อ hitbox หดให้ตรง
    a_* = กล่องแรก, b_* = กล่องที่สอง: ซ้อนกันเมื่อทุกด้านเหลื่อมกัน"""
    return (a_x < b_x + b_width and a_x + a_width > b_x and
            a_y < b_y + b_height and a_y + a_height > b_y)

# ----- เติมส่วนนี้เอง (งานของคุณ) (1): สร้างตารางโหมด 3 ระดับ -----
#   ตาราง MODES = list ของ tuple 6 ช่อง:
#   (ชื่อ, spawn_delay, speed_mul, lives, lose_when_pass, lose_when_hit)
# TODO ทำตามขั้น:
#   1) เก็บแถว FREE ตัวอย่างไว้ (รันได้แล้ว) — มันคือโหมดฝึกมือ ไม่มีอะไรลงโทษ
#   2) เพิ่มแถว EASY: spawn ห่างขึ้น (ปล่อยช้าลง), speed_mul < 1 (ช้าลง), ชีวิตน้อยลง,
#      lose_when_pass=False แต่ lose_when_hit=True (ชนยานเสีย แต่หลุดล่างไม่เสีย)
#   3) เพิ่มแถว DIFFICULT: spawn ถี่ที่สุด, speed_mul สูงสุด, ชีวิตน้อยสุด,
#      lose_when_pass=True และ lose_when_hit=True (โหดทั้งสองทาง)
#   ค่าตัวเลขปรับเอาเองให้รู้สึก "ยากขึ้นเป็นชั้น" (ดู starter ถ้าอยากเทียบค่า)
MODES = [
    ("FREE SHOOTER", 16, 0.85, 99, False, False),  # ตัวอย่างไว้ 1 แถวให้รันได้ก่อน เดี๋ยวคุณเพิ่ม EASY/DIFFICULT เอง
]
MODE = 0                                        # เลือกโหมด (0/1/2) — C เลือกผ่านเมนูบนจอ
MODE_NAME, SPAWN_DELAY, SPEED_MUL, START_LIVES, LOSE_WHEN_PASS, LOSE_WHEN_HIT = MODES[MODE]

game.title("SHOOTER")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

ship = game.Box(365, 352, 62, 24, game.GREEN)
ship_x, ship_speed = 365.0, 0.0
score, lives, fire_cooldown = 0, START_LIVES, 0
spawn_timer = 8                                  # ตัวนับจังหวะปล่อยศัตรู
hud = game.Text("%s   Score: 0   Lives: %d" % (MODE_NAME, lives), 10, 8, game.WHITE)

bullets = [game.Box(0, -50, 6, 14, game.CYAN) for _ in range(MAX_BULLETS)]
for bullet in bullets:
    bullet.hide()

# ศัตรูเริ่มจอด "ซ่อน" ทั้งหมด แล้วปล่อยทีละตัวเป็นคลื่น (enemy_active[] = ลอยอยู่ไหม)
enemies = [game.Box(0, -50, 30, 24, ENEMY_COLORS[0]) for _ in range(MAX_ENEMIES)]
for enemy in enemies:
    enemy.hide()
enemy_active = [False] * MAX_ENEMIES
enemy_speed = [0.0] * MAX_ENEMIES

def find_free_bullet():
    for bullet in bullets:
        if bullet.y < -20:
            return bullet
    return None

def spawn_enemy():
    # ----- เติมส่วนนี้เอง (งานของคุณ) (2): ปล่อยศัตรู 1 ตัวจากบ่อจอด -----
    # ทำตามขั้น:
    #   1) วน index ใน range(MAX_ENEMIES) หาตัวแรกที่ enemy_active[index] เป็น False
    #   2) ตั้ง enemy_active[index] = True (จองตัวนั้นว่า "ลอยอยู่")
    #   3) สุ่มสีปล่อยมัน: ใช้ .set_color(...) กับ random.choice(ENEMY_COLORS)
    #   4) วางมันไว้บนสุดนอกจอ: ใช้ .move_to(...) — x สุ่ม (random.randint) ให้อยู่ในจอ, y ติดลบ (ยังไม่โผล่)
    #   5) เรียก .show() ให้มองเห็น
    #   6) ตั้ง enemy_speed[index] = ความเร็วสุ่ม (random.uniform) คูณ SPEED_MUL ของโหมด
    #   7) return ออกทันที (ปล่อยแค่ตัวเดียวต่อการเรียก 1 ครั้ง)
    # (ช่วงตัวเลขความเร็ว/ขอบ x ปรับเอง — ดู starter ถ้าติด)
    pass   # <- ลบ pass ออกเมื่อเริ่มเขียน

def park_enemy(index):
    enemy_active[index] = False
    enemies[index].hide()
    enemies[index].move_to(0, -50)

# ปล่อยคลื่นแรก 3 ตัว (เหมือน C shooter_start :347-349)
spawn_enemy(); spawn_enemy(); spawn_enemy()

def on_frame():
    global ship_x, ship_speed, score, lives, fire_cooldown, spawn_timer
    keys = game.keys()
    # (Back=ออก / Start=เริ่มใหม่ — game.run() จัดการให้)

    # spawn timer — ปล่อยศัตรูเป็นคลื่นตามจังหวะของโหมด (:362-368)
    if spawn_timer > 0:
        spawn_timer -= 1
    else:
        spawn_enemy()
        spawn_timer = SPAWN_DELAY

    # ยาน
    if keys.left:    ship_speed -= ACCEL
    elif keys.right: ship_speed += ACCEL
    else:            ship_speed *= FRICTION
    ship_speed = max(-MAX_SPEED, min(MAX_SPEED, ship_speed))
    ship_x = max(0, min(game.WIDTH - ship.w, ship_x + ship_speed))
    ship.move_to(ship_x, 352)

    # ยิง
    fire_cooldown = max(0, fire_cooldown - 1)
    if (keys.a or keys.up) and fire_cooldown == 0:
        bullet = find_free_bullet()
        if bullet:
            bullet.show(); bullet.move_to(ship_x + ship.w // 2 - 3, 340); game.sfx("fire"); fire_cooldown = 8
    for bullet in bullets:
        if bullet.y >= -20:
            bullet.move_to(bullet.x, bullet.y - 9)
            if bullet.y < -20: bullet.hide()

    # ศัตรู + ชน + คะแนน + ชีวิต (ตรรกะเดียวกับ C :388-454)
    for index in range(MAX_ENEMIES):
        if not enemy_active[index]:
            continue
        enemy = enemies[index]
        enemy.move_to(enemy.x, enemy.y + enemy_speed[index])
        if enemy.y > game.HEIGHT:               # หลุดล่าง
            park_enemy(index)
            if LOSE_WHEN_PASS:                  # เฉพาะ DIFFICULT ที่หลุดล่างแล้วเสียชีวิต
                lives -= 1
                hud.set("%s   Score: %d   Lives: %d" % (MODE_NAME, score, lives))
                if lives <= 0:
                    game.sfx("gameover")
                    game.Text("GAME OVER", 320, 180, game.RED)
                    return False
            continue

        # กระสุน x ศัตรู (hitbox หด — เท่ากับ C :414-416)
        enemy_box = (enemy.x, enemy.y, ENEMY_HITBOX[0], ENEMY_HITBOX[1])
        was_hit = False
        for bullet in bullets:
            if bullet.y >= -20 and boxes_overlap(bullet.x, bullet.y, BULLET_HITBOX[0], BULLET_HITBOX[1], *enemy_box):
                score += 1
                game.sfx("hit")
                hud.set("%s   Score: %d   Lives: %d" % (MODE_NAME, score, lives))
                bullet.move_to(0, -50); bullet.hide()
                park_enemy(index)
                was_hit = True
                break
        if was_hit:
            continue

        # ----- เติมส่วนนี้เอง (งานของคุณ) (3): ยานชนศัตรู แล้วเสียชีวิต (ยกเว้นโหมด FREE) -----
        # ทำตามขั้น (เทียบ enemy_box ที่เตรียมไว้ด้านบน):
        #   1) เช็คยานชนศัตรูด้วย boxes_overlap(...) — กล่องยานคือ ship_x, ตำแหน่ง y ของยาน,
        #      ขนาด ship.w/ship.h, แล้วกาง *enemy_box เป็นกล่องที่สอง
        #   2) ถ้าชน: เรียก park_enemy(index) เก็บศัตรูกลับบ่อจอด
        #   3) ถ้าโหมดนี้ลงโทษ (LOSE_WHEN_HIT): ลด lives ลง 1 แล้วอัปเดต hud ด้วย hud.set(...)
        #   4) ถ้า lives หมด (<= 0): เล่น game.sfx("gameover"), โชว์ game.Text("GAME OVER", ...) แล้ว return False
        #   5) ถ้ายังไม่หมดชีวิต: เล่นเสียงระเบิด game.sfx("explode")
        # (FREE ไม่ลงโทษ เพราะ LOSE_WHEN_HIT=False — ปล่อยให้ if ข้ามไปเอง)
        pass   # <- ลบ pass ออกเมื่อเริ่มเขียน

game.run(on_frame, fps=30)
