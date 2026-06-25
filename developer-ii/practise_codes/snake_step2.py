# โครงเว้นบางส่วน ให้เราเติมช่องที่เป็นงานของคุณเอง
# เฉลย: starter/snake_step2.py · ใบ้: ในใบงาน session
# snake_step2.py — สร้าง Snake #2 (คาบ 5): งูเดินได้ + บังคับด้วยจอย
# ใหม่จาก step1: game loop (game.run/update) + เดินทีละช่อง + เลี้ยวด้วย game.keys()
#
# เรื่องย่อของคาบนี้: ทำให้งู "มีชีวิต" คือทุก ๆ จังหวะ (frame) งูจะคืบไปข้างหน้า 1 ช่อง
#   เคล็ดลับของ Snake: ไม่ต้องขยับทั้งตัว แค่เติมหัวใหม่ข้างหน้าแล้วตัดหางทิ้ง 1 ช่อง
#   เท่านี้งูก็ดูเหมือนเลื้อยไปข้างหน้าแล้ว (พอทำเสร็จงูจะเดินตามจอยได้จริง)
import bentogame as game

CELL_PX = 26
GRID_COLS = game.WIDTH // CELL_PX
GRID_ROWS = game.HEIGHT // CELL_PX

game.start()

snake_body = [[6, 8], [5, 8], [4, 8]]       # หัวอยู่ตัวแรก
body_squares = [game.Box(col * CELL_PX, row * CELL_PX, CELL_PX - 2, CELL_PX - 2, game.GB_DARK)
                for col, row in snake_body]
body_squares[0].set_color(game.GB_LIGHT)
score_text = game.Text("Score: 0", 10, 8, game.WHITE)

# ทิศที่งูกำลังเดิน เก็บเป็น "ก้าวละกี่ช่องในแนวคอลัมน์/แถว"
# 1,0 = ขวา · -1,0 = ซ้าย · 0,-1 = ขึ้น · 0,1 = ลง
step_col, step_row = 1, 0


def on_each_frame():                         # ฟังก์ชันนี้ถูกเรียกซ้ำทุกจังหวะ (= หัวใจของเกม)
    global step_col, step_row
    keys = game.keys()
    # เลี้ยวตามจอย — แต่ "ห้ามถอยหลังกลับทับตัวเอง" (เลี้ยวได้เมื่อแกนนั้นกำลังนิ่ง = 0)
    if keys.left and step_col == 0:  step_col, step_row = -1, 0
    if keys.right and step_col == 0: step_col, step_row = 1, 0
    if keys.up and step_row == 0:    step_col, step_row = 0, -1
    if keys.down and step_row == 0:  step_col, step_row = 0, 1
    # Back = ออกจากเกม · Start = เริ่มใหม่ — game.run() จัดการให้ทั้งคู่อยู่แล้ว

    # ----- เติมส่วนนี้เอง (งานของคุณ): ทำให้งูเดินไปข้างหน้า 1 ช่อง -----
    # TODO 1) หาช่องใหม่ของหัว: เอาหัวเดิม snake_body[0] (เป็น [col, row]) มาบวกกับทิศ step_col, step_row
    #         เก็บผลลัพธ์ไว้ในตัวแปร เช่น next_head (เป็น list [col ใหม่, row ใหม่])
    # TODO 2) เติมหัวใหม่ไว้หน้าสุดของ snake_body ด้วยเมท็อด .insert(...) (แทรกที่ตำแหน่ง 0)
    # TODO 3) ตัดหางทิ้ง 1 ช่องด้วยเมท็อด .pop() — รวมกันแล้วงูจะดูเหมือนเลื้อยไป 1 ช่อง
    pass   # <- ลบ pass ออกเมื่อเริ่มเขียน · ติดตรงไหนเปิดดู starter/snake_step2.py
    # ===================================================================

    # วาดทุกปล้องให้ไปอยู่ช่องที่ถูกต้อง (หัวสีอ่อน ลำตัวสีเข้ม)
    for index, cell in enumerate(snake_body):
        body_squares[index].set_color(game.GB_LIGHT if index == 0 else game.GB_DARK)
        body_squares[index].move_to(cell[0] * CELL_PX, cell[1] * CELL_PX)


game.run(on_each_frame, fps=9)               # เรียก on_each_frame 9 ครั้ง/วินาที = จังหวะ Snake
