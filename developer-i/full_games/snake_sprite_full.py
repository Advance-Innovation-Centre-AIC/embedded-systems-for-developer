# snake_sprite_full.py — Snake ฉบับเต็ม วาดด้วยสไปรต์ C จริงของบอร์ด (spike-b)
# บนฮาร์ดแวร์ ตัวงู/หัวงู/แอปเปิลคือ "พิกเซลชุดเดียวกัน" กับเกม Snake ในเครื่อง
# เป๊ะๆ (ฝั่ง C เป็นเจ้าของรูป เราส่งแค่ชื่อกับตำแหน่งข้าม IPC) ส่วนบนซิมพีซี
# จะถอยไปเป็นกล่องเขียว GB ให้ตรรกะเดิมยังรันได้
#
# ตานี้เราตามเกม C ครบทั้งวงจรของมัน (page_game_snake.c):
#   สนามหญ้า, เมนูเลือกความยาก RELAXED/CLASSIC/TURBO, Score/Best/Len บน HUD,
#   เสียงกิน + เสียงพิเศษทุกแอปเปิลลูกที่ 10, เสียงตายแยกชนกำแพง/กัดตัวเอง,
#   ตายแล้วขึ้นป้ายให้เล่นซ้ำได้ทันที ไม่ต้องรีบูต, เลี้ยวแบบจับจังหวะกด
import bentogame as game
import random

# ----- ค่าคงที่ของเกม (ตัวเลขชุดเดียวกับ page_game_snake.c) -----
CELL = 16                                   # ขนาดช่องตาราง (SNAKE_CELL_PX = 16)
COLS, ROWS = game.WIDTH // CELL, game.HEIGHT // CELL   # 49 x 24 ช่อง
START_LEN = 5                               # งูเริ่มยาว 5 ท่อน เท่าเกม C

# โหมดความยาก = คาบเวลาต่อ 1 ก้าวของงู (มิลลิวินาที) ลอกมาจาก s_snake_modes:
# ก้าวช้า = มีเวลาคิด, ก้าวถี่ = ต้องตัดสินใจไว ตัวเกมอย่างอื่นเหมือนกันหมด
MODES = (("RELAXED", 150), ("CLASSIC", 115), ("TURBO", 70))

# สนามหญ้าแบบเกม C: พื้นเขียวอ่อน สลับแถบ "หญ้าเพิ่งตัด" เขียวเข้มกว่านิดเดียว
# (ของจริงใน C เป็นตารางหมากรุก 48px แต่แบบนั้นต้องใช้กล่องราว 70 ชิ้น
#  เกินงบ widget ของจอ — แถบแนวนอน 4 แถบให้อารมณ์สนามเดียวกันในราคา 4 ชิ้น)
GRASS_BASE = 0x4CA838
GRASS_MOWN = 0x409030

# ----- งบ widget (จอมีได้สูงสุด 32 ชิ้นรวมทุกอย่าง) นับกันตรงนี้เลย -----
#   พื้นหลัง 1 + แถบหญ้า 4 + ลำตัวงู 23 + หัว 1 + อาหาร 1 + HUD 1   = 31
#   + ป้ายบอกปุ่มของ game.run() อีก 1                               = 32 พอดี
#   (ป้าย PAUSED ยืมป้ายบอกปุ่มตัวเดิม — พักเกมจึงไม่กินงบเพิ่มสักชิ้น)
# ตอนตายจริงค่อยลบแถบหญ้า 4 ชิ้นทิ้ง (ตานั้นจบแล้ว ฉากโดนป้ายทับอยู่ดี)
# เพื่อคืนงบให้ป้าย game over 4 ชิ้นขึ้นครบ: 32 - 4 + 4 = 32 พอดีเป๊ะ
# เพราะงบนี้ งูยาวได้สูงสุด 24 ท่อน (เกม C วาดเองบน CM55 เลยยาวได้ถึง 140)
POOL = 23                                   # ลำตัวที่เตรียมไว้ล่วงหน้าใน pool
MAX_BODY = POOL + 1                         # + หัวอีก 1

HEAD_BY_DIR = {(1, 0): "snake_head_r", (-1, 0): "snake_head_l",
               (0, -1): "snake_head_u", (0, 1): "snake_head_d"}

game.title("SNAKE", melody=True)            # หน้าเริ่ม: Start=เล่น Back=ออก

