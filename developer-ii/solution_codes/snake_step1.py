# snake_step1.py — สร้าง Snake #1 (คาบ 4): "วาด" สนาม + ตัวงู + คะแนน (ยังไม่ขยับ)
# เป้าหมาย: หน้าจอใกล้เคียง snake_game.png (ภาพเกมจริง) แบบภาพนิ่ง
#
# เรื่องย่อของคาบนี้: เราจะ "วาด" งูลงบนกริด เหมือนวางหมากลงกระดาน
#   จอแบ่งเป็นช่องสี่เหลี่ยมเท่า ๆ กัน (กริด) แล้วงูคือกล่องเรียงต่อกันเป็นช่อง ๆ
#   คาบนี้ยังไม่ให้งูเดิน เราแค่ทำภาพนิ่งให้หน้าตาเหมือนเกมจริงก่อน ค่อย ๆ ไปทีละขั้นนะ
import bentogame as game

CELL_PX = 26                                # 1 ช่องกริด = 26 พิกเซล
GRID_COLS = game.WIDTH // CELL_PX           # หน้าจอกว้างกี่ช่อง
GRID_ROWS = game.HEIGHT // CELL_PX          # หน้าจอสูงกี่ช่อง

game.title("SNAKE")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

# งู = list ของช่อง [คอลัมน์, แถว] โดย "หัวงูอยู่ช่องแรกของ list" เสมอ — จำกฎนี้ไว้ให้ดี
snake_body = [[6, 8], [5, 8], [4, 8]]

# แปลง "ช่องกริด" ของแต่ละปล้อง -> กล่องสีเขียวบนจอ (ช่อง x 26 พิกเซล = ตำแหน่งจริง)
body_squares = [game.Box(col * CELL_PX, row * CELL_PX, CELL_PX - 2, CELL_PX - 2, game.GB_DARK)
                for col, row in snake_body]
body_squares[0].set_color(game.GB_LIGHT)    # หัวงูสีอ่อนกว่า ให้เห็นชัดว่าหัวอยู่ไหน

food_square = game.Box(7 * CELL_PX, 4 * CELL_PX, CELL_PX - 2, CELL_PX - 2, game.GB_LIGHTEST)
score = 0
score_text = game.Text("Score: 0", 10, 8, game.WHITE)

# ----- เติมส่วนนี้เอง -----
#    ลองขยับ snake_body เริ่มต้นไปวางตรงอื่น หรือเปลี่ยนสีหัวงู ดูว่าหน้าจอเปลี่ยนตามไหม

# ภาพยังนิ่งอยู่ คาบหน้าเราจะเติม logic เดินใน update() (Back = ออก / Start = เริ่มใหม่ จัดการให้โดย game.run())
def update():
    pass                                    # ทุกเฟรมไม่ต้องทำอะไร ภาพเลยนิ่ง

game.run(update, fps=9)
