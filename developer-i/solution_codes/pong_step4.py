# pong_step4.py — สร้าง Pong #4 (คาบ 13): นับคะแนน + เสิร์ฟใหม่ + first-to-N
#   จบระดับ beginner: เล่นได้ครบ + parity-provable (ผลเท่า C step4)
#
# step นี้เกมของเราเป็น "เกมจริง" แล้ว ฝั่งขวามีคู่ต่อสู้ AI ง่าย ๆ ที่
#   "วิ่งตามลูก" ทำให้ตีโต้กันได้สองฝั่ง, ลูกหลุดออกข้าง = ได้แต้ม + เสิร์ฟลูกใหม่,
#   ใครถึง WIN_SCORE ก่อนชนะ มีแพ้ มีชนะ มีคะแนน เล่นจบเกมได้จริง
#
# ใหม่จาก step3: ไม้ขวากลายเป็น AI ง่าย ๆ ที่ "วิ่งตามลูก" (เพื่อให้ตีกลับได้ทั้งสองฝั่ง),
#   ลูกหลุดซ้าย/ขวา = ได้แต้ม, เสิร์ฟใหม่, ใครถึง WIN_SCORE ก่อนชนะ
# ส่วนที่คุณเขียนเอง: AI ตัวตามลูก (ไม้ขวา), การนับคะแนน + serve(),
#   เงื่อนไขจบเกม + เสียง win/lose
# ส่วนที่ core ทำให้: score_text.set, game.sfx("win"/"lose") + ของเดิม
# C step == Python step on screen: page_game_pong_lite.c step4 -> AI/คะแนน/เสิร์ฟ/จบเกมเหมือนกัน
#
# หมายเหตุ parity (§1E divergence #2): Pong ใช้ "ไม้เดียวที่ผู้เล่นคุม" (ซ้าย) เท่านั้น
#   เพราะ C track มีปุ่มหน้า A/B/X/RB รวมเป็น .action ปุ่มเดียว ผู้เล่น 2 คน
#   จึง mirror ข้าม track ไม่ได้ คู่ต่อสู้จึงเป็น AI (mirror สะอาดทั้งสอง track)
#   step5 ต่อยอด AI ตัวนี้ด้วยโหมด EASY/HARD + เมนู
#
# tear-down ของจริง: page_game_pong.c:284-308 (scoring), :310-316 (AI), :430-470 (serve)
# Python twin: pong_full.py:40-44 (AI), :60-68 (scoring)
import bentogame as game

PADDLE_W, PADDLE_H, BALL_SIZE = 14, 90, 14
PADDLE_START_Y = game.HEIGHT // 2 - PADDLE_H // 2

ACCEL, MAX_SPEED, FRICTION = 1.5, 12.0, 0.78
SPEEDUP, BALL_CAP, SPIN = 0.35, 14.0, 0.28
SERVE_SPEED = 6.2
AI_SPEED = 4.2         # ความเร็วที่ไม้ AI วิ่งตามลูก
WIN_SCORE = 7          # first-to-N

game.title("PONG")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

