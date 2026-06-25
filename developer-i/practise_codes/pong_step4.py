# โครงเว้นไว้ให้เราเติมเอง เติมช่องที่ทำเครื่องหมายไว้ให้ครบ แล้วเกมจะเล่นได้จริง
# เฉลย: starter/pong_step4.py   /   ใบ้: ในใบงาน session
#
# pong_step4.py — สร้าง Pong #4 (คาบ 13): นับคะแนน + เสิร์ฟใหม่ + first-to-N
#   จบระดับ beginner: เล่นได้ครบ และผลตรงกับ C step4
#
# เรื่องราวของ step นี้: ตอนนี้เกมของเราเป็นเกมที่เล่นได้จริงแล้ว ฝั่งขวามีคู่ต่อสู้ AI
#   ง่าย ๆ ที่วิ่งตามลูก ทำให้ตีโต้กันได้สองฝั่ง, ลูกหลุดออกข้าง = ได้แต้ม แล้วเสิร์ฟลูกใหม่,
#   ใครถึง WIN_SCORE ก่อนเป็นฝ่ายชนะ มีแพ้ มีชนะ มีคะแนน เล่นจนจบเกมได้
#
# ใหม่จาก step3: ไม้ขวากลายเป็น AI ง่าย ๆ ที่วิ่งตามลูก (เพื่อให้ตีกลับได้ทั้งสองฝั่ง),
#   ลูกหลุดซ้าย/ขวา = ได้แต้ม, เสิร์ฟใหม่, ใครถึง WIN_SCORE ก่อนชนะ
# ส่วนที่เราเขียนเอง: AI ตัวตามลูก (ไม้ขวา), การนับคะแนน + serve(),
#   เงื่อนไขจบเกม + เสียง win/lose
# ส่วนที่ core เตรียมไว้ให้: score_text.set, game.sfx("win"/"lose") + ของเดิม
# โค้ด C กับ Python ทำงานตรงกันบนจอ: page_game_pong_lite.c step4 -> AI/คะแนน/เสิร์ฟ/จบเกมเหมือนกัน
#
# หมายเหตุ parity (§1E divergence #2): Pong ใช้ "ไม้เดียวที่ผู้เล่นคุม" (ซ้าย) เท่านั้น
#   เพราะ C track มีปุ่มหน้า A/B/X/RB รวมเป็น .action ปุ่มเดียว — ผู้เล่น 2 คน
#   จึง mirror ข้าม track ไม่ได้. คู่ต่อสู้จึงเป็น AI (mirror สะอาดทั้งสอง track).
#   step5 ต่อยอด AI ตัวนี้ด้วยโหมด EASY/HARD + เมนู.
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

game.start()

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

    # ----- เติมส่วนนี้เอง (งานของคุณ): ไม้ AI (ขวา) วิ่งตามลูก -----
    # เขียน AI ง่าย ๆ ที่ขยับไม้ขวาเข้าหาลูก:
    #   1) คำนวณตำแหน่งเป้า (target) ที่อยากให้ "กลางไม้" ไปตรงกับ ball_y
    #      (ระวัง: ai_y คือขอบบนของไม้ ไม่ใช่กลางไม้ — ต้องหักครึ่งความสูง PADDLE_H)
    #   2) ถ้า ai_y ยังอยู่เหนือเป้า -> เลื่อนลงทีละ AI_SPEED ; ถ้าอยู่ใต้เป้า -> เลื่อนขึ้น
    #      (ใส่ระยะ deadzone เล็ก ๆ กันไม้สั่น ลองปรับเอง / ดู starter ถ้าติด)
    #   3) clamp ai_y ให้อยู่ในจอ (เทียบกับไม้ผู้เล่นด้านบนเป็นแบบอย่าง)
    #   4) ย้ายไม้จริงด้วย ai_paddle.move_to(ai_paddle.x, ai_y)
    pass   # <- ลบ pass ออกเมื่อเริ่มเขียน

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

    # ----- เติมส่วนนี้เอง (งานของคุณ): นับคะแนน + เสิร์ฟใหม่ + จบเกม -----
    # ตรวจว่าลูกหลุดข้างจอหรือยัง แล้วให้แต้ม + เสิร์ฟใหม่ + เช็คผู้ชนะ:
    #   1) ลูกหลุดซ้าย (ball_x น้อยกว่า 0) -> ฝั่งขวา (AI) ได้แต้ม: เพิ่ม ai_score
    #      แล้วเรียก serve() ให้เสิร์ฟไปทางขวา (ทิศ +1)
    #   2) ลูกหลุดขวา (ball_x เกินขอบจอ game.WIDTH) -> ผู้เล่นได้แต้ม: เพิ่ม player_score
    #      แล้ว serve() เสิร์ฟไปทางซ้าย (ทิศ -1)
    #   3) ทุกครั้งที่แต้มเปลี่ยน อัปเดตป้ายคะแนนด้วย score_text.set(...)
    #      (ประกอบสตริงรูปแบบ "คะแนนซ้าย : คะแนนขวา" เอง)
    #   4) ถ้าใครถึง WIN_SCORE แล้ว -> เล่นเสียงด้วย game.sfx("win") หรือ game.sfx("lose"),
    #      โชว์ผลด้วย game.Text(...), ตั้ง game_over = True แล้ว return False เพื่อจบเกม
    pass   # <- ลบ pass ออกเมื่อเริ่มเขียน

game.run(on_each_frame, fps=60)
