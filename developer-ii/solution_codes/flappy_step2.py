# flappy_step2.py — สร้าง Flappy #2: แรงโน้มถ่วง + กระพือปีก
# -----------------------------------------------------------------------------
# คาบนี้เราจะทำให้นกมีชีวิตขึ้นมา:
#   โลกในเกมมีแรงโน้มถ่วงดึงนกลงทุกเฟรม ถ้าเราไม่ทำอะไร นกก็จะค่อยๆ ร่วงลง
#   พอกด A (หรือ UP) นกจะกระพือปีกดีดตัวขึ้น หัวใจของเกม Flappy ทั้งเกม
#   อยู่ในไม่กี่บรรทัดนี้เอง พอทำเสร็จเราจะเห็นนกตกแล้วเด้งขึ้นตามนิ้วเรา
#
# ส่วนที่คุณจะเขียนเองคาบนี้ (ฟิสิกส์ของนก):
#     bird_velocity += GRAVITY           # โน้มถ่วงดึงลง ทุกเฟรม
#     ถ้ากด A/UP: bird_velocity = FLAP   # กระพือ = ดีดขึ้น (ความเร็วติดลบ)
#     bird_y += bird_velocity            # เลื่อนนกตามความเร็ว
#   + กันชนเพดานบน และ "ตกพื้น = จบเกม"
# ส่วนที่อาจารย์เตรียมไว้ให้แล้ว: game.keys() (อ่านปุ่ม), game.sfx("flap") (เสียง)
#   (bentogame.py:262,64)
# C step == Python step บนจอ: c_track/flappy_step2.c (page_game_flappy.c:307-318)
# อ้างอิง: reference/flappy_full.py:30-42
import bentogame as game

GRAVITY = 0.45                                  # แรงโน้มถ่วง (ดึงลงต่อเฟรม)
FLAP = -7.4                                     # แรงกระพือ (ดีดขึ้น) (flappy_full.py:8)

game.title("FLAPPY")                          # หน้าเริ่ม: Start=เล่น Back=ออก (ทำ start ให้ในตัว)

bird = game.Box(150, 180, 34, 34, game.GB_LIGHTEST)
bird_y = 180.0                                  # ความสูงของนก
bird_velocity = 0.0                             # ความเร็วแนวตั้งของนก (+ = ลง, - = ขึ้น)
score = 0
score_label = game.Text("0", 384, 16, game.WHITE)

def on_each_frame():
    global bird_y, bird_velocity
    # ----- เติมส่วนนี้เอง: ฟิสิกส์ของ flappy -----
    keys = game.keys()
    if keys.a or keys.up:
        bird_velocity = FLAP                    # กระพือ = ดีดขึ้น
        game.sfx("flap")
    bird_velocity += GRAVITY                     # โน้มถ่วงดึงลงทุกเฟรม
    bird_y += bird_velocity                      # เลื่อนนกตามความเร็ว
    if bird_y < 0:                               # ชนเพดานบน → หยุดความเร็ว
        bird_y, bird_velocity = 0, 0
    if bird_y > game.HEIGHT - bird.h:            # ตกพื้น → จบเกม
        game.Text("GAME OVER", 320, 180, game.RED)
        return False
    bird.move_to(bird.x, bird_y)

game.run(on_each_frame, fps=50)
