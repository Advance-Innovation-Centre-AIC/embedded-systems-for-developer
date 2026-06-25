# โครงเว้น 30% — ช่องที่คุณจะเติมเอง
# เฉลย: starter/snake_sprite_step2.py · ใบ้: ในใบงาน session
#
# snake_sprite_step2.py — Snake #4 (คาบ 5): กริด-เดิน + กินแล้วโตด้วย sprite pool + ชนตัวเอง/กำแพง = ตาย
#
# ต่อยอดจากคาบ 4 (snake_sprite.py: เปลี่ยนกล่อง -> sprite, เดินได้แล้ว).
# คาบนี้เราจะใส่ "สมอง" ส่วนที่คุณเขียนเองให้ครบลูป:
#   - เดิน  = body.insert(หัวใหม่) + body.pop(หาง)
#   - โต    = body.insert(หัวใหม่) แต่ "ไม่" pop หาง  (หัวใจของ Snake)
#   - ตาย   = หัวชนกำแพง หรือ หัวไปอยู่ใน body (ชนตัวเอง)
#   - ลำตัว = sprite pool สร้างครั้งเดียว (game.pool) -> show/hide/move ซ้ำ (ห้ามสร้างใน update())
#
# บนบอร์ดจริง = sprite พิกเซลเป๊ะเท่าเกม C; บน desktop sim = กล่องเขียว GB (logic เหมือนกันทุกบรรทัด).
# โค้ดเฉลยเต็ม (มี directional head + stretch) อยู่ที่ reference/snake_sprite_full.py
import bentogame as game
import random

CELL = 16                                   # ตรงกับ C game (SNAKE_CELL_PX = 16)
COLS = game.WIDTH // CELL
ROWS = game.HEIGHT // CELL
POOL = 26                                   # จำนวนปล้องลำตัว (<= 32 - หัว - อาหาร - score = 29 widget ปลอดภัย)
MAX_BODY = POOL + 1                         # + หัว

game.start()

# ----- สร้าง sprite ครั้งเดียว (หัว + pool ลำตัว + อาหาร) -- อย่าสร้างใน update() นะ -----
body = [[6, 8], [5, 8], [4, 8]]            # หัวอยู่ช่องแรก (เก็บเป็น "ช่อง" [col, row])
body_segment_pool = game.pool("snake_body", POOL)   # สร้าง 26 ปล้อง ครั้งเดียว (ซ่อนไว้ก่อน)
head = game.Sprite("snake_head_r", 0, 0)   # หัวงู sprite จริง
food = game.Sprite("snake_food", 0, 0)     # อาหาร sprite จริง
score_text = game.Text("Score: 0", 10, 8, game.WHITE)

step_x, step_y, score = 1, 0, 0             # 1,0=ขวา · -1,0=ซ้าย · 0,-1=ขึ้น · 0,1=ลง
food_cell = [0, 0]


def place_food():
    """สุ่มอาหารเป็น 'ช่อง' (ไม่ใช่พิกเซล) แล้วค่อยคูณ CELL ตอนวาด; ห้ามทับตัวงู."""
    while True:
        col = random.randint(0, COLS - 1)
        row = random.randint(0, ROWS - 1)
        if [col, row] not in body:
            food_cell[0], food_cell[1] = col, row
            food.move_to(col * CELL, row * CELL)   # ช่อง -> พิกเซล
            return


def draw():
    """ย้ายเฉพาะ sprite ที่ใช้: show ปล้องที่มีจริง, hide ที่เหลือ (เร็ว — C core วาดพิกเซลให้)."""
    head.move_to(body[0][0] * CELL, body[0][1] * CELL)
    for segment_index in range(POOL):       # body[1:] -> map ลง body_segment_pool
        if segment_index + 1 < len(body):
            body_segment_pool[segment_index].show()
            body_segment_pool[segment_index].move_to(body[segment_index + 1][0] * CELL, body[segment_index + 1][1] * CELL)
        else:
            body_segment_pool[segment_index].hide()


place_food()
draw()


def update():
    global step_x, step_y, score
    k = game.keys()

    # ----- เติมส่วนนี้เอง (งานของคุณ): อ่านปุ่มทิศ -> เปลี่ยน step_x, step_y (เลี้ยวงู) -----
    # 1) อ่านปุ่มจาก k (game.keys คืน k.left/k.right/k.up/k.down/k.start)
    # 2) เลี้ยวซ้าย/ขวา -> ตั้ง step_x,step_y ให้ขยับแกน x (อีกแกนเป็น 0); ขึ้น/ลง -> ขยับแกน y
    # 3) กันถอยหลังทับตัวเอง: เลี้ยวซ้าย/ขวาได้เฉพาะตอน step_x==0, เลี้ยวขึ้น/ลงได้เฉพาะตอน step_y==0
    # 4) ถ้ากด k.start ให้ return False เพื่อออกเกม
    pass   # ลบ pass ออกเมื่อเริ่มเขียน

    next_head = [body[0][0] + step_x, body[0][1] + step_y]   # ช่องถัดไปของหัว

    # ----- เติมส่วนนี้เอง (งานของคุณ): ตรวจ "ตาย" ก่อน insert (ชนกำแพง หรือ ชนตัวเอง) -----
    # 1) เช็คชนกำแพง: next_head[0] (col) ออกนอกช่วง 0..COLS-1 หรือ next_head[1] (row) ออกนอกช่วง 0..ROWS-1
    # 2) เช็คชนตัวเอง: next_head อยู่ใน body หรือไม่ (ใช้ตัวดำเนินการ in)
    # 3) ถ้าตายข้อใดข้อหนึ่ง -> เล่นเสียงด้วย game.sfx(...), แสดงคำว่า GAME OVER ด้วย game.Text(...)
    #    (เลือกตำแหน่ง x,y กลางจอเอง + สี game.RED) แล้ว return False
    pass   # ลบ pass ออกเมื่อเริ่มเขียน

    body.insert(0, next_head)                  # เติมหัวใหม่เสมอ

    # ----- เติมส่วนนี้เอง (งานของคุณ): กินอาหาร -> โต / ไม่กิน -> เดินปกติ (ตัดหาง) -----
    # 1) ถ้าหัวใหม่ตรงกับช่องอาหาร (next_head == food_cell) แปลว่า "กิน" -> งูโต:
    #    - บวกแต้ม score, เล่นเสียงด้วย game.sfx(...)
    #    - อัปเดตป้ายคะแนนด้วย score_text.set(...) (จัดข้อความเอง), แล้วสุ่มอาหารใหม่ด้วย place_food()
    #    - กันลำตัวเกินเพดาน pool: ถ้า len(body) > MAX_BODY ค่อย body.pop()
    # 2) ไม่งั้น (else) ให้เดินปกติ -> ตัดหางทิ้งด้วย body.pop()
    # (หมายเหตุ: body.insert หัวใหม่ทำให้แล้วในบรรทัดบน — โต = ไม่ pop, เดิน = pop)
    body.pop()   # placeholder ให้รันได้ก่อน (ยังไม่โต); แทนที่ด้วย if/else ของคุณ

    draw()


game.run(update, fps=9)                        # 9 เฟรม/วิ = จังหวะ Snake คลาสสิก
