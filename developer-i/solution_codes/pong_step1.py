# pong_step1.py — สร้าง Pong #1 (คาบ 5): ลูกบอลเด้งกำแพงบน/ล่าง (ยังไม่มีไม้ตี)
#
# เรื่องราวของ step นี้: เราจะปล่อยลูกบอลหนึ่งลูกให้วิ่งในจอ พอมันชนกำแพง
#   บน/ล่าง ก็เด้งกลับ เหมือนลูกแก้วเด้งในกล่อง ซึ่งเป็นหัวใจของฟิสิกส์เกม
#
# ส่วนที่คุณเขียนเอง: สถานะลูกบอล ball_x/ball_y + ความเร็ว ball_vx/ball_vy
#   + ขยับลูก (integrate) + เด้งกำแพงบน/ล่าง (reflect) ใน on_each_frame()
# ส่วนที่ core เตรียมให้เรียกใช้: game.start, game.Box, game.Text,
#   game.run(on_each_frame, fps), game.sfx("wall")
# โค้ด C ฝั่งเฟิร์มแวร์ให้ผลบนจอเหมือนกัน: page_game_pong_lite.c step1 (tick)
#   ลูกบอลวิ่งและเด้งบน/ล่างเหมือนกันเป๊ะ
#
# ที่มาในเฟิร์มแวร์จริง: page_game_pong.c:241-254 (integrate + top/bottom bounce)
# เวอร์ชัน Python คู่กัน: pong_full.py:48-51 (เป็นส่วนย่อย ยังไม่มีไม้ตี/คะแนน)
import bentogame as game

BALL_SIZE = 14                                 # ลูกบอลกว้าง/สูงกี่พิกเซล

game.title("PONG")                             # core: หน้าเริ่ม (Start=เล่น Back=ออก) + ล้างจอ

ball = game.Box(game.WIDTH // 2, game.HEIGHT // 2, BALL_SIZE, BALL_SIZE, game.GB_LIGHTEST)
game.Text("Pong - ball bounces the walls", 16, 12, game.WHITE)

# ----- เติมส่วนนี้เอง: สถานะลูกบอล (ตำแหน่ง + ความเร็วต่อเฟรม) -----
# ----- เติมส่วนนี้เอง: ตั้งตำแหน่งเริ่มต้นกลางจอ + ความเร็ว x/y -----
ball_x, ball_y = float(game.WIDTH // 2), float(game.HEIGHT // 2)
ball_vx, ball_vy = 6.2, 3.4                     # บวก = ไปขวา/ลง, ลบ = ไปซ้าย/ขึ้น

def on_each_frame():
    global ball_x, ball_y, ball_vx, ball_vy
    # (Back=ออก / Start=เริ่มใหม่ — game.run() จัดการให้ก่อนถึง on_each_frame)

    # ----- เติมส่วนนี้เอง: ขยับลูกหนึ่งก้าว แล้วเด้งกำแพงบน/ล่าง -----
    # ----- เติมส่วนนี้เอง: บวกความเร็วเข้าตำแหน่งคือการขยับ แล้วสะท้อนเมื่อชนกำแพง -----
    ball_x += ball_vx                           # ขยับลูกตามความเร็ว
    ball_y += ball_vy
    if ball_y <= 0:                            # ชนขอบบน -> กลับทิศแนวตั้ง
        ball_y = 0
        ball_vy = -ball_vy
        game.sfx("wall")
    if ball_y >= game.HEIGHT - BALL_SIZE:      # ชนขอบล่าง
        ball_y = game.HEIGHT - BALL_SIZE
        ball_vy = -ball_vy
        game.sfx("wall")

    # ยังไม่มีไม้ตี -> เด้งซ้าย/ขวาไว้ก่อน เพื่อให้ลูกอยู่ในจอ (คาบหน้าทำไม้ตี)
    if ball_x <= 0 or ball_x >= game.WIDTH - BALL_SIZE:
        ball_vx = -ball_vx

    ball.move_to(ball_x, ball_y)               # core: วาดลูกที่ตำแหน่งใหม่

game.run(on_each_frame, fps=60)                # core: เรียก on_each_frame() 60 ครั้ง/วินาที
