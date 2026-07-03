# flappy_full.py — Flappy Bird ฉบับอ้างอิง หน้าตาและจังหวะตามเกม C บนเครื่อง
# (page_game_flappy.c): นกเงือก sprite ตัวจริง, ท่อเขียวมีปากท่อ, ท้องฟ้าไล่สี,
# เลือกความยาก EASY/NORMAL/HARD, คะแนน+Best, ตายแล้วกด Start เล่นใหม่ได้ทันที
# หรือกด Y ระหว่างเล่นเพื่อเริ่มตาใหม่โหมดเดิมทันที (ปุ่มเดียวกับเกม C)
#
# สองเทคนิคสำคัญที่อยากให้อ่านช้าๆ:
# - pressed_once(): กด 1 ครั้ง = กระพือ 1 ครั้ง กดค้างแล้วลอยไม่ได้
#   (เกม C ก็เข้มแบบนี้ — ความยากของ Flappy อยู่ตรงจังหวะกดนี่แหละ)
# - delta-time (dt): ความเร็วทุกตัวคิดเป็น "ต่อวินาที" แล้วคูณเวลาที่ผ่านจริง
#   ของแต่ละเฟรม เฟรมจะช้าจะเร็วเกมก็ไหลเท่าเดิม ไม่กระตุก (เกม C ทำแบบเดียวกัน)

import bentogame as game
import random
import time

# ---- ค่าคงที่ ยกชุดมาจากเกม C (หน่วย px, px/s, px/s^2) ----
BIRD_X = 120             # ตำแหน่งแกน x ของนก (นกอยู่กับที่ ฉากเลื่อนเข้าหาแทน)
BIRD_W, BIRD_H = 44, 29  # ขนาด sprite นกเงือกตัวจริง
BIRD_BOX = 36            # กล่องชนสี่เหลี่ยม (เกม C ใช้ 36 — ใจดีกว่าขนาด sprite นิดหน่อย)
PIPE_SPACING = 210       # ระยะห่างระหว่างท่อ
CAP_W, CAP_H = 82, 18    # ปากท่อ: กว้างเกินตัวท่อ สไตล์ท่อมาริโอ
PIPE_W = 64              # ความกว้างท่อ (คงที่ — ท่อเป็นกล่องสูงเต็มจอ ไม่ resize เลย)
GROUND_H = 20            # แถบพื้นหญ้าด้านล่าง = เส้นตาย

# ความยาก 3 ระดับ ตัวเลขชุดเดียวกับ s_flap_modes ของเกม C:
# (ชื่อ, ช่องว่างท่อ px, ความเร็วท่อ px/s, แรงโน้มถ่วง px/s^2, แรงกระพือ px/s)
MODES = (
    ("EASY",   175, 110.0,  850.0, -300.0),   # ช่องกว้าง ช้า เบา
    ("NORMAL", 130, 150.0, 1050.0, -340.0),   # จูนมาตรฐานของเกม C
    ("HARD",   105, 200.0, 1200.0, -360.0),   # ช่องแคบ เร็ว หนัก
)
PIPE_TINTS = (0x6CD84C, 0x4CB838, 0x84E060)   # เขียว 3 เฉด สุ่มให้ท่อแต่ละต้นไม่ซ้ำกัน
CAP_COLOR = 0x7CE85C                          # ปากท่อสว่างกว่าตัวท่อหน่อย ให้ดูนูน
# ฟ้าไล่ 8 ระดับ เข้มบน->จางล่าง (ยิ่งซอยถี่ยิ่งเนียนเข้าใกล้ gradient ของเกม C)
SKY_BANDS = (0x4898F0, 0x58A2F1, 0x68ADF2, 0x78B7F3,
             0x88C1F5, 0x98CBF6, 0xA8D6F7, 0xB8E0F8)

game.title("FLAPPY", melody=True)

