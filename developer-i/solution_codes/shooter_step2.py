# shooter_step2.py — สร้าง Shooter #2 (คาบ 15): บังคับยานซ้าย/ขวา (เร่ง + ลื่น)
# ------------------------------------------------------------------------------
# step นี้เราจะทำให้ยาน "ขับได้" เหมือนรถบนน้ำแข็ง คือกดค้างไว้แล้วยิ่งเร็วขึ้น
# (เร่ง/accel) พอปล่อยมือก็ค่อย ๆ ลื่นช้าลง (ฝืด/friction) นี่เป็นฟิสิกส์เกมง่าย ๆ
# ที่ทำให้การบังคับรู้สึกมีน้ำหนักและคุมสนุกขึ้น
# Core 70% ที่เพิ่งได้ใช้: game.keys()  (อ่านปุ่ม/จอย)
# C step == Python step บนจอ: ยานเร่ง-ลื่น-ชนขอบหยุด เหมือนกัน
#   (เทียบ shooter_step2.c — ตรรกะ accel/friction/clamp เดียวกัน)
# อ้างอิงเกมจริง: reference/shooter_full.py:42-47 ; page_game_shooter.c:505-524 (svel)
# ------------------------------------------------------------------------------
import bentogame as game

ACCEL, MAX_SPEED, FRICTION = 1.4, 13.0, 0.80  # ค่าฟิสิกส์เดียวกับเกมจริง (:43-45)

game.title("SHOOTER")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

ship = game.Box(365, 352, 62, 24, game.GREEN)
ship_x, ship_speed = 365.0, 0.0               # ตำแหน่ง x + ความเร็วของยาน
score, lives = 0, 3
hud = game.Text("Score: 0   Lives: 3", 10, 8, game.WHITE)

def on_frame():
    global ship_x, ship_speed
    keys = game.keys()
    # ปุ่มออก/เริ่มใหม่ เอนจินจัดการเอง: Back = ออก · Start = เริ่มใหม่

    # ----- เติมส่วนนี้เอง: ฟิสิกส์การเคลื่อนที่ของยาน -----
    if keys.left:    ship_speed -= ACCEL      # กดซ้าย = เร่งไปทางซ้าย
    elif keys.right: ship_speed += ACCEL      # กดขวา = เร่งไปทางขวา
    else:            ship_speed *= FRICTION   # ปล่อย = ค่อย ๆ ช้าลง (ลื่น)
    ship_speed = max(-MAX_SPEED, min(MAX_SPEED, ship_speed))   # จำกัดความเร็วสูงสุด
    ship_x = max(0, min(game.WIDTH - ship.w, ship_x + ship_speed))  # ขยับ + อยู่ในจอ
    ship.move_to(ship_x, 352)
    # -----------------------------------------------------------------------

game.run(on_frame, fps=30)
