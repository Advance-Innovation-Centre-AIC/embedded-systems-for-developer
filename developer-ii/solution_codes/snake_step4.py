# snake_step4.py — สร้าง Snake #4 (คาบ 6): "แพ้ได้แล้ว" ชนกำแพง/ชนตัวเอง = GAME OVER
# -----------------------------------------------------------------------------
# เรื่องย่อของคาบนี้: เกมที่แพ้ไม่ได้ ก็ยังไม่ค่อยเป็นเกมเท่าไหร่ คาบนี้เราเลยมาเติม "เงื่อนไขแพ้" กัน
#   พอใส่เงื่อนไขนี้ครบ step4 ก็จะกลายเป็นเกมที่เล่นแพ้/ชนะได้จริง สมบูรณ์ในระดับผู้เริ่มต้น
#
# ส่วนที่คุณจะเติมเพิ่มจาก step3:  เช็คหัวงูออกนอกกริด หรือ หัวซ้อนทับตัวเอง -> จบเกม
#   - if หัว นอกขอบ  (col<0 / col>=GRID_COLS / row<0 / row>=GRID_ROWS) -> ตาย
#   - if หัว in snake_body (หัวใหม่ไปอยู่ช่องที่ตัวเองอยู่แล้ว)        -> ตาย
#   - ตาย: game.sfx("die") + ขึ้นป้าย "GAME OVER" + return False (ออกจาก loop)
# ส่วน core ที่เรา "เรียกใช้" (เตรียมมาให้แล้ว ไม่ต้องเขียนเอง):
#   game.start, game.Box, game.Text+.set, game.keys, game.sfx, game.run
#   (ตรรกะ wall/self collision = ของ snake_full.py:40-44 เป๊ะ)
# C step == Python step บนจอ:  เหมือน page_game_snake_lite.c (tick():83-88 ตาย+ป้าย)
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

    # ----- เติมส่วนนี้เอง: เงื่อนไข "แพ้" (ตรวจก่อนขยับงูจริง) -----
    if (next_head[0] < 0 or next_head[0] >= GRID_COLS or   # ชนกำแพงซ้าย/ขวา
            next_head[1] < 0 or next_head[1] >= GRID_ROWS or   # ชนกำแพงบน/ล่าง
            next_head in snake_body):                          # หัวซ้อนทับตัวเอง
        game.sfx("die")
        game.Text("GAME OVER", 320, 180, game.RED)
        return False                               # ออกจาก game loop

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

# step5 (คาบ 6-สุดท้าย): เปลี่ยน Box -> Sprite จริง (หัวงูหันทิศ) + เมนูเลือกความยาก
# -> ดูต่อที่ snake_step5.py  (เป้าหมายสุดท้าย คือให้เหมือนเกม C จริง page_game_snake.c)
