# โครงเริ่มต้น มีช่องให้คุณเติมเองอยู่ข้างใน
# ถ้าติด ดูเฉลยได้ที่ starter/pong_step3.py หรือดูใบ้ในใบงานของคาบนี้
# pong_step3.py — Pong #3 (คาบ 13): ตีลูกกลับ (สะท้อน + เร่ง + มุม + สปิน)
#
# คาบนี้ไม้ของเรา "ตีโดน" ลูกได้จริงแล้ว ตีโดนตรงไหนของไม้ ลูกก็เด้งออกมุมต่างกัน
#   (โดนปลายไม้จะได้มุมชัน) ตียิ่งหลายครั้งลูกก็ยิ่งเร็วขึ้น แต่เราใส่เพดานไว้ไม่ให้
#   เร็วเกินไป และถ้าไม้กำลังเคลื่อนตอนตี เราก็ใส่ "สปิน" ให้ลูกด้วย เริ่มใกล้เคียง
#   ปิงปองจริงแล้วนะ
#
# ที่เพิ่มจาก step2: ลูกชนไม้เราแล้วตีกลับ คือสะท้อนทิศ ball_vx, เร่งความเร็ว (มี cap),
#   ใส่มุมตามจุดที่โดน (contact angle), แล้วเติมสปินจากความเร็วไม้
# ส่วนที่คุณเขียนเอง: เงื่อนไข game.hit(ball, player_paddle) แล้วคำนวณความเร็วใหม่
# ส่วนที่ระบบเตรียมให้: game.hit, game.sfx("paddle") และของเดิม
# ฝั่ง C ทำเหมือนกัน: page_game_pong_lite.c step3 ทำการสะท้อน/มุม/สปินแบบเดียวกัน
#
# tear-down ของจริง: page_game_pong.c:257-268 (left paddle collision)
# Python twin: pong_full.py:54-55
import bentogame as game

PADDLE_W, PADDLE_H, BALL_SIZE = 14, 90, 14
PADDLE_START_Y = game.HEIGHT // 2 - PADDLE_H // 2

ACCEL, MAX_SPEED, FRICTION = 1.5, 12.0, 0.78
SPEEDUP  = 0.35          # เพิ่มความเร็วลูกทุกครั้งที่ตีโดน
BALL_CAP = 14.0          # เพดานความเร็วลูก
SPIN     = 0.28          # สัดส่วนความเร็วไม้ที่ใส่เป็นสปิน

game.start()

player_paddle = game.Box(20, PADDLE_START_Y, PADDLE_W, PADDLE_H, game.GB_LIGHT)
ball = game.Box(game.WIDTH // 2, game.HEIGHT // 2, BALL_SIZE, BALL_SIZE, game.GB_LIGHTEST)
game.Text("Hit the ball back with your paddle!", 16, 12, game.WHITE)

ball_x, ball_y = float(game.WIDTH // 2), float(game.HEIGHT // 2)
ball_vx, ball_vy = -6.2, 3.4      # เสิร์ฟมาทางเรา (vx ลบ = วิ่งมาทางซ้าย)
player_y, player_speed = float(PADDLE_START_Y), 0.0

def on_each_frame():
    global ball_x, ball_y, ball_vx, ball_vy, player_y, player_speed
    keys = game.keys()
    if keys.start:
        return False

    # ไม้ผู้เล่น (เหมือน step2)
    if keys.up and not keys.down:    player_speed -= ACCEL
    elif keys.down and not keys.up:  player_speed += ACCEL
    else:                            player_speed *= FRICTION
    player_speed = max(-MAX_SPEED, min(MAX_SPEED, player_speed))
    player_y = max(0, min(game.HEIGHT - PADDLE_H, player_y + player_speed))
    player_paddle.move_to(20, player_y)

    # ลูกบอล + เด้งบน/ล่าง
    ball_x += ball_vx
    ball_y += ball_vy
    if ball_y <= 0 or ball_y >= game.HEIGHT - BALL_SIZE:
        ball_vy = -ball_vy
        game.sfx("wall")
    ball.move_to(ball_x, ball_y)

    # ตีกลับเมื่อชนไม้เรา (ลูกกำลังวิ่งเข้าหาไม้: ball_vx < 0)
    # ----- เติมส่วนนี้เอง (งานของคุณ): ตีลูกกลับเมื่อชนไม้ (สะท้อน + เร่ง + มุม + สปิน) -----
    # เขียนเป็น if ... : แล้วทำ 4 ขั้นข้างใน
    #   1) เงื่อนไข: เช็คว่าลูกกำลังวิ่งเข้าหาไม้ (ball_vx ติดลบ) และชนไม้จริง
    #      โดยใช้ game.hit(ball, player_paddle)  (ดู bentogame.py:355)
    #   2) กลับทิศ + เร่ง: พลิกเครื่องหมาย ball_vx ให้วิ่งกลับ แล้วบวก SPEEDUP เพิ่มความเร็ว
    #      อย่าลืมจำกัดไม่ให้เกิน BALL_CAP (ลองนึกถึง min(...) ถ้าติดดู starter ได้)
    #   3) ใส่มุมตามจุดสัมผัส: หา hit_offset คือโดนบน/กลาง/ล่างของไม้ ให้ได้ค่าราว -1..1
    #      (ใช้ตำแหน่งกลางลูก ball_y+BALL_SIZE/2 เทียบกลางไม้ player_y+PADDLE_H/2)
    #      แล้วบวกผลของ hit_offset เข้า ball_vy ให้เด้งเป็นมุม
    #   4) ใส่สปินจากไม้: บวก player_speed คูณ SPIN เข้า ball_vy แล้วเรียก game.sfx("paddle")
    pass   # ลบ pass ออกเมื่อเริ่มเขียน

    # ฝั่งขวายังเป็นกำแพง (คาบหน้าทำคู่ต่อสู้ + คะแนน)
    if ball_x >= game.WIDTH - BALL_SIZE:
        ball_vx = -abs(ball_vx)

game.run(on_each_frame, fps=60)
