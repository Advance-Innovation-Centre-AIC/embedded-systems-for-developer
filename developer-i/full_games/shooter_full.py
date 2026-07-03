# shooter_full.py — Space Shooter ฉบับอ้างอิง (เกมเต็ม)
# หน้าตาและจังหวะลอกมาจากเกม C บนเครื่อง (page_game_shooter.c) ให้ตรงที่สุด:
#   - ยานสไปรต์ลำเดียวกับเกม C บินอิสระ 2 แกน กดค้างแล้วเร่ง ปล่อยแล้วไถล
#   - ศัตรู 3 แบบ (invader ม่วง / UFO เงิน / demon แดง) สุ่มชนิดตอนเกิด
#   - กระสุนติดโมเมนตัมของยาน — สไลด์ไปยิงไป กระสุนจะพุ่งเฉียงตามแรงยาน
#   - ยิงโดนแล้ว "บึ้ม" เป็นภาพระเบิด 2 เฟรม สีตามชนิดศัตรู พร้อมเสียงครบทุกจังหวะ
#   - โหมด FREE SHOOTER / EASY / DIFFICULT ค่าตัวเลขชุดเดียวกับเกม C
# ปุ่ม: ซ้าย/ขวา/ขึ้น/ลง = ขับยาน   A = ยิง (กดทีละนัด กดค้างไม่รัว)
#       Y = เริ่มโหมดเดิมใหม่ทันที   Start = พักเกม   Back = ออก

import bentogame as game
import random

# ---- ค่าคงที่ยกมาจากเกม C (page_game_shooter.c) ----------------------------
SHIP_W, SHIP_H = 62, 28                  # ขนาดสไปรต์ยาน
SHIP_Y_MIN     = 24                      # เพดานบนที่ยานบินถึง
SHIP_Y_HOME    = game.HEIGHT - SHIP_H - 32   # ตำแหน่งพัก (ล่างสุดของสนาม)
ACCEL, MAXV, FRICTION = 1.4, 13.0, 0.80  # ฟิสิกส์ยาน — ชุดเดียวกับเกม C เป๊ะ
BULLET_VY      = 8.0                     # ความเร็วกระสุน (ขึ้น)
BULLET_INHERIT = 0.55                    # สัดส่วนโมเมนตัมยานที่กระสุนพกไปด้วย
BOOM_TICKS     = 6                       # ระเบิดค้างบนจอกี่เฟรม

# งบ widget: จอมีได้สูงสุด 32 ชิ้นรวมทุกอย่าง เกม C ตัวจริงเปิดพร้อมกันได้ถึง
# ดาว 24 + ศัตรู 8 + กระสุน 6 + ระเบิด 4 ซึ่งเกินงบฝั่ง Python
# ตัวเกม (ศัตรู/กระสุน) สำคัญกว่าฉากหลัง — เลยคงจำนวนศัตรูกับกระสุนของเกม C
# ไว้ครบทุกตัว แล้วไปหักที่ดาวประดับแทน (ความยากจะได้เท่าเกม C จริงๆ):
#   พื้นหลัง 1 + ดาว 5 + ยาน 1 + ศัตรู 8 + กระสุน 6 + ระเบิด 3 + HUD 1 = 25
#   + ป้ายบอกปุ่มของ run() 1 (ป้าย PAUSED ยืมป้ายนี้ ไม่กินงบเพิ่ม) = 26
#   + ป้าย game over ชั่วคราวอีก 4 = 30  — ยังไม่ชนเพดาน 32
EMAX, BMAX, BOOMMAX, STARS = 5, 4, 3, 5   # จุดสมดุล: object น้อยพอให้ลื่น แต่ยังมี action

LASER = 0x80F4FF                         # สีลำแสงฟ้า (สีเดียวกับกระสุนเกม C)

