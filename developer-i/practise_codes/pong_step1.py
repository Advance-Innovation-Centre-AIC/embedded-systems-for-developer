# โครงเว้น 30% — เติมช่องที่เป็นงานของคุณให้ครบ แล้วเกมจะเล่นได้จริง
# เฉลย: starter/pong_step1.py   /   ใบ้: ในใบงาน session
#
# pong_step1.py — สร้าง Pong #1 (คาบ 12): ลูกบอลเด้งกำแพงบน/ล่าง (ยังไม่มีไม้ตี)
#
# เรื่องราวของ step นี้: เราจะปล่อยลูกบอลหนึ่งลูกให้วิ่งในจอ พอมันชนกำแพง
#   บน/ล่าง ก็เด้งกลับ เหมือนลูกแก้วเด้งในกล่อง นี่คือหัวใจของฟิสิกส์เกม
#
# STUDENT WRITES (30% นี้): สถานะลูกบอล ball_x/ball_y + ความเร็ว ball_vx/ball_vy
#   + ขยับลูก (integrate) + เด้งกำแพงบน/ล่าง (reflect) ใน on_each_frame()
# CORE IT CALLS (70% ที่เรียกใช้): game.start, game.Box, game.Text,
#   game.run(on_each_frame, fps), game.sfx("wall")
# C step == Python step on screen: page_game_pong_lite.c step1 (tick) ให้ผลเดียวกัน
#   ลูกบอลวิ่ง+เด้งบน/ล่างเหมือนกันเป๊ะ
#
# tear-down ของจริง: page_game_pong.c:241-254 (integrate + top/bottom bounce)
# Python twin: pong_full.py:48-51 (subset — ยังไม่มีไม้/คะแนน)
import bentogame as game

BALL_SIZE = 14                                 # ลูกบอลกว้าง/สูงกี่พิกเซล

game.start()                                   # core: ล้างจอ + ปลุกจอย

ball = game.Box(game.WIDTH // 2, game.HEIGHT // 2, BALL_SIZE, BALL_SIZE, game.GB_LIGHTEST)
game.Text("Pong - ball bounces the walls", 16, 12, game.WHITE)

# --- สถานะลูกบอล (ตำแหน่ง + ความเร็วต่อเฟรม) ---
# ============ ----- เติมส่วนนี้เอง (งานของคุณ): ตั้งค่าเริ่มต้นของลูกบอล ----- ============
# TODO: 1) ตั้ง ball_x, ball_y ให้ลูกเริ่มกลางจอ (อ่านค่าจาก game.WIDTH, game.HEIGHT)
#       2) ตั้งความเร็วต่อเฟรม ball_vx, ball_vy เป็นเลขทศนิยม
#          (บวก=ไปขวา/ลง, ลบ=ไปซ้าย/ขึ้น — เลือกค่าเล็กๆ ลองปรับเอง / ดู starter ถ้าติด)
ball_x, ball_y = 0.0, 0.0       # <- แก้ค่าให้เริ่มกลางจอเมื่อเริ่มเขียน
ball_vx, ball_vy = 0.0, 0.0     # <- ใส่ความเร็วต่อเฟรมเมื่อเริ่มเขียน

def on_each_frame():
    global ball_x, ball_y, ball_vx, ball_vy
    keys = game.keys()
    if keys.start:                             # กด Start = ออก
        return False

    # --- ขยับลูกหนึ่งก้าว แล้วเด้งกำแพงบน/ล่าง ---
    # ============ ----- เติมส่วนนี้เอง (งานของคุณ): ขยับลูก + เด้งกำแพงบน/ล่าง ----- ============
    # TODO: 1) "ขยับ" หนึ่งก้าว: บวกความเร็วแต่ละแกนเข้ากับตำแหน่งแกนนั้น (integrate)
    #       2) เช็กว่าลูกชนขอบบนหรือขอบล่างหรือยัง — ขอบบนคือ y ต่ำสุด,
    #          ขอบล่างคือ y ที่ขอบลูกแตะก้นจอ (คิดจาก game.HEIGHT กับ BALL_SIZE)
    #       3) ถ้าชน ให้กลับทิศความเร็วแนวตั้ง (สลับเครื่องหมาย ball_vy) แล้วเรียก game.sfx("wall")
    #       4) ยังไม่มีไม้ตี: ถ้าชนขอบซ้าย/ขวา ให้กลับทิศ ball_vx ด้วย กันลูกหลุดจอ
    pass   # <- ลบ pass ออกเมื่อเริ่มเขียน

    ball.move_to(ball_x, ball_y)               # core: วาดลูกที่ตำแหน่งใหม่

game.run(on_each_frame, fps=60)                # core: เรียก on_each_frame() 60 ครั้ง/วินาที
