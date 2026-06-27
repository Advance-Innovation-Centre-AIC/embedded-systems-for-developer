# โครงเว้น 30% — เติมช่องที่เป็นงานของคุณ / เฉลย: starter/snake_step4.py / ใบ้: ในใบงาน session
# snake_step4.py — สร้าง Snake #4 (คาบ 6): "แพ้ได้แล้ว" ชนกำแพง/ชนตัวเอง = GAME OVER
# -----------------------------------------------------------------------------
# เรื่องย่อของคาบนี้: เกมที่แพ้ไม่ได้ ก็ยังไม่ค่อยเป็นเกมเท่าไหร่ คาบนี้เราเติม "เงื่อนไขแพ้" กัน
#   พอใส่เงื่อนไขนี้ครบ step4 จะกลายเป็นเกมที่จบได้สมบูรณ์ระดับผู้เริ่มต้น เล่นแพ้/ชนะได้จริง
#
# ส่วนที่คุณเขียนเพิ่มจาก step3: เช็คหัวงูออกนอกกริด หรือ หัวซ้อนทับตัวเอง แล้วจบเกม
#   - แนวคิด: หัวตายเมื่อ "หลุดขอบกริด" หรือ "ไปทับช่องที่ตัวงูอยู่แล้ว"
#   - เครื่องมือที่ใช้: game.sfx() (เสียงตาย), game.Text() (ป้ายบนจอ), return False (ออกจาก loop)
# core ที่เราเรียกใช้ (ส่วนนี้เตรียมมาให้แล้ว ไม่ต้องเขียนเอง):
#   game.start, game.Box, game.Text+.set, game.keys, game.sfx, game.run
#   (ตรรกะ wall/self collision อ้างอิงตาม snake_full.py:40-44)
# C step กับ Python step บนจอ: เทียบได้กับ page_game_snake_lite.c (tick():83-88 ตาย+ป้าย)
# -----------------------------------------------------------------------------
import bentogame as game
import random

CELL_PX = 26
GRID_COLS = game.WIDTH // CELL_PX
GRID_ROWS = game.HEIGHT // CELL_PX

game.title("SNAKE")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

snake_body = [[6, 8], [5, 8], [4, 8]]       # หัวอยู่ตัวแรก
body_squares = [game.Box(col * CELL_PX, row * CELL_PX, CELL_PX - 2, CELL_PX - 2, game.GB_DARK)
                for col, row in snake_body]
body_squares[0].set_color(game.GB_LIGHT)
food_square = game.Box(0, 0, CELL_PX - 2, CELL_PX - 2, game.GB_LIGHTEST)
score_text = game.Text("Score: 0", 10, 8, game.WHITE)

step_col, step_row, score = 1, 0, 0


def place_food_at_random_empty_cell():
    while True:
        col = random.randint(0, GRID_COLS - 1)
        row = random.randint(0, GRID_ROWS - 1)
        if [col, row] not in snake_body:
            food_square.move_to(col * CELL_PX, row * CELL_PX)
            return


place_food_at_random_empty_cell()


def on_each_frame():
    global step_col, step_row, score
    keys = game.keys()
    if keys.left and step_col == 0:  step_col, step_row = -1, 0
    if keys.right and step_col == 0: step_col, step_row = 1, 0
    if keys.up and step_row == 0:    step_col, step_row = 0, -1
    if keys.down and step_row == 0:  step_col, step_row = 0, 1
    # (Back=ออก / Start=เริ่มใหม่ — game.run() จัดการให้)

    next_head = [snake_body[0][0] + step_col, snake_body[0][1] + step_row]   # ช่องถัดไปของหัว

    # ----- เติมส่วนนี้เอง (งานของคุณ): เงื่อนไข "แพ้" (ตรวจก่อนขยับงูจริง) -----
    # next_head คือ [col, row] ของหัวงูช่องถัดไป (คำนวณให้แล้วบรรทัดบน)
    # 1) เขียน if ตรวจ "แพ้" 2 กรณี รวมกันด้วย or:
    #      (ก) หัวหลุดขอบกริด — col หรือ row ติดลบ หรือ เกินจำนวนช่อง (GRID_COLS / GRID_ROWS)
    #      (ข) หัวไปทับตัวเอง — next_head อยู่ใน snake_body แล้ว (ใช้ตัวดำเนินการ in)
    # 2) ถ้าเข้าเงื่อนไขแพ้ ภายใน if ให้:
    #      - เล่นเสียงตายด้วย game.sfx() (ชื่อเสียง "die")
    #      - ขึ้นป้ายด้วย game.Text(ข้อความ, x, y, สี) — เลือกตำแหน่งกลางจอเอง, ใช้สี game.RED
    #      - return False เพื่อออกจาก game loop
    # (ติดจริงดู starter/snake_step4.py)
    pass   # <- ลบ pass ออกเมื่อเริ่มเขียน

    snake_body.insert(0, next_head)
    if next_head == [food_square.x // CELL_PX, food_square.y // CELL_PX]:   # กินอาหาร -> โต + คะแนน
        score += 1
        game.sfx("eat")
        score_text.set("Score: %d" % score)
        body_squares.append(game.Box(0, 0, CELL_PX - 2, CELL_PX - 2, game.GB_DARK))
        place_food_at_random_empty_cell()
    else:
        snake_body.pop()                            # ไม่กิน -> เดินปกติ

    for index, cell in enumerate(snake_body):
        body_squares[index].set_color(game.GB_LIGHT if index == 0 else game.GB_DARK)
        body_squares[index].move_to(cell[0] * CELL_PX, cell[1] * CELL_PX)


game.run(on_each_frame, fps=9)

# step5 (คาบ 6 สุดท้าย): เปลี่ยน Box เป็น Sprite จริง (หัวงูหันทิศ) + เมนูเลือกความยาก
# -> ดู snake_step5.py (เป้าหมายสุดท้ายคือให้เหมือนเกม C จริง page_game_snake.c)