player_paddle = game.Box(20, PADDLE_START_Y, PADDLE_W, PADDLE_H, game.GB_LIGHT)
ai_paddle = game.Box(game.WIDTH - 20 - PADDLE_W, PADDLE_START_Y, PADDLE_W, PADDLE_H, game.GB_LIGHT)
ball = game.Box(game.WIDTH // 2, game.HEIGHT // 2, BALL_SIZE, BALL_SIZE, game.GB_LIGHTEST)
score_text = game.Text("0 : 0", game.WIDTH // 2 - 24, 12, game.WHITE)

ball_x, ball_y = float(game.WIDTH // 2), float(game.HEIGHT // 2)
ball_vx, ball_vy = -SERVE_SPEED, 3.4
player_y, player_speed = float(PADDLE_START_Y), 0.0
ai_y = float(PADDLE_START_Y)
player_score, ai_score = 0, 0
game_over = False

def serve(direction):
    global ball_x, ball_y, ball_vx, ball_vy
    ball_x, ball_y = game.WIDTH / 2, game.HEIGHT / 2
    ball_vx, ball_vy = SERVE_SPEED * direction, 3.4

def on_each_frame():
    global ball_x, ball_y, ball_vx, ball_vy, player_y, player_speed, ai_y
    global player_score, ai_score, game_over
    keys = game.keys()
    if keys.start or game_over:
        return False

    # ไม้ผู้เล่น (ซ้าย) UP/DOWN
    if keys.up and not keys.down:    player_speed -= ACCEL
    elif keys.down and not keys.up:  player_speed += ACCEL
    else:                            player_speed *= FRICTION
    player_speed = max(-MAX_SPEED, min(MAX_SPEED, player_speed))
    player_y = max(0, min(game.HEIGHT - PADDLE_H, player_y + player_speed))
    player_paddle.move_to(20, player_y)

    # ----- เติมส่วนนี้เอง: ไม้ AI (ขวา) = วิ่งตามลูก -----
    # อยากให้กลางไม้ตรงกับลูก -> ลูกอยู่ล่างก็ลง, อยู่บนก็ขึ้น
    target_y = ball_y - PADDLE_H / 2
    if ai_y < target_y - 6:    ai_y += AI_SPEED
    elif ai_y > target_y + 6:  ai_y -= AI_SPEED
    ai_y = max(0, min(game.HEIGHT - PADDLE_H, ai_y))
    ai_paddle.move_to(ai_paddle.x, ai_y)

    # ลูกบอล + เด้งบน/ล่าง
    ball_x += ball_vx
    ball_y += ball_vy
    if ball_y <= 0 or ball_y >= game.HEIGHT - BALL_SIZE:
        ball_vy = -ball_vy
        game.sfx("wall")
    ball.move_to(ball_x, ball_y)

    # ตีไม้ซ้าย (เหมือน step3)
    if ball_vx < 0 and game.hit(ball, player_paddle):
        hit_offset = ((ball_y + BALL_SIZE / 2) - (player_y + PADDLE_H / 2)) / (PADDLE_H / 2)
        ball_vx = min(-ball_vx + SPEEDUP, BALL_CAP)
        ball_vy += hit_offset * 2.0 + player_speed * SPIN
        game.sfx("paddle")

    # ตีไม้ขวา = mirror ของไม้ซ้าย (ball_vx > 0)
    elif ball_vx > 0 and game.hit(ball, ai_paddle):
        hit_offset = ((ball_y + BALL_SIZE / 2) - (ai_y + PADDLE_H / 2)) / (PADDLE_H / 2)
        ball_vx = -min(ball_vx + SPEEDUP, BALL_CAP)
        ball_vy += hit_offset * 2.0
        game.sfx("paddle")

    # ----- เติมส่วนนี้เอง: นับคะแนน + เสิร์ฟใหม่ + จบเกม -----
    # ลูกหลุดข้างไหน = อีกฝั่งได้แต้ม -> เสิร์ฟใหม่ -> เช็คผู้ชนะ
    if ball_x < 0:                              # หลุดซ้าย -> ฝั่งขวา (AI) ได้แต้ม
        ai_score += 1
        score_text.set("%d : %d" % (player_score, ai_score))
        serve(1)
    elif ball_x > game.WIDTH:                   # หลุดขวา -> ผู้เล่น (ซ้าย) ได้แต้ม
        player_score += 1
        score_text.set("%d : %d" % (player_score, ai_score))
        serve(-1)

    if player_score >= WIN_SCORE or ai_score >= WIN_SCORE:
        player_won = player_score > ai_score
        game.sfx("win" if player_won else "lose")
        game.Text("YOU WIN!" if player_won else "AI WINS",
                  game.WIDTH // 2 - 70, game.HEIGHT // 2,
                  game.GREEN if player_won else game.RED)
        game_over = True
        return False

game.run(on_each_frame, fps=60)