mode = 1                 # เปิดมาชี้ NORMAL ก่อน เหมือนเกม C
dead_msg = None          # สาเหตุที่ตายตาก่อน — โชว์บนหัวเมนูแบบเกม C
restart_same = False     # ปุ่ม Y = เริ่มตาใหม่โหมดเดิมทันที ไม่ต้องผ่านเมนู
while True:      # ตายแล้ววนกลับมาเลือกโหมดใหม่ได้เลย ไม่ต้องรีบูตเครื่อง

    # ล้างฉากของรอบก่อนทิ้งก่อนสร้างใหม่ — flappy สร้าง ~20 widget/รอบ (ฟ้า+ท่อ+นก)
    # ถ้าไม่ล้าง widget จะสะสมข้ามรอบจนทะลุงบ 32 ชิ้น แล้ว CM55 จะ "not ready"
    game.clear()

    # ---- จัดฉากก่อน แล้วค่อยขึ้นเมนู: วาดฉาก+นกให้เสร็จก่อน จากนั้นเมนูลอยทับ
    #  ให้เลือกโหมด — ระหว่างที่ผู้เล่นเลือก ฉากมีเวลาวาดจนครบ พอกดเล่นจึงเห็น
    #  ทุกอย่างทันทีและบังคับนกได้เลย ไม่มีช่วงจอโล่ง/นกตกก่อนฉากขึ้น ----

    # ---- จัดฉาก (สร้างครั้งเดียว ไม่มีงานต่อเฟรม) ----
    # เกม C ใช้ gradient จริงบนจอ ฝั่ง Python ปูแถบสี 8 แถบแทน ได้อารมณ์เดียวกัน
    PLAY_H = game.HEIGHT - GROUND_H           # ความสูงสนามเล่นจริง (เหนือพื้นหญ้า)
    band_h = PLAY_H // len(SKY_BANDS)
    for i, sky in enumerate(SKY_BANDS):
        h = band_h if i < len(SKY_BANDS) - 1 else PLAY_H - band_h * i
        game.Box(0, i * band_h, game.WIDTH, h, sky)
    game.grass(GROUND_H)

    # ท่อ 3 ต้น หมุนเวียนใช้ซ้ำ (widget มีได้ 32 ชิ้น — สร้างใหม่ทุกต้นไม่ไหว)
    # ต้นละ 4 ชิ้น: ตัวท่อบน/ล่าง + ปากท่อบน/ล่าง สร้างแบบซ่อนไว้ก่อน
    pipes = []
    for _ in range(3):
        # ท่อบน/ล่างเป็นกล่อง "สูงเต็มสนาม" (PIPE_W x PLAY_H) สร้างครั้งเดียว ไม่ resize อีกเลย
        # ช่องว่างเกิดจากการเลื่อนตำแหน่ง y (ท่อบนโผล่จากขอบบน ท่อล่างโผล่จากขอบล่าง)
        parts = {"top": game.Box(-200, 0, PIPE_W, PLAY_H, game.GB_DARK),
                 "bot": game.Box(-200, 0, PIPE_W, PLAY_H, game.GB_DARK),
                 "cap_t": game.Box(-200, 0, CAP_W, CAP_H, CAP_COLOR),
                 "cap_b": game.Box(-200, 0, CAP_W, CAP_H, CAP_COLOR)}
        for box in parts.values():
            box.hide()
        parts.update({"x": 0.0, "w": PIPE_W, "gap": 130, "gy": 189, "passed": False,
                      "gap_top": 0, "gap_bot": PLAY_H,
                      "vis": {"top": False, "bot": False,
                              "cap_t": False, "cap_b": False}})
        pipes.append(parts)

    # นกเงือก = sprite pixel-art ตัวเดียวกับเกม C (ปีกวาดมาในรูปแล้ว เกม C ก็ใช้ภาพนิ่ง)
    bird = game.Sprite("bird", BIRD_X - BIRD_W // 2, PLAY_H // 2 - BIRD_H // 2)
    hud = game.Text("Score: 0    Best: %d" % game.best("flappy"), 16, 8, game.WHITE)
    status = game.Text("", 16, 34, game.WHITE)

    # ---- ฉากวาดครบแล้ว → ขึ้นเมนูเลือกโหมด (เมนูเก็บกวาดป้ายของตัวเองตอนจบ ฉากไม่โดนแตะ)
    #  หัวเมนูบอกด้วยว่าตาก่อนจบเพราะอะไร; ตาที่กด Y มา ข้ามเมนูไปเริ่มโหมดเดิมเลย ----
    if not restart_same:
        picked = game.menu("EASY", "NORMAL", "HARD", selected=mode,
                           heading=dead_msg or "SELECT MODE")
        if picked is None:               # BACK จากหน้าเมนู = เลิกเล่น
            break
        mode = picked
    restart_same = False
    MODE_NAME, GAP, PIPE_SPEED, GRAVITY, FLAP_VEL = MODES[mode]
    status.set("%s  -  A/UP = flap  (กระพือเพื่อออกตัว)" % MODE_NAME)

    def reset_pipe(pipe, first_x=None):
        # เกิดใหม่ทางขวา: สุ่มช่องว่าง ตำแหน่งช่อง เฉดสี — "ไม่ resize" (ท่อสูงเต็มจอคงที่)
        if first_x is not None:
            pipe["x"] = float(first_x)
        else:
            pipe["x"] = max(p["x"] for p in pipes) + PIPE_SPACING
        pipe["gap"] = GAP + random.randint(-12, 12)
        half = pipe["gap"] // 2
        pipe["gy"] = random.randint(half + 24, PLAY_H - half - 24)
        pipe["passed"] = False
        pipe["gap_top"] = max(pipe["gy"] - half, 20)
        pipe["gap_bot"] = min(pipe["gy"] + half, PLAY_H - 20)
        tint = PIPE_TINTS[random.randint(0, 2)]
        pipe["top"].set_color(tint)
        pipe["bot"].set_color(tint)

    def render_pipe(pipe):
        # ต่อเฟรม: "เลื่อนอย่างเดียว" ไม่ resize — ท่อสูงเต็มจอ ส่วนพ้นขอบให้ฮาร์ดแวร์ตัด
        x = int(pipe["x"])
        on = -pipe["w"] < x < game.WIDTH
        for key in ("top", "bot", "cap_t", "cap_b"):
            if on and not pipe["vis"][key]:
                pipe[key].show(); pipe["vis"][key] = True
            elif not on and pipe["vis"][key]:
                pipe[key].hide(); pipe["vis"][key] = False
        if not on:
            return
        pipe["top"].move_to(x, pipe["gap_top"] - PLAY_H)   # ขอบล่างของท่อบน = ขอบช่องบน
        pipe["bot"].move_to(x, pipe["gap_bot"])            # ขอบบนของท่อล่าง = ขอบช่องล่าง
        cap_x = x + pipe["w"] // 2 - CAP_W // 2
        pipe["cap_t"].move_to(cap_x, pipe["gap_top"] - CAP_H)
        pipe["cap_b"].move_to(cap_x, pipe["gap_bot"])

    def hit_pipe(pipe):
        # กล่องชน 36px รอบใจกลางนก เทียบกับท่อบน/ล่าง (สูตรเดียวกับ flappy_hit_pipe)
        half_bird = BIRD_BOX // 2
        if (BIRD_X + half_bird < pipe["x"] or
                BIRD_X - half_bird > pipe["x"] + pipe["w"]):
            return False                       # ยังไม่ถึงแนวท่อ ไม่ต้องเช็กต่อ
        half = pipe["gap"] // 2
        return (bird_y - half_bird < pipe["gy"] - half or
                bird_y + half_bird > pipe["gy"] + half)

    # ---- ตั้งค่าเริ่มรอบ ----
    for i, pipe in enumerate(pipes):
        reset_pipe(pipe, first_x=game.WIDTH + i * PIPE_SPACING)
        render_pipe(pipe)

    bird_y, velocity_y = float(PLAY_H // 2), 0.0
    score, best_seen = 0, game.best("flappy")
    scroll_acc = 0.0                # เศษ pixel สะสมของการเลื่อนท่อ
    dead_msg = "GAME OVER"
    restart_now = False             # ตั้งเป็นจริงเมื่อผู้เล่นกด Y
    started = False                 # ยังไม่เริ่มบิน — นกลอยรอจนกระพือครั้งแรก
    start_ms = 0                    # เวลาที่ออกตัว — ใช้คุมช่วง grace 4 วิแรก (นกตายไม่ได้)
    last_ms = time.ticks_ms()

    def update():
        global bird_y, velocity_y, score, best_seen, scroll_acc, dead_msg, last_ms
        global restart_now, started, start_ms

        # delta-time: วัดเวลาที่ผ่านจริงตั้งแต่เฟรมก่อน แล้วใช้คูณความเร็วทุกตัว
        now = time.ticks_ms()
        dt = time.ticks_diff(now, last_ms) / 1000.0
        last_ms = now
        if dt > 0.05:
            dt = 0.05      # เพิ่งกลับจาก pause หรือเฟรมค้างนาน: กันนกวาร์ปทะลุท่อ
        if dt <= 0:
            return

        # กระพือปีก: จับเฉพาะจังหวะกด (อ่านทั้งสองปุ่มก่อน ค่อย or —
        # ให้ pressed_once เห็นทุกปุ่มทุกเฟรม จะได้จำสถานะถูก)
        k = game.keys()
        if game.pressed_once("y", k):      # Y = เริ่มตาใหม่โหมดเดิมทันที (แบบเกม C)
            restart_now = True
            return False
        flap_a = game.pressed_once("a", k)
        flap_up = game.pressed_once("up", k)
        if flap_a or flap_up:
            velocity_y = FLAP_VEL
            game.sfx("flap")
            status.set("Flap!")

        if not started:                    # ยังไม่ออกตัว: นกลอยรอกลางจอ ไม่มีแรงโน้มถ่วง
            if not (flap_a or flap_up):     # จนกว่าจะกระพือครั้งแรก — ท่อยังไม่เลื่อน นกไม่ตก
                return                       # ให้ผู้เล่นพร้อม (ฉากวาดครบตั้งแต่หน้าเมนูแล้ว)
            started = True                    # กระพือครั้งแรก = ออกบิน
            start_ms = now                     # เริ่มจับเวลา grace 4 วิ

        grace = time.ticks_diff(now, start_ms) < 4000   # 4 วิแรก: นกตายไม่ได้ (ครอบช่วงจอกำลังวาด)

        velocity_y += GRAVITY * dt
        bird_y += velocity_y * dt

        if bird_y < BIRD_BOX / 2:              # ชนเพดาน: หยุดค้างไว้ ไม่ตาย
            bird_y, velocity_y = BIRD_BOX / 2, 0.0
        if bird_y > PLAY_H - BIRD_BOX / 2:     # ร่วงถึงพื้น
            if grace:                          # ช่วง grace: ไม่ตาย แค่หยุดที่พื้น
                bird_y, velocity_y = PLAY_H - BIRD_BOX / 2, 0.0
            else:
                game.sfx("fall")
                dead_msg = "GROUND!"
                return False
        bird.move_to(BIRD_X - BIRD_W // 2, int(bird_y) - BIRD_H // 2)

        # ท่อเลื่อนซ้าย: ตำแหน่งบนจอเป็นจำนวนเต็ม แต่ระยะต่อเฟรมเป็นทศนิยม
        # เลยสะสมเศษไว้ก่อน ครบ 1 pixel ค่อยขยับ (เฟรมช้าๆ จะได้ไม่ทิ้งเศษระยะ)
        scroll_acc += PIPE_SPEED * dt
        step = int(scroll_acc)
        scroll_acc -= step

        for pipe in pipes:
            pipe["x"] -= step
            if not pipe["passed"] and pipe["x"] + pipe["w"] < BIRD_X:
                pipe["passed"] = True          # นกพ้นท่อทั้งต้น = ได้ 1 คะแนน
                score += 1
                game.sfx("point")
                if score > best_seen:
                    best_seen = score          # Best ขยับตามทันทีเหมือนเกม C
                hud.set("Score: %d    Best: %d" % (score, best_seen))
            if pipe["x"] + pipe["w"] < 0:      # หลุดจอซ้าย: วนกลับไปเกิดใหม่ทางขวา
                reset_pipe(pipe)
            render_pipe(pipe)
            if hit_pipe(pipe) and not grace:   # ช่วง grace 4 วิแรก: ชนท่อไม่ตาย
                game.sfx("fall")
                dead_msg = "PIPE!"
                return False

    if not game.run(update, fps=50):           # Back กลางเกม = เลิกเล่น
        game.save_best(score, "flappy")        # คะแนนดีๆ ไม่หายไปกับตาที่ออกกลางคัน
        break
    if restart_now:                            # Y = วนไปเริ่มโหมดเดิมใหม่ทันที
        game.save_best(score, "flappy")
        game.replay()
        restart_same = True
        continue
    if not game.game_over(score, name="flappy", msg=dead_msg):
        break                                  # Start = เล่นรอบใหม่ / Back = ออก
