# snake_step5.py — สร้าง Snake #5 (step สุดท้ายของ 30%): "อัปเกรดเป็นสไปรท์จริง" + เลือกความยาก
# -----------------------------------------------------------------------------
# เรื่องย่อของคาบนี้: เกมเหมือน step4 ทุกอย่าง แต่เปลี่ยน "ผิวเกม" จากกล่องสี่เหลี่ยม
#   -> เป็นรูปวาดงูจริง (pixel-art) + หัวงูหันหน้าตามทางเดิน + มีเมนูเลือกความยาก + เก็บสถิติ Best
#   นี่คือก้าวจาก "เกมที่เล่นได้" -> "เกมที่ดูเหมือนของจริง" — ถึงตรงนี้คุณทำเกมเต็มได้แล้ว
#
#   ตรรกะงู (เดิน/โต/ตาย) ยังเป็น 30% ใน on_each_frame()+state เหมือน step4 — แค่ "ผิวเกม" เปลี่ยน.
#   ยังเรียก 70% core (game.Sprite/.pool/.frame/.keys/.run) เหมือนทุก step — ไม่ลงไปแตะ engine.
# เป้าหมาย: ผลบนจอ = ตรงกับ C step5 (snake_step5.c) ทุกประการ — Python step == C step.
# 30% ที่เด็กเขียนเพิ่มจาก step4 (logic เดิม ไม่เปลี่ยน):
#   1) วาดด้วย "สไปรท์จริง" แทน Box: game.Sprite("snake_head_r"/"snake_body"/"snake_food")
#      + หัวงูหันทิศตามทาง  head_sprite.frame(HEAD_SPRITE_FOR[(step_col,step_row)])
#   2) pool สไปรท์ลำตัว = game.pool("snake_body", BODY_POOL_SIZE) สร้าง "ครั้งเดียว" ห้ามสร้างใน on_each_frame
#      (กฎ reuse-don't-create — เพดาน 32 widget ฝั่ง Python, UI_MAX_WIDGETS=32 ที่ ipc_ui_protocol.h:163; ดูเพิ่ม PARITY.md:46)
#   3) เลือกความยาก RELAXED/CLASSIC/TURBO ก่อนเริ่ม -> กำหนด fps (page_game_snake.c:42-46)
#   4) Best score (ค่าดีที่สุดข้ามรอบ)                    (page_game_snake.c:101-110)
# core ที่ "เรียกใช้" (70% ให้มา): game.start, game.Sprite/.frame/.move_to/.hide/.show,
#   game.pool, game.Text+.set, game.keys, game.sfx, game.run
# C step == Python step บนจอ:  snake_step5.c (สไปรท์หัวหันทิศ + เมนูโหมด + Best ตรงกัน).
#   บนบอร์ดจริง = pixel-identical; บน sim เก่า game.Sprite จะ fallback เป็นกล่อง GB-green
#   อัตโนมัติ (logic เหมือนเดิม).
#
# เกินจาก step5 (CAPSTONE / REFERENCE — ไม่ใช่ 30% step, ไม่ต้องให้เด็กพิมพ์เอง):
#   - reference/snake_sprite_full.py  = เฉลย Python เต็ม (directional head + stretch)
#   - page_game_snake.c (ของจริงที่ flash บนบอร์ด, 578 บรรทัด) = engine เต็ม + เมนู/เพลง/
#     โหมดครบ. เป็น "ปลายทางให้ดู" ว่าเกมสุดท้ายหน้าตาเป็นอย่างไร — เด็กไม่ต้องเขียนระดับนี้.
# -----------------------------------------------------------------------------
import bentogame as game
import random
import time

CELL_PX = 16                                # ตรงกับเกม C จริง (SNAKE_CELL_PX = 16)
GRID_COLS, GRID_ROWS = game.WIDTH // CELL_PX, game.HEIGHT // CELL_PX
BODY_POOL_SIZE = 26                         # ปล้องลำตัว (<= 32 - head - food - score)
MAX_SNAKE_LENGTH = BODY_POOL_SIZE + 1       # + หัว

# โหมดความยาก = ค่า fps ของ game tick (snake_modes ใน page_game_snake.c:42-46)
DIFFICULTY_MODES = [("RELAXED", 6), ("CLASSIC", 9), ("TURBO", 14)]

game.title("SNAKE")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

snake_body = [[6, 8], [5, 8], [4, 8]]       # หัวอยู่ตัวแรก
body_pool = game.pool("snake_body", BODY_POOL_SIZE)   # สร้างครั้งเดียว — ห้ามอยู่ใน on_each_frame()!
head_sprite = game.Sprite("snake_head_r", 0, 0)
food_sprite = game.Sprite("snake_food", 0, 0)
score_text = game.Text("Score: 0   Best: 0", 10, 8, game.WHITE)

