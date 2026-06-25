# โครงเว้นบางส่วนให้คุณเติมเอง
# เฉลย: starter/pong_step2.py / ใบ้: ในใบงาน session
# pong_step2.py — สร้าง Pong #2 (คาบ 12): ไม้ตีฝั่งเราขยับ (เร่ง+เสียดทาน)
#
# step นี้เราได้ "ไม้ตี" ของตัวเองมาแล้ว กด UP/DOWN ให้ไม้
#   ค่อย ๆ เร่งความเร็ว พอปล่อยปุ่มมันจะ "ไถลแล้วหยุดเอง" เหมือนรถเบรก
#   ฟีลเดียวกับยานใน Shooter. ลูกบอลยังเด้งเล่นไปก่อน คาบหน้าค่อยตีโดน
#
# ใหม่จาก step1: ไม้ตีซ้าย (ของผู้เล่น) + บังคับด้วยจอย ขึ้น/ลง แบบ "เร่งความเร็ว"
# ส่วนที่คุณเขียนเอง: player_speed เร่งเมื่อกด up/down, เสียดทานเมื่อปล่อย,
#   จำกัดความเร็วสูงสุด, แล้ว clamp ไม้ให้อยู่ในสนาม
# ส่วนที่ระบบเตรียมให้: game.start, game.Box, game.keys, game.run
# C step == Python step on screen: page_game_pong_lite.c step2 -> ไม้เลื่อนรู้สึกเดียวกัน
#
# tear-down ของจริง: page_game_pong.c:370-387 (accel/friction/clamp ไม้ผู้เล่น)
# Python twin: pong_full.py:33-38
import bentogame as game

PADDLE_W, PADDLE_H, BALL_SIZE = 14, 90, 14
PADDLE_START_Y = game.HEIGHT // 2 - PADDLE_H // 2   # วางไม้กลางจอตอนเริ่ม

ACCEL    = 1.5      # เร่งต่อเฟรมเมื่อกดค้าง
MAX_SPEED = 12.0    # ความเร็วสูงสุดของไม้
FRICTION = 0.78     # หน่วงเมื่อปล่อยปุ่ม (คูณความเร็วให้ค่อย ๆ เหลือศูนย์)

game.start()

player_paddle = game.Box(20, PADDLE_START_Y, PADDLE_W, PADDLE_H, game.GB_LIGHT)
ball = game.Box(game.WIDTH // 2, game.HEIGHT // 2, BALL_SIZE, BALL_SIZE, game.GB_LIGHTEST)
game.Text("Move your paddle: UP / DOWN", 16, 12, game.WHITE)

ball_x, ball_y = float(game.WIDTH // 2), float(game.HEIGHT // 2)
ball_vx, ball_vy = 6.2, 3.4
player_y, player_speed = float(PADDLE_START_Y), 0.0   # ตำแหน่ง + ความเร็วไม้ของเรา

def on_each_frame():
    global ball_x, ball_y, ball_vx, ball_vy, player_y, player_speed
    keys = game.keys()
    if keys.start:
        return False

    # ----- เติมส่วนนี้เอง (งานของคุณ): ขยับไม้ตีแบบเร่ง + เสียดทาน + กันออกนอกจอ -----
    # TODO: ทำให้ไม้ตี "เร่งตอนกดค้าง" และ "ไถลแล้วหยุดเองตอนปล่อย" (ฟีลเดียวกับยาน Shooter)
    #   1) อ่านปุ่มขึ้น/ลงจาก keys.up / keys.down  (game.keys ที่ bentogame.py:262)
    #   2) ถ้ากดขึ้น ให้ player_speed เร่งไปทางขึ้น / ถ้ากดลง ให้เร่งไปทางลง — ก้าวละ ACCEL
    #   3) ถ้าไม่ได้กดอะไรเลย ให้ player_speed ค่อย ๆ ลดลงด้วย FRICTION (คูณให้เข้าใกล้ 0)
    #   4) จำกัด player_speed ไม่ให้เกินช่วง -MAX_SPEED .. MAX_SPEED  (ใบ้: ใช้ max() คู่กับ min())
    #   5) บวก player_speed เข้ากับ player_y แล้ว clamp ให้อยู่ในสนาม 0 .. game.HEIGHT-PADDLE_H
    #   6) ย้ายไม้ไปตำแหน่งใหม่ด้วย player_paddle.move_to(...)  (move_to ที่ bentogame.py:188)
    #   (ทิศของแกน y: ค่าน้อย=บน ค่ามาก=ล่าง — ลองปรับเครื่องหมายเอง / ดู starter ถ้าติด)
    pass   # <- ลบ pass ออกเมื่อเริ่มเขียน

    # ลูกบอล (ยังเด้งทั้ง 4 ด้าน — คาบหน้าทำให้ตีกลับด้วยไม้)
    ball_x += ball_vx
    ball_y += ball_vy
    if ball_y <= 0 or ball_y >= game.HEIGHT - BALL_SIZE:
        ball_vy = -ball_vy
        game.sfx("wall")
    if ball_x <= 0 or ball_x >= game.WIDTH - BALL_SIZE:
        ball_vx = -ball_vx
    ball.move_to(ball_x, ball_y)

game.run(on_each_frame, fps=60)
