# โครงเว้นไว้ให้คุณเติมเอง เติมตรงช่องที่บอกว่าเป็นงานของคุณ
# ถ้าติด: เปิดดู starter/snake_step5.py หรือใบงานประจำคาบ
# snake_step5.py — Snake #5 (step สุดท้ายที่คุณเขียนเอง): อัปเกรดเป็นสไปรท์จริง + เลือกความยาก
# -----------------------------------------------------------------------------
# คาบนี้เรายังเล่นเหมือน step4 ทุกอย่าง แต่เปลี่ยน "ผิวเกม" จากกล่องสี่เหลี่ยม
#   ให้เป็นรูปวาดงูจริง (pixel-art) หัวงูหันหน้าตามทางเดิน มีเมนูเลือกความยาก และเก็บสถิติ Best
#   เป็นก้าวจาก "เกมที่เล่นได้" ไปสู่ "เกมที่ดูเหมือนของจริง" พอถึงตรงนี้คุณทำเกมเต็มได้แล้ว
#
#   ตรรกะงู (เดิน/โต/ตาย) ยังเป็นส่วนที่คุณเขียนเอง อยู่ใน on_each_frame()+state เหมือน step4 เปลี่ยนแค่ "ผิวเกม"
#   เรายังเรียก core ที่ให้มา (game.Sprite/.pool/.frame/.keys/.run) เหมือนทุก step ไม่ต้องลงไปแตะ engine
# เป้าหมาย: ผลบนจอตรงกับ C step5 (snake_step5.c) ทุกประการ Python step == C step
# ส่วนที่คุณเขียนเพิ่มจาก step4 (logic เดิม ไม่เปลี่ยน):
#   1) วาดด้วย "สไปรท์จริง" แทน Box: game.Sprite("snake_head_r"/"snake_body"/"snake_food")
#      และหัวงูหันทิศตามทาง  head_sprite.frame(HEAD_SPRITE_FOR[(step_col,step_row)])
#   2) pool สไปรท์ลำตัว = game.pool("snake_body", BODY_POOL_SIZE) สร้าง "ครั้งเดียว" อย่าสร้างใน on_each_frame
#      (กฎ reuse-don't-create เพดาน 32 widget ฝั่ง Python, UI_MAX_WIDGETS=32 ที่ ipc_ui_protocol.h:163 ดูเพิ่ม PARITY.md:46)
#   3) เลือกความยาก RELAXED/CLASSIC/TURBO ก่อนเริ่ม เพื่อกำหนด fps (page_game_snake.c:42-46)
#   4) Best score (ค่าดีที่สุดข้ามรอบ)                    (page_game_snake.c:101-110)
# core ที่เราเรียกใช้ (ส่วนที่ให้มา): game.start, game.Sprite/.frame/.move_to/.hide/.show,
#   game.pool, game.Text+.set, game.keys, game.sfx, game.run
# C step == Python step บนจอ:  snake_step5.c (สไปรท์หัวหันทิศ เมนูโหมด และ Best ตรงกัน)
#   บนบอร์ดจริงจะ pixel-identical ส่วนบน sim เก่า game.Sprite จะ fallback เป็นกล่อง GB-green
#   อัตโนมัติ (logic เหมือนเดิม)
#
# ส่วนที่เกินจาก step5 (CAPSTONE / REFERENCE ไม่ใช่ส่วนที่คุณต้องเขียนเอง ไว้เปิดดูเฉยๆ):
#   - reference/snake_sprite_full.py  = เฉลย Python เต็ม (directional head + stretch)
#   - page_game_snake.c (ของจริงที่ flash บนบอร์ด, 578 บรรทัด) = engine เต็ม พร้อมเมนู/เพลง/
#     โหมดครบ เป็นปลายทางให้ดูว่าเกมสุดท้ายหน้าตาเป็นอย่างไร คุณไม่ต้องเขียนถึงระดับนี้
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
    # ----- เติมส่วนนี้เอง (งานของคุณ): ตรรกะงู เดิน/ตาย/กินโต (เหมือน step4 ผิวเกมเป็นสไปรท์แล้ว) -----
    # ตรรกะเดิมจาก step4 ทั้งหมด ผิวเกมเปลี่ยนเป็นสไปรท์ แต่ logic ไม่เปลี่ยนเลย ค่อยๆ ทำตามขั้น:
    # 1) เช็คตาย: ถ้า next_head ออกนอกกริด (col หรือ row ต่ำกว่า 0 หรือถึง/เกิน GRID_COLS/GRID_ROWS)
    #    หรือ next_head ไปทับลำตัวตัวเอง (อยู่ใน snake_body) -> เล่นเสียงตายด้วย game.sfx(...),
    #    อัปเดต best_score ถ้า score ทำได้ดีกว่าเดิม, โชว์ข้อความจบเกมด้วย game.Text(...), แล้ว return False
    # 2) เดินไปข้างหน้า: เอา next_head ใส่ "หัวแถว" ของ snake_body (เมท็อด list ที่แทรกตำแหน่ง 0)
    # 3) กินอาหารไหม? ถ้า next_head ตรงกับ food_cell -> บวกแต้ม (score += 1) + อัปเดต best_score,
    #    เล่นเสียงกินด้วย game.sfx(...), อัปเดตป้ายคะแนนด้วย score_text.set(...) (โชว์ทั้ง Score และ Best),
    #    สุ่มอาหารใหม่ด้วย place_food_at_random_empty_cell(); ถ้างูยาวเกิน MAX_SNAKE_LENGTH ให้ตัดหางทิ้ง (.pop())
    #    --- ถ้าไม่ได้กิน -> ตัดหางทิ้งด้วย .pop() (หางเดินตามหัว ความยาวเท่าเดิม)
    # 4) ปิดท้ายทุกเฟรม: เรียก redraw() เพื่อวาดหัว/ลำตัว/อาหาร ใหม่
    # (ติดตรงไหนเปิดดู starter/snake_step5.py ได้)
    snake_body.pop()   # <- placeholder กันค้าง (ลบทิ้งเมื่อเริ่มเขียนข้อ 1-4)
    redraw()


game.run(on_each_frame, fps=fps)
