# โครงเว้นบางส่วน — เติมช่องที่เป็นงานของคุณให้ครบ แล้วเกมจะเล่นได้จริง
# เฉลย: starter/flappy_step5.py / ใบ้: ในใบงาน session
# -----------------------------------------------------------------------------
# เรื่องราวของคาบนี้:
#   step4 เราเล่นจบไปแล้ว คาบนี้เราจะทำให้มันใกล้เคียงเกมในตู้จริง: มีเมนูเลือก
#   ความยาก EASY/NORMAL/HARD, จำคะแนนดีที่สุด (best) ข้ามรอบ, และใช้ฟิสิกส์แบบ
#   delta-time (วัดเวลาจริงที่ผ่านไป ต่อให้เฟรมกระตุก ความเร็วนกก็ยังคงที่)
#
# ส่วนที่เป็นงานของคุณในคาบนี้:
#   - delta-time: dt = เวลาจริงที่ผ่านไป แล้ว v += g*dt ; y += v*dt (หน่วยเป็น "ต่อวินาที")
#   - เลือกโหมดด้วย UP/DOWN ก่อนเริ่ม แล้วดึง gap/speed/grav/flap จากโหมดนั้น
#   - best score คงค่าข้ามรอบเล่น
# ส่วน core ที่เรียกใช้: เหมือนเดิม (start/Box/Text/keys/hit/sfx/run)
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

game.start()
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
        # ----- เติมส่วนนี้เอง (งานของคุณ): ฟิสิกส์ delta-time + ชน + นับคะแนน -----
        # ลองทำทีละขั้นนะ ชื่อเครื่องมือบอกไว้ให้แล้ว ส่วนตัวเลข/สูตรลองปรับเอง ถ้าติดเปิด starter ดูได้:
        #   1) วัด dt (วินาที): ใช้ time.ticks_ms() + time.ticks_diff() เทียบกับเวลาเฟรมก่อน
        #      (เก็บไว้ใน last_clock[0]) แล้วหารพันให้เป็นวินาที เผื่อ clamp ค่าสูงสุดกันเฟรมค้าง
        #   2) อ่านปุ่ม: game.keys() ถ้ากดกระโดด (.a หรือ .up) ตั้ง velocity = flap แล้ว game.sfx("flap")
        #   3) ฟิสิกส์: เพิ่ม velocity ด้วย gravity*dt, เพิ่ม y ด้วย velocity*dt, กันทะลุเพดาน/พื้น
        #      ตกพื้น (y เกิน game.HEIGHT - bird.h) ให้ game.sfx("die") แล้ว return False ; วาดนกด้วย bird.move_to(...)
        #   4) วน pipes แต่ละท่อ: เลื่อน x ด้วย speed*dt, ท่อที่หลุดซ้ายให้รีไซเคิลไปขวาสุด (ปรับ gap_top
        #      + .resize() ใหม่), ขยับท่อด้วย .move_to(); ถ้า game.hit(bird, ท่อ) ให้ตาย; ถ้านกผ่านท่อ (ยัง
        #      ไม่ scored) ให้ score+=1, game.sfx("point"), อัปเดต best_score แล้ว hud_label.set(...)
        pass   # <- ลบ pass ออกเมื่อเริ่มเขียน (คงไว้ตอนนี้เพื่อให้รันได้)

    last_clock = [last_time]                       # ห่อใน list เพื่อให้ closure แก้ค่าได้
    game.run(on_each_frame, fps=60)
    if bird_state["score"] > best_score:
        best_score = bird_state["score"]
    game.Text("GAME OVER  -  score %d" % bird_state["score"], 290, 180, game.RED)
    return bird_state["score"]

def choose_mode():
    game.clear()                                  # ล้างจอ GAME OVER ของรอบก่อน
    selected = 1                                   # ค่าเริ่มต้น = NORMAL
    mode_label = game.Text("", 280, 150, game.GB_LIGHTEST)
    hint_label = game.Text("UP/DOWN เลือกโหมด, A = เริ่ม", 250, 200, game.WHITE)
    def draw_choice():
        mode_label.set("MODE:  < %s >" % MODES[selected][0])
    draw_choice()
    while True:
        # ----- เติมส่วนนี้เอง (งานของคุณ): หน้าจอเลือกโหมด (รับ UP/DOWN + A) -----
        # อ่านปุ่มด้วย game.keys() ในลูป แล้ว:
        #   1) ปุ่มขึ้น (.up)   เลื่อน selected ไปโหมดก่อนหน้า (วนรอบด้วย % len(MODES)) แล้วเรียก draw_choice()
        #   2) ปุ่มลง (.down)  เลื่อน selected ไปโหมดถัดไป (วนรอบเช่นกัน) แล้วเรียก draw_choice()
        #   3) ปุ่มยืนยัน (.a)  return selected (ออกจากลูปเริ่มเล่นโหมดที่เลือก)
        # เคล็ด: หลังเลื่อนให้หน่วงสั้น ๆ (time.sleep_ms) กันปุ่มเด้งรัว ลองหาเวลาที่พอดีเอง
        return selected   # <- ตอนนี้คืนค่าเริ่มต้นไปก่อน เพื่อให้รันได้; แก้เป็นลูปจริงเมื่อเริ่มเขียน

# วนเหมือนคอนโซลจริง (C step5): เลือกโหมด แล้วเล่น พอตายก็กลับไปเมนูเลือกโหมดใหม่
while True:
    chosen_mode = choose_mode()
    play_round(chosen_mode)
    time.sleep_ms(700)                            # ค้างจอ GAME OVER ก่อนกลับเมนู
