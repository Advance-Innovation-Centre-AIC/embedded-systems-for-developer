# snake_full.py — REFERENCE build of the classic Snake (Game Boy palette).
# This is the target students rebuild step-by-step in Block B. Faithful to the
# on-board C game (page_game_snake.c): grass-field arena, RELAXED/CLASSIC/TURBO
# mode picker, Score/Best/Len HUD, edge-triggered turns, eat/coin sounds,
# die/lose sounds แยกชนกำแพง/กัดตัวเอง, Y = เริ่มตาใหม่โหมดเดิมทันที,
# and Start = play again without rebooting MicroPython.

import bentogame as game
import random
import time

CELL = 16                    # ขนาดช่องเท่าเกม C เป๊ะ (SNAKE_CELL_PX = 16px)
COLS = game.WIDTH // CELL    # 49 คอลัมน์ (เกม C โหมดจอยได้ 45 — ใกล้กันมาก)
ROWS = game.HEIGHT // CELL   # 24 แถว (เท่าเกม C)

# ชื่อโหมด + คาบเวลาเกมเดิน 1 ก้าว (ms) — ตัวเลขชุดเดียวกับตาราง s_snake_modes ในเกม C
# ความยากของงูคือ "จังหวะก้าว" ล้วนๆ: ก้าวถี่ขึ้น = ตัดสินใจต้องไวขึ้น
MODES = (("RELAXED", 150), ("CLASSIC", 115), ("TURBO", 70))

# งบวิดเจ็ตของจอมี 32 ชิ้น แบ่งแบบนี้: ฉาก 8 (พื้น 1 + แถบหญ้า 4 + แอปเปิล 1
# + HUD 1 + ป้ายปุ่มของ game.run อีก 1 — ป้ายพักยืมป้ายนี้ ไม่กินงบเพิ่ม)
# + ป้าย game over ชั่วคราว 4 = 12  เหลือให้ตัวงู 19 ช่อง (หัว 1 + ลำตัว 18)
# รวมพีค 31 ยังเหลือเผื่อ 1 — เกม C วาด sprite เองในเครื่องเลยยาวได้ถึง 140 ช่อง
# ฝั่ง Python พอโตครบ 19 แล้วตัวจะหยุดยาว แต่คะแนนยังนับต่อ
MAX_LEN = 19

GRASS      = 0x4CA838        # สีสนามหญ้า ลอกจากเกม C
GRASS_MOWN = 0x409030        # สีแถบหญ้าที่เพิ่งตัด (ลายกว้าง 48px แบบเกม C)
APPLE      = 0xD82818        # แอปเปิลสีแดง (เกม C ใช้ sprite รูปแอปเปิล)


def coin_sound():
    # เกม C มีเสียงเหรียญ "cha-ching" ทุกแอปเปิลลูกที่ 10 (เป็นไฟล์เสียง PCM
    # ที่ Python ยังเรียกตรงๆ ไม่ได้) เราเลยแต่งโน้ต 2 ตัวให้ได้อารมณ์เดียวกัน
    game.tone(83, ms=60)
    time.sleep_ms(45)
    game.tone(88, ms=160)


game.title("SNAKE", melody=True)

