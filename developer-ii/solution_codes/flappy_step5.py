# flappy_step5.py — Flappy #5: เข้าใกล้เกมจริงบนคอนโซล (โหมดความยาก + best)
# -----------------------------------------------------------------------------
# เรื่องราวของคาบนี้:
#   step4 เราเล่นจบไปแล้ว คาบนี้เราจะทำให้มันใกล้ "เกมในตู้จริง" มากขึ้น: มีเมนู
#   เลือกความยาก EASY/NORMAL/HARD, จำคะแนนดีที่สุด (best) ข้ามรอบ, และใช้ฟิสิกส์
#   แบบ delta-time (วัดเวลาจริงที่ผ่านไป ต่อให้เฟรมกระตุก ความเร็วนกก็ยังคงที่)
#
# หมายเหตุเรื่อง asymmetry (MASTER_PLAN 2.2:115 — flagged ไว้ให้อนุมัติตาม §0):
# Step-5 ของ Flappy ไม่มี Python twin แบบ 1:1 เพราะ reference/flappy_full.py
# จงใจหยุดที่ Step-4 (เกมเล่นจบ). ส่วนที่เป็นของแถมฝั่ง C console —
#   เมนูเลือกโหมด, LCD scanlines, เพลงพื้นหลัง, ปุ่มสัมผัส overlay —
# เป็น native CM55 (page_game_flappy.c:255,498,579,592) ที่ Python (วิ่งผ่าน IPC
# + เพดาน 32 sprite) ทำเลียนได้ไม่ครบ. ไฟล์นี้จึงหยิบเฉพาะส่วนที่ย้ายมา Python
# ได้จริงมาทำให้ครบ: (1) ฟิสิกส์แบบ delta-time (เฟรมไม่นิ่งก็ความเร็วคงที่) และ
# (2) ตารางโหมด EASY/NORMAL/HARD (ปรับ gap/speed/grav) แบบเดียวกับ s_flap_modes[]
# (page_game_flappy.c:59-63). chrome ฝั่ง C เราบันทึกไว้เป็น teaching point ไม่ทำเงียบ.
#
# ส่วนที่คุณเติมเองคาบนี้:
#   - delta-time: dt = เวลาจริงที่ผ่านไป → v += g*dt ; y += v*dt (หน่วยเป็น "ต่อวินาที")
#   - เลือกโหมดด้วย UP/DOWN ก่อนเริ่ม แล้วดึง gap/speed/grav/flap จากโหมดนั้น
#   - best score คงค่าข้ามรอบเล่น
# ส่วน core ที่เราเรียกใช้: เหมือนเดิม (start/Box/Text/keys/hit/sfx/run)
# C step ตรงกับ Python step บนจอ: c_track/flappy_step5.c == page_game_flappy.c (ของจริง)
import bentogame as game
import random, time

GAP, PIPE_WIDTH, SPACING = 152, 64, 270

# ตารางโหมด: (ชื่อ, gap, speed px/s, grav px/s^2, flap px/s)  — มิเรอร์ s_flap_modes[]
# page_game_flappy.c:59-63 (ค่าปรับให้เข้ากับสเกล Python ของ step1-4)
MODES = [
    ("EASY",   175, 200.0,  900.0, -360.0),
    ("NORMAL", 152, 240.0, 1100.0, -390.0),
    ("HARD",   120, 300.0, 1300.0, -410.0),
]

game.title("FLAPPY")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)
best_score = 0