# ตารางโหมดของเกม C: (ชื่อ, เว้นกี่เฟรมค่อยปล่อยศัตรู, ตัวคูณความเร็วตก,
#                     ชีวิตเริ่มต้น, หลุดขอบล่างเสียชีวิตไหม, ชนยานเสียชีวิตไหม)
MODES = (
    ("FREE SHOOTER", 16, 0.85, 99, False, False),   # ยิงเล่นเพลินๆ ไม่มีบทลงโทษ
    ("EASY",         26, 0.70,  5, False, True),    # ศัตรูห่างและช้า หลุดล่างไม่เป็นไร
    ("DIFFICULT",    12, 1.00,  3, True,  True),    # โจทย์ดั้งเดิมของเกม C
)

ENEMY_SPR   = ("enemy", "enemy2", "enemy3")          # invader / UFO / demon
BOOM_FRAMES = (("boom1", "boom2"),                   # ระเบิดม่วง (invader)
               ("boom3", "boom4"),                   # ระเบิดฟ้า (UFO)
               ("boom5", "boom6"))                   # ระเบิดไฟ (demon)


def overlap(ax, ay, aw, ah, ox, oy, ow, oh):
    # กล่องชนกล่อง (สูตรเดียวกับ shooter_overlap ของเกม C)
    return not (ax + aw < ox or ax > ox + ow or ay + ah < oy or ay > oy + oh)


game.title("SHOOTER", melody=True)       # หน้าเริ่ม: Start=เล่น Back=ออก

