# โครงเว้นบางส่วนให้คุณเติมเอง
# เฉลย: starter/flappy_step4.py / ใบ้: ในใบงาน session
# flappy_step4.py — สร้าง Flappy #4: ชนท่อ = จบ + ผ่านท่อ = +1 แต้ม
#   STEP นี้คือเกมที่เล่นจบได้สมบูรณ์ (beginner-complete) เทียบได้กับ reference/flappy_full.py
# -----------------------------------------------------------------------------
# เรื่องราวของคาบนี้:
#   ตอนนี้เรามีนก มีท่อ แต่ยังแพ้ไม่ได้ ชนะไม่ได้ คาบนี้เราจะเติมกติกาเข้าไป:
#   ชนท่อ = จบเกม, ลอดท่อผ่านได้ = +1 แต้ม เคล็ดลับคือติดธง "scored" ที่ท่อ
#   เพื่อกันนับแต้มซ้ำท่อเดิม จบคาบนี้เราจะได้เกม Flappy ที่เล่นได้จริงทั้งเกม
#
# ส่วนที่คุณจะได้เขียนเองคาบนี้ (กติกาแพ้/ชนะ):
#     - ชนท่อบนหรือท่อล่าง (AABB) → GAME OVER + เสียง "die"
#     - ท่อเลื่อนพ้นตัวนกครั้งแรก → +1 แต้ม + เสียง "point" (กัน scored ซ้ำ)
# 70% core ที่เพิ่ม: game.hit() (ชน AABB), game.sfx("point"/"die")
#   (bentogame.py:355,64)
# C step == Python step บนจอ: c_track/flappy_step4.c (flappy_hit_pipe :231)
# อ้างอิง: reference/flappy_full.py:54-60
import bentogame as game
import random

GRAVITY = 0.45                                  # แรงโน้มถ่วง
FLAP = -7.4                                     # แรงกระพือ
SPEED = 3.4                                     # ความเร็วท่อเลื่อนซ้าย
GAP = 152                                       # ช่องว่างที่นกลอด
PIPE_WIDTH = 64                                 # ความกว้างของท่อ
SPACING = 270                                   # ระยะห่างระหว่างท่อ

game.title("FLAPPY")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

bird = game.Box(150, 180, 34, 34, game.GB_LIGHTEST)
bird_y = 180.0
bird_velocity = 0.0
score = 0
score_label = game.Text("0", 384, 16, game.WHITE)

pipes = []
def add_pipe(start_x):
    gap_top = random.randint(60, game.HEIGHT - 60 - GAP)
    pipes.append({
        "x": float(start_x), "gap_top": gap_top, "scored": False,   # ใหม่: ธง scored กันนับซ้ำ
        "top": game.Box(start_x, 0, PIPE_WIDTH, gap_top, game.GB_DARK),
        "bot": game.Box(start_x, gap_top + GAP, PIPE_WIDTH,
                        game.HEIGHT - gap_top - GAP, game.GB_DARK),
    })
for index in range(3):
    add_pipe(game.WIDTH + index * SPACING)

def on_each_frame():
    global bird_y, bird_velocity, score
    keys = game.keys()
    if keys.a or keys.up:
        bird_velocity = FLAP; game.sfx("flap")
    bird_velocity += GRAVITY
    bird_y += bird_velocity
    if bird_y < 0: bird_y, bird_velocity = 0, 0
    if bird_y > game.HEIGHT - bird.h:
        game.sfx("die")
        game.Text("GAME OVER", 320, 180, game.RED); return False
    bird.move_to(bird.x, bird_y)

    for pipe in pipes:
        pipe["x"] -= SPEED
        if pipe["x"] < -PIPE_WIDTH:
            pipe["x"] = max(other["x"] for other in pipes) + SPACING
            pipe["gap_top"] = random.randint(60, game.HEIGHT - 60 - GAP)
            pipe["scored"] = False
            pipe["top"].resize(PIPE_WIDTH, pipe["gap_top"])
            pipe["bot"].resize(PIPE_WIDTH, game.HEIGHT - pipe["gap_top"] - GAP)
        pipe["top"].move_to(pipe["x"], 0)
        pipe["bot"].move_to(pipe["x"], pipe["gap_top"] + GAP)

        # ----- เติมส่วนนี้เอง (งานของคุณ): กติกาแพ้/ชนะ (ชนท่อ + นับแต้ม) -----
        # TODO 1 (แพ้ = ชนท่อ):
        #   1) เช็คว่านกชนท่อบน "หรือ" ท่อล่าง ด้วย game.hit(...) (รับ 2 กล่อง คืน True/False)
        #      กล่องนกคือ bird, ท่ออยู่ที่ pipe["top"] กับ pipe["bot"]
        #   2) ถ้าชน → เล่น game.sfx(...) เสียงตาย, โชว์ game.Text(...) คำว่า GAME OVER,
        #      แล้ว return False เพื่อจบเกม
        # TODO 2 (ได้แต้ม = ลอดท่อผ่าน):
        #   1) เช็ค 2 เงื่อนไขพร้อมกัน: ท่อนี้ยังไม่เคยนับ (ดู pipe["scored"])
        #      และขอบขวาของท่อเลื่อนพ้นตำแหน่งนกไปแล้ว (เทียบ pipe["x"]+PIPE_WIDTH กับ bird.x)
        #   2) ถ้าใช่ → ปักธง pipe["scored"] = True (กันนับซ้ำ), บวก score, เล่น game.sfx(...) เสียงแต้ม
        #   3) อัปเดตป้ายคะแนนบนจอด้วยเมธอด .set(...) ของ score_label (ส่งคะแนนเป็น str)
        #   ใบ้ API (bentogame.py): hit():355  sfx():64  Text:227  Text.set():233
        pass   # ลบ pass ออกเมื่อเริ่มเขียน

game.run(on_each_frame, fps=50)