step_col, step_row, score, best_score = 1, 0, 0, 0
food_cell = [0, 0]
# หัวหันทิศ: ทิศเดิน (step_col,step_row) -> ชื่อสไปรท์หัว (snake_sprite_full.py:32-33)
HEAD_SPRITE_FOR = {(1, 0): "snake_head_r", (-1, 0): "snake_head_l",
                   (0, -1): "snake_head_u", (0, 1): "snake_head_d"}


def place_food_at_random_empty_cell():
    while True:
        col, row = random.randint(0, GRID_COLS - 1), random.randint(0, GRID_ROWS - 1)
        if [col, row] not in snake_body:
            food_cell[0], food_cell[1] = col, row
            food_sprite.move_to(col * CELL_PX, row * CELL_PX)
            return


def redraw():
    head_sprite.frame(HEAD_SPRITE_FOR[(step_col, step_row)])   # หัวหันทิศ เหมือนเกม C
    head_sprite.move_to(snake_body[0][0] * CELL_PX, snake_body[0][1] * CELL_PX)
    for pool_index in range(BODY_POOL_SIZE):   # snake_body[1:] -> pool ลำตัว
        if pool_index + 1 < len(snake_body):
            body_pool[pool_index].show()
            body_pool[pool_index].move_to(snake_body[pool_index + 1][0] * CELL_PX,
                                          snake_body[pool_index + 1][1] * CELL_PX)
        else:
            body_pool[pool_index].hide()


def choose_mode():
    """เมนูเลือกความยาก: UP/DOWN เลือก, A เริ่ม — เหมือน snake_show_menu (page_game_snake.c:205).
    หมายเหตุ: นี่คือ loop ของเราเอง (ก่อนเข้า game.run) จึงต้อง time.sleep_ms เองทุกรอบ
    มิฉะนั้น while True จะหมุนเปล่า (busy-loop) กิน CPU 100% — ห้ามใช้ game.run() ซ้อนในนี้."""
    selected = 1                             # CLASSIC เป็นค่าตั้งต้น
    menu_text = game.Text("", 250, 170, game.GB_LIGHTEST)
    while True:
        menu_text.set("MODE: < %s >   (UP/DOWN, A=start)" % DIFFICULTY_MODES[selected][0])
        keys = game.keys()
        if keys.up:    selected = (selected - 1) % len(DIFFICULTY_MODES)
        if keys.down:  selected = (selected + 1) % len(DIFFICULTY_MODES)
        if keys.a or keys.start:
            menu_text.set("")
            return DIFFICULTY_MODES[selected][1]    # คืนค่า fps ของโหมดที่เลือก
        time.sleep_ms(125)                   # 1 รอบ ~8/วิ (กันลั่นปุ่ม + ไม่ busy-hang)


fps = choose_mode()                          # เลือกก่อนเริ่มเล่น
place_food_at_random_empty_cell()
redraw()


def on_each_frame():
    global step_col, step_row, score, best_score
    keys = game.keys()
    if keys.left and step_col == 0:  step_col, step_row = -1, 0
    if keys.right and step_col == 0: step_col, step_row = 1, 0
    if keys.up and step_row == 0:    step_col, step_row = 0, -1
    if keys.down and step_row == 0:  step_col, step_row = 0, 1
    # (Back=ออก / Start=เริ่มใหม่ — game.run() จัดการให้)

    next_head = [snake_body[0][0] + step_col, snake_body[0][1] + step_row]
    # ----- เติมส่วนนี้เอง: ตรรกะเดิมจาก step4 (ตาย/โต/เดิน) ผิวเกมเปลี่ยนเป็นสไปรท์เท่านั้น -----
    if (next_head[0] < 0 or next_head[0] >= GRID_COLS or
            next_head[1] < 0 or next_head[1] >= GRID_ROWS or next_head in snake_body):
        game.sfx("die")
        if score > best_score:
            best_score = score
        game.Text("GAME OVER", 330, 180, game.RED)
        return False
    snake_body.insert(0, next_head)
    if next_head == food_cell:
        score += 1
        if score > best_score:
            best_score = score
        game.sfx("eat")
        score_text.set("Score: %d   Best: %d" % (score, best_score))
        place_food_at_random_empty_cell()
        if len(snake_body) > MAX_SNAKE_LENGTH:      # pool เต็ม -> หยุดโต
            snake_body.pop()
    else:
        snake_body.pop()
    redraw()


game.run(on_each_frame, fps=fps)