mode = 1                     # เปิดมาชี้ CLASSIC ก่อน เหมือนเกม C
death_msg = None             # สาเหตุที่ตายตาก่อน — โชว์บนหัวเมนูแบบเกม C
restart_same = False         # ปุ่ม Y = เริ่มโหมดเดิมใหม่ทันที ไม่ต้องผ่านเมนู
while True:
    if not restart_same:
        # ตายแล้ววนกลับมาเลือกโหมดใหม่ได้ทุกตา — จังหวะเดียวกับเกม C
        # (หัวเมนูบอกด้วยว่าตาก่อนจบเพราะอะไร เหมือน status ของ picker ใน C)
        picked = game.menu("RELAXED", "CLASSIC", "TURBO", selected=mode,
                           heading=death_msg or "SELECT MODE")
        if picked is None:   # BACK จากหน้าเมนู = เลิกเล่น (เหมือนเกม C)
            break
        mode = picked
    restart_same = False

    # ---- จัดฉาก (ต้องสร้างใหม่ทุกตา เพราะ replay ล้างจอทั้งหมด) ----
    game.background(GRASS)
    for row in range(1, 8, 2):                     # แถบหญ้าสลับสีแบบสนามตัดหญ้า
        game.Box(0, row * 48, game.WIDTH, 48, GRASS_MOWN)

    body = [[10 - i, 10] for i in range(5)]        # ช่องของงู หัวอยู่หน้าสุด (จุดเกิดเดียวกับเกม C)
    head = game.Box(body[0][0] * CELL, body[0][1] * CELL, CELL - 2, CELL - 2, game.GB_DARKEST)
    boxes = []                                     # กล่องลำตัวที่โชว์อยู่ เรียงจากคอไปหาง
    for cell in body[1:]:
        boxes.append(game.Box(cell[0] * CELL, cell[1] * CELL, CELL - 2, CELL - 2, game.GB_DARK))
    spare = []                                     # กล่องลำตัวสำรอง สร้างครบตั้งแต่แรกแล้วซ่อนไว้ (เกม C ก็ทำแบบนี้)
    for _ in range(MAX_LEN - len(body)):
        b = game.Box(-100, -100, CELL - 2, CELL - 2, game.GB_DARK)
        b.hide()
        spare.append(b)
    food = game.Box(0, 0, CELL - 2, CELL - 2, APPLE)
    food_cell = [0, 0]
    hud = game.Text("", 10, 8, game.WHITE)

    score = 0
    step_x, step_y = 1, 0                          # เริ่มวิ่งไปขวา เหมือนเกม C
    death_msg = "GAME OVER"
    restart_now = False                            # ตั้งเป็นจริงเมื่อผู้เล่นกด Y

    def show_hud():
        # ช่อง Best ขยับสดระหว่างเล่นแบบเกม C: คะแนนแซงเมื่อไหร่ Best ตามทันที
        hud.set("%s    Score: %d    Best: %d    Len: %d"
                % (MODES[mode][0], score, max(game.best("snake"), score), len(body)))

    def place_food():
        # สุ่มช่องไปเรื่อยๆ จนกว่าจะเจอช่องที่งูไม่ได้ทับอยู่
        while True:
            c = [random.randint(0, COLS - 1), random.randint(0, ROWS - 1)]
            if c not in body:
                food_cell[0], food_cell[1] = c
                food.move_to(c[0] * CELL, c[1] * CELL)
                return

    place_food()
    show_hud()

    def update():
        global score, step_x, step_y, death_msg, restart_now
        k = game.keys()
        if game.pressed_once("y", k):    # Y = เริ่มตาใหม่โหมดเดิมทันที (แบบเกม C)
            restart_now = True
            return False
        # เลี้ยวแบบจับ "จังหวะกด" เหมือนเกม C (กดค้างไม่นับซ้ำ) — อ่านครบทุกปุ่ม
        # ก่อน แล้วค่อยเลือกตามลำดับ และห้ามกลับหลังหัน 180 องศา
        up    = game.pressed_once("up", k)
        down  = game.pressed_once("down", k)
        left  = game.pressed_once("left", k)
        right = game.pressed_once("right", k)
        if up and step_y == 0:      step_x, step_y = 0, -1
        elif down and step_y == 0:  step_x, step_y = 0, 1
        elif left and step_x == 0:  step_x, step_y = -1, 0
        elif right and step_x == 0: step_x, step_y = 1, 0

        old_head = body[0]
        next_head = [old_head[0] + step_x, old_head[1] + step_y]

        # ชนขอบสนามหรือชนตัวเอง = จบตา (ลำดับการเช็คเดียวกับเกม C)
        if not (0 <= next_head[0] < COLS and 0 <= next_head[1] < ROWS):
            game.sfx("die"); death_msg = "Wall hit"; return False
        if next_head in body:            # กัดตัวเอง — คนละเสียงกับชนกำแพง แบบเกม C
            game.sfx("lose"); death_msg = "Self collision"; return False

        body.insert(0, next_head)
        grew = False
        if next_head == food_cell:
            score += 1
            game.sfx("eat")
            if score % 10 == 0:                    # ทุกลูกที่ 10 มีเสียงเหรียญ เหมือนเกม C
                coin_sound()
            if len(body) <= MAX_LEN:               # ยังไม่ชนเพดานงบวิดเจ็ต → ตัวยาวขึ้นจริง
                grew = True
            place_food()
        if not grew:
            body.pop()
        show_hud()                                 # เกม C ก็อัปเดต HUD ท้ายทุกก้าวแบบนี้

        # เคล็ดงูคลาสสิก: แต่ละก้าวทั้งตัวดูเหมือนขยับ แต่ที่เปลี่ยนจริงมีแค่หัวกับหาง
        # เลยย้าย "กล่องหาง" ไปสวมตำแหน่งหัวเก่า แทนการขยับทุกกล่อง — เร็วกว่ากันมาก
        head.move_to(next_head[0] * CELL, next_head[1] * CELL)
        if grew:
            box = spare.pop()
            box.move_to(old_head[0] * CELL, old_head[1] * CELL)
            box.show()
        else:
            box = boxes.pop()
            box.move_to(old_head[0] * CELL, old_head[1] * CELL)
        boxes.insert(0, box)                       # กลายเป็นคอ (ต่อจากหัว)

    # (Start = พักเกม / Back = ออก — game.run() จัดการให้)
    if not game.run(update, fps=1000 / MODES[mode][1]):
        game.save_best(score, "snake")             # Back กลางเกม: คะแนนดีๆ ไม่หาย
        break                                      # Back = เลิกเล่น กลับ Playground
    if restart_now:                                # Y = วนไปเริ่มโหมดเดิมใหม่ทันที
        game.save_best(score, "snake")
        game.replay()
        restart_same = True
        continue
    if not game.game_over(score, name="snake", msg=death_msg):
        break                                      # Start = เล่นใหม่ / Back = พอแค่นี้
