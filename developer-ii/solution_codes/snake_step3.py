# snake_step3.py — สร้าง Snake #3 (คาบ 5): อาหาร + กินแล้วโต + คะแนน + เสียง
# ใหม่จาก step2: สุ่มอาหาร, หัวชนอาหาร -> ต่อปล้อง + คะแนน + "Nice bite!" + game.sfx("eat")
#
# เรื่องย่อของคาบนี้: เพิ่ม "เป้าหมาย" ให้เกม — วางอาหารแบบสุ่ม พองูกินก็ยาวขึ้น + ได้แต้ม
#   เคล็ดลับ "กินแล้วโต": ปกติเราเติมหัว + ตัดหาง (ยาวเท่าเดิม) แต่ถ้ากินอาหาร เราจะ
#   "เติมหัว แต่ไม่ตัดหาง" -> งูยาวขึ้น 1 ช่องทันที พร้อมเสียงงับ เห็นผลทันตา
import bentogame as game
import random

CELL_PX = 26
GRID_COLS = game.WIDTH // CELL_PX
GRID_ROWS = game.HEIGHT // CELL_PX

game.title("SNAKE")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

snake_body = [[6, 8], [5, 8], [4, 8]]
body_squares = [game.Box(col * CELL_PX, row * CELL_PX, CELL_PX - 2, CELL_PX - 2, game.GB_DARK)
                for col, row in snake_body]
body_squares[0].set_color(game.GB_LIGHT)
food_square = game.Box(0, 0, CELL_PX - 2, CELL_PX - 2, game.GB_LIGHTEST)   # อาหาร = ช่องสว่างสุด
score_text = game.Text("Score: 0", 10, 8, game.WHITE)

step_col, step_row, score = 1, 0, 0


def place_food_at_random_empty_cell():       # หาช่องว่าง (ไม่ทับตัวงู) แล้ววางอาหารตรงนั้น
    while True:
        col = random.randint(0, GRID_COLS - 1)    # สุ่ม "ช่อง"
        row = random.randint(0, GRID_ROWS - 1)
        if [col, row] not in snake_body:          # ห้ามทับตัวงู
            food_square.move_to(col * CELL_PX, row * CELL_PX)   # ช่อง -> พิกเซล
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

    next_head = [snake_body[0][0] + step_col, snake_body[0][1] + step_row]
    snake_body.insert(0, next_head)

    # ----- เติมส่วนนี้เอง: เช็คว่าหัวงูไปอยู่ช่องเดียวกับอาหารไหม -----
    ate_food = (next_head == [food_square.x // CELL_PX, food_square.y // CELL_PX])
    if ate_food:                                   # งูกินอาหารเข้า
        score += 1
        game.sfx("eat")                            # เสียงงับ มาจาก C engine จริง
        score_text.set("Score: %d" % score)
        body_squares.append(game.Box(0, 0, CELL_PX - 2, CELL_PX - 2, game.GB_DARK))  # โต 1 ปล้อง
        game.Text("Nice bite!", 320, 180, game.GB_LIGHT)
        place_food_at_random_empty_cell()
    else:
        snake_body.pop()                           # ไม่กิน -> ตัดหาง = เดินปกติ

    for index, cell in enumerate(snake_body):
        body_squares[index].set_color(game.GB_LIGHT if index == 0 else game.GB_DARK)
        body_squares[index].move_to(cell[0] * CELL_PX, cell[1] * CELL_PX)


game.run(on_each_frame, fps=9)

# คาบ 6 (step สุดท้าย): เพิ่ม ชนกำแพง/ชนตัวเอง = GAME OVER + Best/Len + ความยาก
# -> ดูไฟล์เต็มที่ reference/snake_full.py (เป้าหมายสุดท้าย = เหมือน snake_game.png เป๊ะ)