def play_round(mode_index):
    """เล่นหนึ่งรอบด้วยโหมดที่เลือก. คืน score เมื่อจบ."""
    global best_score
    mode_name, gap, speed, gravity, flap = MODES[mode_index]

    game.clear()                                  # ล้างจอเมนูก่อนเริ่มรอบ (กันทะลุเพดาน 32 sprite)
    bird = game.Box(150, 180, 34, 34, game.GB_LIGHTEST)
    bird_y, bird_velocity, score = 198.0, 0.0, 0
    hud_label = game.Text("0  Best: %d  [%s]" % (best_score, mode_name), 300, 16, game.WHITE)

    pipes = []
    def add_pipe(start_x):
        gap_top = random.randint(60, game.HEIGHT - 60 - gap)
        pipes.append({"x": float(start_x), "gap_top": gap_top, "scored": False,
                      "top": game.Box(start_x, 0, PIPE_WIDTH, gap_top, game.GB_DARK),
                      "bot": game.Box(start_x, gap_top + gap, PIPE_WIDTH,
                                      game.HEIGHT - gap_top - gap, game.GB_DARK)})
    for index in range(3):
        add_pipe(game.WIDTH + index * SPACING)

    last_time = time.ticks_ms()
    bird_state = {"y": bird_y, "velocity": bird_velocity, "score": score, "over": False}

    def on_each_frame():
        global best_score                        # อัปเดต best (ตัวแปรระดับ module) ในนี้ด้วย
        # ----- เติมส่วนนี้เอง: ฟิสิกส์แบบ delta-time -----
        now = time.ticks_ms()
        dt = time.ticks_diff(now, last_clock[0]) / 1000.0   # เวลาจริงที่ผ่านไป (วินาที)
        last_clock[0] = now
        if dt > 0.05: dt = 0.05                   # กันเฟรมค้างยาวทะลุท่อ
        keys = game.keys()
        if keys.a or keys.up:
            bird_state["velocity"] = flap; game.sfx("flap")
        bird_state["velocity"] += gravity * dt    # โน้มถ่วงต่อวินาที
        bird_state["y"] += bird_state["velocity"] * dt
        if bird_state["y"] < 0:
            bird_state["y"], bird_state["velocity"] = 0, 0
        if bird_state["y"] > game.HEIGHT - bird.h:
            game.sfx("fall"); return False
        bird.move_to(bird.x, bird_state["y"])

        for pipe in pipes:
            pipe["x"] -= speed * dt
            if pipe["x"] < -PIPE_WIDTH:
                pipe["x"] = max(other["x"] for other in pipes) + SPACING
                pipe["gap_top"] = random.randint(60, game.HEIGHT - 60 - gap)
                pipe["scored"] = False
                pipe["top"].resize(PIPE_WIDTH, pipe["gap_top"])
                pipe["bot"].resize(PIPE_WIDTH, game.HEIGHT - pipe["gap_top"] - gap)
            pipe["top"].move_to(pipe["x"], 0)
            pipe["bot"].move_to(pipe["x"], pipe["gap_top"] + gap)
            if game.hit(bird, pipe["top"]) or game.hit(bird, pipe["bot"]):
                game.sfx("fall"); return False
            if not pipe["scored"] and pipe["x"] + PIPE_WIDTH < bird.x:
                pipe["scored"] = True
                bird_state["score"] += 1
                game.sfx("point")
                if bird_state["score"] > best_score: best_score = bird_state["score"]
                hud_label.set("%d  Best: %d  [%s]" % (bird_state["score"], best_score, mode_name))

    last_clock = [last_time]                       # ห่อใน list เพื่อให้ closure แก้ค่าได้
    game.run(on_each_frame, fps=60)
    if bird_state["score"] > best_score:
        best_score = bird_state["score"]
    game.Text("GAME OVER  -  score %d" % bird_state["score"], 290, 180, game.RED)
    return bird_state["score"]

# ----- เติมส่วนนี้เอง: หน้าจอเลือกโหมด (เลียน s_flap_modes UP/DOWN+A) -----
def choose_mode():
    game.clear()                                  # ล้างจอ GAME OVER ของรอบก่อน
    selected = 1                                   # ค่าเริ่มต้น = NORMAL
    mode_label = game.Text("", 280, 150, game.GB_LIGHTEST)
    hint_label = game.Text("UP/DOWN เลือกโหมด, A = เริ่ม", 250, 200, game.WHITE)
    def draw_choice():
        mode_label.set("MODE:  < %s >" % MODES[selected][0])
    draw_choice()
    while True:
        keys = game.keys()
        if keys.up:   selected = (selected - 1) % len(MODES); draw_choice(); time.sleep_ms(180)
        if keys.down: selected = (selected + 1) % len(MODES); draw_choice(); time.sleep_ms(180)
        if keys.a:    return selected
        time.sleep_ms(30)

# วนเหมือนคอนโซลจริง (C step5): เลือกโหมด → เล่น → ตาย → กลับไปเมนูเลือกโหมดใหม่
while True:
    chosen_mode = choose_mode()
    play_round(chosen_mode)
    time.sleep_ms(700)                            # ค้างจอ GAME OVER ก่อนกลับเมนู
