# โครงเว้น 30% — เติมช่องที่ทำเครื่องหมายไว้ / เฉลย: starter/snake_step3.py / ใบ้: ในใบงาน session
# snake_step3.py — สร้าง Snake #3 (คาบ 5): อาหาร + กินแล้วโต + คะแนน + เสียง
# ใหม่จาก step2: สุ่มอาหาร, หัวชนอาหาร -> ต่อปล้อง + คะแนน + "Nice bite!" + game.sfx("eat")
#
# คาบนี้เราจะเพิ่ม "เป้าหมาย" ให้เกม คือวางอาหารแบบสุ่ม พองูกินก็ยาวขึ้นและได้แต้ม
#   เคล็ดลับ "กินแล้วโต": ปกติเราเติมหัว + ตัดหาง (ยาวเท่าเดิม) แต่ถ้ากินอาหาร เราจะ
#   "เติมหัว แต่ไม่ตัดหาง" -> งูยาวขึ้น 1 ช่องทันที (งูโตขึ้นพร้อมเสียงงับ เห็นผลทันตา)
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

    # ----- เติมส่วนนี้เอง (งานของคุณ): หัวงูกินอาหารไหม + ถ้ากินก็โต/ได้แต้ม/มีเสียง -----
    # TODO: เขียน if/else เช็คว่าหัวงูไปอยู่ช่องเดียวกับอาหารหรือไม่
    #   1) หา "ช่อง" ของอาหารจากพิกเซลของมัน: เอา food_square.x , food_square.y มาหารด้วย CELL_PX
    #      (// คือหารปัดลง) แล้วเทียบกับ next_head ว่าเป็นช่องเดียวกันไหม -> ได้ ate_food
    #   2) ถ้ากิน (ate_food):
    #        - บวกแต้ม score += 1
    #        - เล่นเสียงงับด้วย game.sfx(...) (ชื่อเสียงคือ "eat")
    #        - อัปเดตป้ายคะแนนด้วย score_text.set(...) ให้ขึ้น "Score: <แต้ม>"
    #        - ต่อปล้องใหม่ด้วย game.Box(...) แล้ว .append เข้า body_squares (ทำให้งูยาวขึ้น 1)
    #        - โชว์คำว่า "Nice bite!" ด้วย game.Text(...) (เลือกตำแหน่งราวๆ กลางจอเอง)
    #        - เรียก place_food_at_random_empty_cell() เพื่อวางอาหารชิ้นใหม่
    #   3) ถ้าไม่กิน (else): snake_body.pop()  # ตัดหาง = เดินปกติ ยาวเท่าเดิม
    #      สำคัญ! เคล็ดลับ "กินแล้วโต" = เติมหัวเสมอ แต่ตัดหางเฉพาะตอนไม่กิน (ดู starter ถ้าติด)
    snake_body.pop()   # placeholder ให้รันได้ก่อน — ย้ายบรรทัดนี้ไปไว้ในกิ่ง else เมื่อเขียน 30%
    # ===============================================================================

    for index, cell in enumerate(snake_body):
        body_squares[index].set_color(game.GB_LIGHT if index == 0 else game.GB_DARK)
        body_squares[index].move_to(cell[0] * CELL_PX, cell[1] * CELL_PX)


game.run(on_each_frame, fps=9)

# คาบ 6 (step สุดท้าย): เพิ่ม ชนกำแพง/ชนตัวเอง = GAME OVER + Best/Len + ความยาก
# -> ดูไฟล์เต็มที่ reference/snake_full.py (เป้าหมายสุดท้าย = เหมือน snake_game.png เป๊ะ)
