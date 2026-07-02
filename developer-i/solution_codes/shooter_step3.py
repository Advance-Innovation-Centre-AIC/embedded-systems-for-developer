# shooter_step3.py — สร้าง Shooter #3 (คาบ 16): ยิงกระสุน = "บ่อกระสุน" (bullet pool)
# ------------------------------------------------------------------------------
# step นี้คือหัวใจของบทเรียน: REUSE-DON'T-CREATE (อย่าสร้าง object ใน loop)
# เรื่องราว: แทนที่จะ "เกิด" กระสุนใหม่ทุกครั้งที่ยิง (ช้า และกินหน่วยความจำ)
# เราเตรียมกระสุนไว้ล่วงหน้าเป็น "บ่อ" (pool) แล้วหยิบอันที่ว่างมายิง พอยิงเสร็จ
# ก็คืนกลับบ่อ เหมือนยืม-คืนปากกาในกล่อง. กด A แล้วเลเซอร์พุ่งขึ้น
# Core 70% ที่เพิ่งได้ใช้: bullet.show()/bullet.hide()  +  game.sfx("fire")
# C step == Python step บนจอ: ยิง A -> เลเซอร์พุ่งขึ้น, ยิงได้หลายนัด, กระสุนวนใช้ซ้ำ
#   (เทียบ shooter_step3.c — shooter_fire() + reset/move loop เดียวกัน, cap 6 เท่ากัน)
# อ้างอิงเกมจริง: reference/shooter_full.py:19-30,49-59 ; page_game_shooter.c:270-290,372-385
# ------------------------------------------------------------------------------
import bentogame as game

ACCEL, MAX_SPEED, FRICTION = 1.4, 13.0, 0.80
MAX_BULLETS = 6                                 # ขนาดบ่อกระสุน (เท่าเกมจริง :37)

game.title("SHOOTER")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

ship = game.Box(365, 352, 62, 24, game.GREEN)
ship_x, ship_speed, fire_cooldown = 365.0, 0.0, 0
score, lives = 0, 3
hud = game.Text("Score: 0   Lives: 3", 10, 8, game.WHITE)

# ----- เติมส่วนนี้เอง (1): บ่อกระสุน สร้างครั้งเดียว แล้วจอดซ่อนไว้ -----
bullets = [game.Box(0, -50, 6, 14, game.CYAN) for _ in range(MAX_BULLETS)]
for bullet in bullets:
    bullet.hide()

# ----- เติมส่วนนี้เอง (2): หากระสุนว่างมาใช้ซ้ำ (จอดอยู่ = y < -20) -----
def find_free_bullet():
    for bullet in bullets:
        if bullet.y < -20:
            return bullet
    return None

def on_frame():
    global ship_x, ship_speed, fire_cooldown
    keys = game.keys()
    # (Back=ออก / Start=เริ่มใหม่ — game.run() จัดการให้)

    # ยาน (จาก step2)
    if keys.left:    ship_speed -= ACCEL
    elif keys.right: ship_speed += ACCEL
    else:            ship_speed *= FRICTION
    ship_speed = max(-MAX_SPEED, min(MAX_SPEED, ship_speed))
    ship_x = max(0, min(game.WIDTH - ship.w, ship_x + ship_speed))
    ship.move_to(ship_x, 352)

    # ----- เติมส่วนนี้เอง (3): ยิง (มี cooldown กันยิงรัว) -----
    fire_cooldown = max(0, fire_cooldown - 1)
    if (keys.a or keys.up) and fire_cooldown == 0:
        bullet = find_free_bullet()
        if bullet:
            bullet.show()
            bullet.move_to(ship_x + ship.w // 2 - 3, 340)   # ออกจากหัวยาน
            game.sfx("fire")                       # เสียงยิงจาก C engine จริง
            fire_cooldown = 8                      # หน่วง 8 เฟรมก่อนยิงนัดถัดไป

    # ----- เติมส่วนนี้เอง (4): เลื่อนกระสุนขึ้น, พ้นจอ -> จอดกลับ -----
    for bullet in bullets:
        if bullet.y >= -20:
            bullet.move_to(bullet.x, bullet.y - 9)
            if bullet.y < -20:
                bullet.hide()
    # -----------------------------------------------------------------------

game.run(on_frame, fps=30)