mode = 2                                 # เกม C เปิดมาชี้ DIFFICULT เป็นค่าเริ่มต้น
restart_same = False                     # ปุ่ม Y = เล่นโหมดเดิมซ้ำโดยไม่ผ่านเมนู
while True:
    if not restart_same:
        picked = game.menu("FREE SHOOTER", "EASY", "DIFFICULT", selected=mode)
        if picked is None:               # BACK จากหน้าเมนู = เลิกเล่น (เหมือนเกม C)
            break
        mode = picked
    restart_same = False
    mode_name, spawn_gap, vy_mul, lives0, pass_costs, collide_costs = MODES[mode]

    # ---- จัดฉาก (ทำใหม่ทุกรอบที่เริ่มเล่น) — สร้าง widget ครั้งเดียว ห้ามสร้างใน update()
    game.background(0x10122C)            # อวกาศน้ำเงินเข้ม สีเดียวกับสนามเกม C
    game.starfield(STARS, 0xB8C0E0)      # ดาวจางๆ โปรยไว้ก่อนตัวละคร จะได้อยู่ชั้นหลัง
    ship = game.Sprite("ship", 0, 0)
    # กระสุนเกม C เป็นแท่งฟ้าขอบขาวมุมมน — Box ส่งขอบ/มุมให้จอได้ตรงๆ เลย
    bullets = [game.Box(-20, -50, 5, 12, LASER, border=0xFFFFFF, radius=2)
               for _ in range(BMAX)]
    for b in bullets:
        b.hide()
    enemies = game.pool("enemy", EMAX)   # เปลี่ยนหน้าตาเป็นชนิดที่สุ่มได้ตอนเกิด
    booms   = game.pool("boom1", BOOMMAX)
    hud = game.Text("", 10, 8, game.WHITE)

    st = {"sx": (game.WIDTH - SHIP_W) / 2.0, "sy": float(SHIP_Y_HOME),
          "svx": 0.0, "svy": 0.0,
          "score": 0, "lives": lives0, "spawn": 8,
          "msg": "GAME OVER", "restart": False}
    bact = [False] * BMAX                # กระสุน: ใช้งานอยู่ไหม + ตำแหน่ง + แรงเฉียง
    bx, by, bvx = [0.0] * BMAX, [0.0] * BMAX, [0.0] * BMAX
    eact = [False] * EMAX                # ศัตรู: ใช้งานอยู่ไหม + ตำแหน่ง + ความเร็ว + ชนิด
    ex, ey, evy = [0.0] * EMAX, [0.0] * EMAX, [0.0] * EMAX
    ekind = [0] * EMAX
    boom_t, boom_k = [0] * BOOMMAX, [0] * BOOMMAX
    hud_last = [None]

    def hud_update():
        # วาด HUD เฉพาะตอนตัวเลขเปลี่ยน (แบบเดียวกับเกม C — จอนิ่งกว่าและประหยัดงาน)
        row = (st["score"], max(game.best("shooter"), st["score"]), st["lives"])
        if row != hud_last[0]:
            hud_last[0] = row
            hud.set("Score: %d    Best: %d    Lives: %d" % row)

    def set_ship(x, y):
        # ชนขอบสนามแล้วหยุดความเร็วแกนนั้นทิ้ง — ยานจะได้ไม่ "อัด" ขอบด้วยแรงค้าง
        if x < 0:
            x = 0.0
            st["svx"] = 0.0
        if x > game.WIDTH - SHIP_W:
            x = float(game.WIDTH - SHIP_W)
            st["svx"] = 0.0
        if y < SHIP_Y_MIN:
            y = float(SHIP_Y_MIN)
            st["svy"] = 0.0
        if y > SHIP_Y_HOME:
            y = float(SHIP_Y_HOME)
            st["svy"] = 0.0
        st["sx"], st["sy"] = x, y
        ship.move_to(x, y)

    def reset_bullet(j):
        bact[j] = False
        bullets[j].hide()

    def reset_enemy(i):
        eact[i] = False
        enemies[i].hide()

    def spawn_enemy():
        # หาช่องว่างในพูล แล้วส่งศัตรูชนิดสุ่มลงมาจากขอบบน (ช่วงตัวเลขตามเกม C)
        for i in range(EMAX):
            if not eact[i]:
                eact[i] = True
                ex[i] = float(random.randint(20, game.WIDTH - 46))
                ey[i] = -20.0
                evy[i] = random.randint(18, 34) / 10.0 * vy_mul
                ekind[i] = random.randint(0, 2)
                enemies[i].frame(ENEMY_SPR[ekind[i]])
                enemies[i].move_to(ex[i], ey[i])
                enemies[i].show()
                return

    def fire():
        # ยิงจากหัวยาน ณ ตำแหน่งปัจจุบัน + พกโมเมนตัมแนวนอนของยานไปด้วย
        for j in range(BMAX):
            if not bact[j]:
                bact[j] = True
                game.sfx("fire")
                bx[j] = st["sx"] + SHIP_W / 2.0 - 2.0
                by[j] = st["sy"] - 8.0
                bvx[j] = st["svx"] * BULLET_INHERIT
                bullets[j].move_to(bx[j], by[j])
                bullets[j].show()
                return

    def boom(cx, cy, kind):
        # เกม C เล่นคลิประเบิดอัดเสียงจริง — ฝั่ง Python ใช้เสียง synth ที่ใกล้ที่สุด
        game.sfx("explode")
        for b in range(BOOMMAX):
            if boom_t[b] == 0:
                boom_t[b] = BOOM_TICKS
                boom_k[b] = kind
                booms[b].frame(BOOM_FRAMES[kind][0])
                booms[b].move_to(cx - 15, cy - 12)   # จัดกึ่งกลางภาพระเบิด 29x24
                booms[b].show()
                return

    def step_booms():
        for b in range(BOOMMAX):
            if boom_t[b] == 0:
                continue
            boom_t[b] -= 1
            if boom_t[b] == 0:
                booms[b].hide()
            elif boom_t[b] == BOOM_TICKS // 2:       # ครึ่งหลังสลับเป็นเฟรมบึ้มวงใหญ่
                booms[b].frame(BOOM_FRAMES[boom_k[b]][1])

    def update():
        k = game.keys()
        if game.pressed_once("y", k):    # Y = เริ่มโหมดเดิมใหม่ทันที (เหมือนเกม C)
            st["restart"] = True
            return False

        # ขับยาน 2 แกน: กดค้าง = เร่งขึ้นเรื่อยๆ จนชนเพดานความเร็ว ปล่อย = ไถลจนหยุด
        if k.left and not k.right:
            st["svx"] -= ACCEL
        elif k.right and not k.left:
            st["svx"] += ACCEL
        else:
            st["svx"] *= FRICTION
        if k.up and not k.down:
            st["svy"] -= ACCEL
        elif k.down and not k.up:
            st["svy"] += ACCEL
        else:
            st["svy"] *= FRICTION
        st["svx"] = max(-MAXV, min(MAXV, st["svx"]))
        st["svy"] = max(-MAXV, min(MAXV, st["svy"]))
        set_ship(st["sx"] + st["svx"], st["sy"] + st["svy"])

        if game.pressed_once("a", k):    # ยิงทีละนัดตามจังหวะกด — กดค้างไม่รัว
            fire()

        # นาฬิกาปล่อยศัตรู — ยิ่งโหมดยากยิ่งถี่ (spawn_gap ของโหมด)
        if st["spawn"] > 0:
            st["spawn"] -= 1
        else:
            spawn_enemy()
            st["spawn"] = spawn_gap

        # กระสุน: พุ่งขึ้น + เฉียงตามโมเมนตัมที่ติดมา หลุดขอบไหนก็เก็บกลับพูล
        for j in range(BMAX):
            if not bact[j]:
                continue
            by[j] -= BULLET_VY
            bx[j] += bvx[j]
            if by[j] < -12 or bx[j] < -12 or bx[j] > game.WIDTH:
                reset_bullet(j)
                continue
            bullets[j].move_to(bx[j], by[j])

        # ศัตรู: ตกลงมาเรื่อยๆ แล้วเช็คชนครบทุกแบบเหมือนเกม C
        for i in range(EMAX):
            if not eact[i]:
                continue
            ey[i] += evy[i]
            enemies[i].move_to(ex[i], ey[i])

            # หลุดขอบล่าง — โหมด DIFFICULT เท่านั้นที่เสียชีวิต (ตามตารางโหมด)
            if ey[i] > game.HEIGHT:
                reset_enemy(i)
                if pass_costs:
                    st["lives"] -= 1
                    if st["lives"] <= 0:
                        game.sfx("gameover")
                        st["msg"] = "Base destroyed"
                        return False
                continue

            # กระสุนโดนศัตรู — บึ้มสีตามชนิด ได้แต้ม แล้วส่งตัวใหม่ลงมาแทนทันที
            got = False
            for j in range(BMAX):
                if bact[j] and overlap(bx[j], by[j], 4, 10, ex[i], ey[i], 26, 16):
                    boom(ex[i] + 13, ey[i] + 8, ekind[i])
                    reset_bullet(j)
                    reset_enemy(i)
                    got = True
                    game.sfx("hit")      # เสียงยืนยันยิงโดน ซ้อนบนเสียงระเบิด
                    st["score"] += 1
                    spawn_enemy()
                    break
            if got:
                continue

            # ศัตรูชนยาน — บึ้มเหมือนกัน โหมด FREE ยานอึดไม่เสียชีวิต
            if overlap(st["sx"], st["sy"], SHIP_W, SHIP_H, ex[i], ey[i], 26, 16):
                boom(ex[i] + 13, ey[i] + 8, ekind[i])
                reset_enemy(i)
                if collide_costs:
                    st["lives"] -= 1
                    if st["lives"] <= 0:
                        game.sfx("gameover")
                        st["msg"] = "Ship destroyed"
                        return False
                    game.sfx("lose_life")   # รอดมาได้แต่เจ็บ — เสียงเตือนเสียชีวิต

        step_booms()
        hud_update()

    set_ship(st["sx"], st["sy"])
    for _ in range(3):                   # เกม C เปิดฉากด้วยศัตรู 3 ตัวแรกเสมอ
        spawn_enemy()
    hud_update()

    if not game.run(update, fps=50):     # 50 เฟรม/วิ = จังหวะ 20 ms เดียวกับเกม C
        game.save_best(st["score"], "shooter")   # Back กลางเกม: คะแนนดีๆ ไม่หาย
        break                            # Back = เลิกเล่น
    if st["restart"]:                    # Y = วนกลับไปเริ่มโหมดเดิมทันที
        game.save_best(st["score"], "shooter")   # Best ต้องไม่หายไปกับตาที่กด Y ทิ้ง
        game.replay()
        restart_same = True
        continue
    if not game.game_over(st["score"], name="shooter", msg=st["msg"]):
        break                            # Start = เล่นใหม่ (เลือกโหมดได้อีกครั้ง) / Back = ออก
