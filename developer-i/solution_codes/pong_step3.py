# pong_step3.py — สร้าง Pong #3 (คาบ 13): ตีลูกกลับ (สะท้อน + เร่ง + มุม + สปิน)
#
# เรื่องราวของ step นี้: คราวนี้ไม้ของเรา "ตีโดน" ลูกได้จริงแล้ว ตีโดนตรงไหนของไม้
#   ลูกก็เด้งออกมุมต่างกัน (โดนปลายไม้ = มุมชัน), ตียิ่งหลายครั้งลูกยิ่งเร็วขึ้น (มี
#   เพดาน), และถ้าไม้กำลังเคลื่อนตอนตีก็ใส่ "สปิน" ให้ลูกด้วย เริ่มรู้สึกเหมือนปิงปองจริง
#
# ใหม่จาก step2: ลูกชนไม้เราแล้ว "ตีกลับ" — สะท้อนทิศ ball_vx, เร่งความเร็ว (มี cap),
#   มุมตามจุดที่โดน (contact angle), เติมสปินจากความเร็วไม้
# STUDENT WRITES (30% นี้): เงื่อนไข game.hit(ball, player_paddle) -> คำนวณความเร็วใหม่
# CORE IT CALLS (70%): game.hit, game.sfx("paddle") + ของเดิม
# C step == Python step on screen: page_game_pong_lite.c step3 -> การสะท้อน/มุม/สปินเหมือนกัน
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

game.title("PONG")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

player_paddle = game.Box(20, PADDLE_START_Y, PADDLE_W, PADDLE_H, game.GB_LIGHT)
ball = game.Box(game.WIDTH // 2, game.HEIGHT // 2, BALL_SIZE, BALL_SIZE, game.GB_LIGHTEST)
game.Text("Hit the ball back with your paddle!", 16, 12, game.WHITE)

ball_x, ball_y = float(game.WIDTH // 2), float(game.HEIGHT // 2)
ball_vx, ball_vy = -6.2, 3.4      # เสิร์ฟมาทางเรา (vx ลบ = วิ่งมาทางซ้าย)
player_y, player_speed = float(PADDLE_START_Y), 0.0

def on_each_frame():
    global ball_x, ball_y, ball_vx, ball_vy, player_y, player_speed
    keys = game.keys()
    # (Back=ออก / Start=เริ่มใหม่ — game.run() จัดการให้)

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

    # --- STUDENT 30%: ตีกลับเมื่อชนไม้เรา (ลูกกำลังวิ่งเข้าหาไม้: ball_vx < 0) ---
    # ----- เติมส่วนนี้เอง: ถ้าชนไม้ -> กลับทิศ + เร่ง(มีเพดาน) + ใส่มุม + ใส่สปิน -----
    if ball_vx < 0 and game.hit(ball, player_paddle):
        # hit_offset: โดนบน/กลาง/ล่างของไม้ = -1..1 (ใช้กำหนดมุมเด้ง)
        hit_offset = ((ball_y + BALL_SIZE / 2) - (player_y + PADDLE_H / 2)) / (PADDLE_H / 2)
        ball_vx = min(-ball_vx + SPEEDUP, BALL_CAP)         # กลับทิศ + เร่ง (cap)
        ball_vy += hit_offset * 2.0                         # มุมตามจุดสัมผัส
        ball_vy += player_speed * SPIN                      # สปินจากไม้ที่กำลังเคลื่อน
        game.sfx("paddle")

    # ฝั่งขวายังเป็นกำแพง (คาบหน้าทำคู่ต่อสู้ + คะแนน)
    if ball_x >= game.WIDTH - BALL_SIZE:
        ball_vx = -abs(ball_vx)

game.run(on_each_frame, fps=60)