mode = 1                                    # เริ่มชี้ CLASSIC เหมือนเกม C
restart_same = False                        # ปุ่ม Y = เริ่มโหมดเดิมใหม่ ไม่ผ่านเมนู
while True:
    if not restart_same:
        # เลือกความยากก่อนเริ่มทุกตา — ตายแล้วก็วนกลับมาหน้านี้ จังหวะเดียวกับเกม C
        picked = game.menu("RELAXED", "CLASSIC", "TURBO", selected=mode)
        if picked is None:                  # BACK จากหน้าเมนู = เลิกเล่น
            break
        mode = picked
    restart_same = False
    tick_ms = MODES[mode][1]

    # ----- จัดฉาก (ทำใหม่ทุกตา เพราะเล่นซ้ำจะล้างจอทั้งหมด) -----
    game.background(GRASS_BASE)             # พื้นหลังต้องสร้างก่อนเพื่อนเสมอ
    grass_strips = []                       # เก็บไว้ลบตอนตาย คืนงบให้ป้ายจบเกม
    for y in range(48, ROWS * CELL, 96):    # แถบหญ้าตัดที่ y = 48,144,240,336
        grass_strips.append(game.Box(0, y, game.WIDTH, 48, GRASS_MOWN))

    body = [[10 - i, 10] for i in range(START_LEN)]  # หัวอยู่หน้าสุด หันขวา
    body_segments = game.pool("snake_body", POOL)    # สร้างครั้งเดียว นอก update()
    head = game.Sprite("snake_head_r", 0, 0)
    food = game.Sprite("snake_food", 0, 0)
    hud = game.Text("", 12, 8, game.WHITE)

    step_x, step_y, score = 1, 0, 0         # ทิศที่งูก้าวในแต่ละติ๊ก
    food_cell = [0, 0]
    end_reason = ""                         # "wall" หรือ "self" ไว้เลือกข้อความตอนจบ
    restart_now = False                     # ตั้งเป็นจริงเมื่อผู้เล่นกด Y

    def update_hud():
        # HUD แบบเดียวกับเกม C: Score / Best / Len (Best โชว์ค่าสดระหว่างเล่น
        # ส่วนค่าจริงบันทึกให้ตอน game over) บวกชื่อโหมดไว้หน้าสุดกันลืมว่าเล่นอะไรอยู่
        hud.set("%s   Score: %d   Best: %d   Len: %d"
                % (MODES[mode][0], score, max(score, game.best("snake")), len(body)))

    def place_food():
        while True:                         # สุ่มจนกว่าจะได้ช่องว่างที่ไม่ทับตัวงู
            col, row = random.randint(0, COLS - 1), random.randint(0, ROWS - 1)
            if [col, row] not in body:
                food_cell[0], food_cell[1] = col, row
                food.move_to(col * CELL, row * CELL)
                return

    def draw():
        head.frame(HEAD_BY_DIR[(step_x, step_y)])    # หัวหันตามทิศ เหมือนเกม C
        head.move_to(body[0][0] * CELL, body[0][1] * CELL)
        for i in range(POOL):               # body[1:] -> สไปรต์ในพูล
            if i + 1 < len(body):
                body_segments[i].show()
                body_segments[i].move_to(body[i + 1][0] * CELL,
                                         body[i + 1][1] * CELL)
            else:
                body_segments[i].hide()

    place_food()
    draw()
    update_hud()

    def update():
        global step_x, step_y, score, end_reason, restart_now
        k = game.keys()
        if game.pressed_once("y", k):   # Y = เริ่มตาใหม่โหมดเดิมทันที (แบบเกม C)
            restart_now = True
            return False
        # เลี้ยวแบบ "จับจังหวะกด" ทุกทิศทุกเฟรม (กดค้างไม่นับซ้ำ) วิธีเดียวกับเกม C
        # และกันการกลับหลังหัน: เลี้ยวขึ้น/ลงได้เฉพาะตอนวิ่งแนวนอน สลับกันไป
        up, down = game.pressed_once("up", k), game.pressed_once("down", k)
        left, right = game.pressed_once("left", k), game.pressed_once("right", k)
        if up and step_y == 0:      step_x, step_y = 0, -1
        elif down and step_y == 0:  step_x, step_y = 0, 1
        elif left and step_x == 0:  step_x, step_y = -1, 0
        elif right and step_x == 0: step_x, step_y = 1, 0
        # (Back=ออก / Start=พักเกม — game.run() จัดการให้)

        next_head = [body[0][0] + step_x, body[0][1] + step_y]
        if (next_head[0] < 0 or next_head[0] >= COLS or
                next_head[1] < 0 or next_head[1] >= ROWS):
            end_reason = "wall"
            game.sfx("die")                 # เสียงชนกำแพง
            return False
        if next_head in body:
            end_reason = "self"
            game.sfx("lose")                # กัดตัวเอง — คนละเสียงกับชนกำแพง แบบเกม C
            return False

        body.insert(0, next_head)
        if next_head == food_cell:
            score += 1
            game.sfx("eat")
            if score % 10 == 0:             # แอปเปิลทุกลูกที่ 10 มีเสียงรางวัล แบบเกม C
                game.sfx("point")
            place_food()
            if len(body) > MAX_BODY:        # พูลลำตัวเต็ม -> หยุดโต แต่คะแนนนับต่อ
                body.pop()
        else:
            body.pop()
        draw()
        update_hud()

    # คาบเวลาต่อก้าวของโหมด -> fps ของ run() (เช่น CLASSIC 115ms ~ 8.7 ก้าว/วินาที)
    if not game.run(update, fps=1000 / tick_ms):
        game.save_best(score, "snake")      # Back กลางเกม: คะแนนดีๆ ไม่หาย
        break                               # Back = เลิกเล่น กลับ Playground
    if restart_now:                         # Y = วนไปเริ่มโหมดเดิมใหม่ทันที
        game.save_best(score, "snake")
        game.replay()
        restart_same = True
        continue
    for strip in grass_strips:              # ตานี้จบแล้ว: ลบแถบหญ้า 4 ชิ้นทิ้ง
        strip.delete()                      # คืนงบให้ป้าย game over ขึ้นครบ 4 ชิ้น
    msg = ("GAME OVER - Wall hit" if end_reason == "wall"
           else "GAME OVER - Self collision")
    if not game.game_over(score, name="snake", msg=msg):
        break                               # Start = เล่นใหม่ (วนไปเลือกโหมด), Back = ออก
