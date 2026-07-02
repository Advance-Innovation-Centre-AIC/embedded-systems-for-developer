# flappy_step4.py — สร้าง Flappy #4: ชนท่อ = จบ + ผ่านท่อ = +1 แต้ม
#   STEP นี้ = เกมเล่นจบสมบูรณ์ (beginner-complete) เหมือน reference/flappy_full.py
# -----------------------------------------------------------------------------
# เรื่องราวของคาบนี้:
#   ตอนนี้เรามีนก มีท่อแล้ว แต่ยัง "แพ้ไม่ได้ ชนะไม่ได้". คาบนี้เราจะเติม "กติกา":
#   ชนท่อ = จบเกม, ลอดท่อผ่านได้ = +1 แต้ม. เคล็ดลับนิดนึงนะ คือเราติดธง "scored"
#   ไว้ที่ท่อแต่ละอัน เพื่อกันไม่ให้นับแต้มซ้ำท่อเดิม. จบคาบนี้เราจะได้เกม Flappy
#   ที่เล่นได้จริง ครบทั้งเกม
#
# ส่วนที่คุณจะเติมเองในคาบนี้ (กติกาแพ้/ชนะ):
#     - ชนท่อบนหรือท่อล่าง (AABB) → GAME OVER + เสียง "fall"
#     - ท่อเลื่อนพ้นตัวนกครั้งแรก → +1 แต้ม + เสียง "point" (กัน scored ซ้ำ)
# ส่วน core ที่เตรียมไว้ให้: game.hit() (ชน AABB), game.sfx("point"/"fall")
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
        "x": float(start_x), "gap_top": gap_top, "scored": False,   # ของใหม่คาบนี้: ธง scored ไว้กันนับซ้ำ
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
        game.sfx("fall")
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

        # ----- เติมส่วนนี้เอง: ชน + นับแต้ม -----------------------------------
        if game.hit(bird, pipe["top"]) or game.hit(bird, pipe["bot"]):   # ชนท่อ → จบ
            game.sfx("fall")
            game.Text("GAME OVER", 320, 180, game.RED); return False
        if not pipe["scored"] and pipe["x"] + PIPE_WIDTH < bird.x:        # ผ่านท่อ → +1
            pipe["scored"] = True
            score += 1
            game.sfx("point")
            score_label.set(str(score))

game.run(on_each_frame, fps=50)
