# flappy_step3.py — สร้าง Flappy #3: ท่อเลื่อนเข้ามา (ยังไม่ชน/ยังไม่นับแต้ม)
# -----------------------------------------------------------------------------
# เรื่องราวของคาบนี้:
#   ฟ้าโล่งๆ ยังไม่ค่อยท้าทายเท่าไหร่ คาบนี้เรามาเพิ่ม "ท่อ" ที่เลื่อนเข้ามา
#   จากขวาไปซ้ายกัน วิธีที่อยากให้คุณจำคือ เราสร้างท่อแค่ 3 ท่อ "ครั้งเดียว"
#   แล้ว "หมุนเวียนใช้ซ้ำ" (ท่อไหนหลุดขอบซ้าย ก็ส่งกลับไปขวาสุด แล้วสุ่ม
#   ช่องว่างใหม่) ไม่ต้องสร้างท่อใหม่ไม่รู้จบ ประหยัดหน่วยความจำและทำให้
#   ภาพลื่นขึ้น นี่คือ pattern "create once, recycle" ที่เกมจริงเขาใช้กันจริงๆ
#
# ส่วนที่คุณจะเขียนเองคาบนี้ (จัดการท่อ):
#     - list ของท่อ แต่ละท่อมี Box บน + Box ล่าง เว้นช่องว่าง GAP
#     - ทุกเฟรม: เลื่อนท่อไปทางซ้าย SPEED
#     - ท่อไหนเลยขอบซ้าย ก็ย้ายไปขวาสุด แล้วสุ่มช่องว่างใหม่ (resize)
# ส่วน core ที่เตรียมให้: game.Box() x6, box.resize() (bentogame.py:178,208)
# C step == Python step บนจอ: c_track/flappy_step3.c (flappy_reset_pipe :152)
# อ้างอิง: reference/flappy_full.py:20-28,43-52
import bentogame as game
import random

GRAVITY = 0.45                                  # แรงโน้มถ่วง
FLAP = -7.4                                     # แรงกระพือ
SPEED = 3.4                                     # ความเร็วท่อเลื่อนซ้าย (flappy_full.py:8)
GAP = 152                                       # ช่องว่างระหว่างท่อบน-ล่าง (ที่นกลอด)
PIPE_WIDTH = 64                                 # ความกว้างของท่อ
SPACING = 270                                   # ระยะห่างระหว่างท่อแต่ละท่อ

game.title("FLAPPY")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

bird = game.Box(150, 180, 34, 34, game.GB_LIGHTEST)
bird_y = 180.0
bird_velocity = 0.0
score = 0
score_label = game.Text("0", 384, 16, game.WHITE)

# ----- เติมส่วนนี้เอง: สร้างท่อครั้งเดียว แล้วหมุนเวียนใช้ -----
pipes = []
def add_pipe(start_x):
    gap_top = random.randint(60, game.HEIGHT - 60 - GAP)        # ขอบบนของช่องว่าง
    pipes.append({
        "x": float(start_x), "gap_top": gap_top,
        "top": game.Box(start_x, 0, PIPE_WIDTH, gap_top, game.GB_DARK),    # ท่อบน
        "bot": game.Box(start_x, gap_top + GAP, PIPE_WIDTH,
                        game.HEIGHT - gap_top - GAP, game.GB_DARK),         # ท่อล่าง
    })
for index in range(3):
    add_pipe(game.WIDTH + index * SPACING)      # วางท่อ 3 ท่อ เริ่มนอกจอด้านขวา

def on_each_frame():
    global bird_y, bird_velocity
    keys = game.keys()
    if keys.a or keys.up:
        bird_velocity = FLAP; game.sfx("flap")
    bird_velocity += GRAVITY
    bird_y += bird_velocity
    if bird_y < 0: bird_y, bird_velocity = 0, 0
    if bird_y > game.HEIGHT - bird.h:
        game.Text("GAME OVER", 320, 180, game.RED); return False
    bird.move_to(bird.x, bird_y)

    # ----- เติมส่วนนี้เอง: เลื่อนท่อ + หมุนเวียนใช้ซ้ำ -----
    for pipe in pipes:
        pipe["x"] -= SPEED                       # เลื่อนซ้าย
        if pipe["x"] < -PIPE_WIDTH:              # เลยขอบซ้าย ก็ย้ายไปขวาสุด
            pipe["x"] = max(other["x"] for other in pipes) + SPACING
            pipe["gap_top"] = random.randint(60, game.HEIGHT - 60 - GAP)
            pipe["top"].resize(PIPE_WIDTH, pipe["gap_top"])
            pipe["bot"].resize(PIPE_WIDTH, game.HEIGHT - pipe["gap_top"] - GAP)
        pipe["top"].move_to(pipe["x"], 0)
        pipe["bot"].move_to(pipe["x"], pipe["gap_top"] + GAP)

game.run(on_each_frame, fps=50)
