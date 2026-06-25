# โครงเว้นบางส่วน — เติมช่องที่เป็นงานของคุณให้ครบ แล้วเกมจะเล่นได้จริง
# เฉลย: starter/flappy_step3.py / ใบ้: ในใบงาน session
# -----------------------------------------------------------------------------
# เรื่องราวของคาบนี้:
#   ฟ้าโล่งๆ ยังไม่ค่อยท้าทายเท่าไหร่ คาบนี้เราเพิ่ม "ท่อ" ที่เลื่อนเข้ามาจากขวาไปซ้าย
#   เคล็ดลับที่เกมจริงใช้กัน: เราสร้างท่อแค่ 3 ท่อ "ครั้งเดียว" แล้ว "หมุนเวียนใช้ซ้ำ"
#   (ท่อไหนหลุดขอบซ้าย ก็ส่งกลับไปขวาสุด แล้วสุ่มช่องว่างใหม่) ไม่ต้องสร้างท่อใหม่
#   ไปเรื่อยๆ ไม่รู้จบ ประหยัดหน่วยความจำและลื่นกว่า นี่คือ pattern "create once, recycle"
#
# ส่วนที่เป็นงานของคุณในคาบนี้ (จัดการท่อ):
#     - ทุกเฟรม: เลื่อนท่อไปทางซ้าย SPEED
#     - ท่อไหนเลยขอบซ้าย ให้ย้ายไปขวาสุดแล้วสุ่มช่องว่างใหม่ (resize)
# ส่วน core ที่ให้ไว้แล้ว: game.Box() x6, box.resize() (bentogame.py:178,208)
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

game.start()

bird = game.Box(150, 180, 34, 34, game.GB_LIGHTEST)
bird_y = 180.0
bird_velocity = 0.0
score = 0
score_label = game.Text("0", 384, 16, game.WHITE)

# --- สร้างท่อครั้งเดียว แล้วหมุนเวียนใช้ (โครงนี้ให้ไว้แล้ว) ------------------
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

    # ----- เติมส่วนนี้เอง (งานของคุณ): เลื่อนท่อทุกเฟรม + หมุนเวียนใช้ซ้ำ -----
    # ลองทำตาม 5 ขั้นนี้ (วน for pipe in pipes:):
    #   1) เลื่อนท่อไปทางซ้าย ลดค่า pipe["x"] ลงทีละ SPEED
    #   2) เช็คว่าท่อหลุดขอบซ้ายหรือยัง (เทียบ pipe["x"] กับ -PIPE_WIDTH)
    #   3) ถ้าหลุด ก็ย้าย pipe["x"] ไปไว้ขวาสุด (หาท่อที่ x มากสุดใน pipes
    #      แล้วเว้นต่อจากนั้นอีก SPACING ลองคิดดูก่อนนะ ถ้าติดค่อยดู starter)
    #   4) ถ้าหลุด ให้สุ่ม pipe["gap_top"] ใหม่ (random.randint ช่วงเดียวกับ
    #      add_pipe) แล้วปรับขนาดท่อด้วย .resize() ทั้งท่อบนและท่อล่าง
    #   5) ทุกเฟรม วาดท่อตามตำแหน่งใหม่ด้วย .move_to() ทั้ง pipe["top"]
    #      และ pipe["bot"] (bentogame.py: Box:178, move_to:188, resize:208)
    pass   # ลบ pass ออกเมื่อเริ่มเขียน

game.run(on_each_frame, fps=50)
