# โครงเว้น 30% — ส่วนที่คุณต้องเติมเอง / เฉลย: starter/shooter_step3.py
# ใบ้: ดูในใบงาน session
# shooter_step3.py — สร้าง Shooter #3 (คาบ 16): ยิงกระสุนด้วย "บ่อกระสุน" (bullet pool)
# ------------------------------------------------------------------------------
# step นี้คือหัวใจของบทเรียน: REUSE-DON'T-CREATE (อย่าสร้าง object ใหม่ใน loop)
# แทนที่จะ "เกิด" กระสุนใหม่ทุกครั้งที่ยิง ซึ่งช้าและกินหน่วยความจำ
# เราเตรียมกระสุนไว้ล่วงหน้าเป็น "บ่อ" (pool) แล้วหยิบอันที่ว่างมายิง พอยิงเสร็จ
# ก็คืนกลับบ่อ เหมือนยืม-คืนปากกาในกล่อง. กด A แล้วเลเซอร์พุ่งขึ้น เล่นสนุกขึ้นเยอะ
# Core 70% ที่เพิ่งได้ใช้: bullet.show()/bullet.hide() กับ game.sfx("fire")
# C step ได้ผลเท่ากับ Python step บนจอ: ยิง A แล้วเลเซอร์พุ่งขึ้น, ยิงได้หลายนัด, กระสุนวนใช้ซ้ำ
#   (เทียบ shooter_step3.c — shooter_fire() กับ reset/move loop เดียวกัน, cap 6 เท่ากัน)
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

# บ่อกระสุน — สร้างครั้งเดียว แล้วจอดซ่อนไว้ (KEEP: นี่คือ REUSE-DON'T-CREATE)
bullets = [game.Box(0, -50, 6, 14, game.CYAN) for _ in range(MAX_BULLETS)]
for bullet in bullets:
    bullet.hide()

# หากระสุนว่างมาใช้ซ้ำ (จอดอยู่ = y < -20)
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

    # ----- เติมส่วนนี้เอง (งานของคุณ): ยิงกระสุน (มี cooldown กันยิงรัว) -----
    # 1) ทุกเฟรมให้ลด fire_cooldown ลงทีละ 1 แต่อย่าให้ติดลบ (ใช้ max(0, ...)).
    # 2) เช็คว่ากดยิงไหม: กด A (keys.a) หรือดันขึ้น (keys.up) "และ" fire_cooldown == 0.
    # 3) ถ้าใช่ -> ขอกระสุนว่างด้วย find_free_bullet(); ถ้าได้ (ไม่ใช่ None):
    #    3.1 โผล่กระสุนด้วย .show()
    #    3.2 ย้ายไปที่หัวยานด้วย .move_to(x, y) — x = กึ่งกลางลำยาน, y = เหนือยานเล็กน้อย
    #    3.3 เล่นเสียงยิงด้วย game.sfx("fire")
    #    3.4 ตั้ง fire_cooldown เป็นค่าหน่วง (ลองปรับเอง — มากไป=ยิงช้า, น้อยไป=รัว / ดู starter ถ้าติด)
    pass   # <- ลบ pass ออกเมื่อเริ่มเขียน

    # ----- เติมส่วนนี้เอง (งานของคุณ): เลื่อนกระสุนขึ้น, พ้นจอแล้วจอดกลับบ่อ -----
    # 1) วนทุกกระสุน: for bullet in bullets:
    # 2) ถ้ากระสุนยัง "ลอยอยู่" (bullet.y >= -20) ให้ขยับขึ้นด้วย .move_to(x, y)
    #    โดย x คงเดิม ส่วน y ลดลงทีละน้อยทุกเฟรม = พุ่งขึ้น (เลือกระยะเอง — มาก=เร็ว)
    # 3) หลังขยับ ถ้ามันพ้นจอบนแล้ว (bullet.y < -20) ให้ .hide() คืนกลับบ่อ
    pass   # <- ลบ pass ออกเมื่อเริ่มเขียน
    # -----------------------------------------------------------------------

game.run(on_frame, fps=30)
