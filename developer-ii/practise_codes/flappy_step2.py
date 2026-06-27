# โครงเว้น 30% — ช่องที่คุณต้องเติมเอง  /  เฉลย: starter/flappy_step2.py  /  ใบ้: ในใบงาน session
# flappy_step2.py — สร้าง Flappy #2: แรงโน้มถ่วง + กระพือปีก
# -----------------------------------------------------------------------------
# เรื่องราวของคาบนี้:
#   คาบนี้เราจะทำให้นกมีชีวิตขึ้นมา โลกของเรามีแรงโน้มถ่วงดึงนกลงทุกเฟรม
#   ถ้าเราไม่ทำอะไรเลย นกก็จะค่อยๆ ร่วงลงไป
#   กด A (หรือ UP) คือกระพือปีก ดีดนกขึ้น หัวใจของเกม Flappy ทั้งเกม
#   อยู่ในแค่ไม่กี่บรรทัดนี้เอง พอเขียนเสร็จ นกจะตกแล้วเด้งขึ้นตามนิ้วเรา
#
# ส่วนที่คุณเขียนเองคาบนี้ (ฟิสิกส์ของนก):
#   - ทุกเฟรม โน้มถ่วงต้องเพิ่มความเร็วลง แล้วเอาความเร็วไปขยับตำแหน่งนก
#   - กด A/UP = กระพือ = ตั้งความเร็วให้ดีดขึ้น (ใช้ค่าคงที่ FLAP)
#   - กันชนเพดานบน และ "ตกพื้น = จบเกม"
# ส่วน core ที่เตรียมไว้ให้: game.keys() (อ่านปุ่ม), game.sfx() (เสียง)
#   (bentogame.py: keys:262, sfx:64)
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
    # ----- เติมส่วนนี้เอง (งานของคุณ): ฟิสิกส์ของนก (กระพือ + โน้มถ่วง + ตกพื้นจบเกม) -----
    # TODO 1) อ่านปุ่มด้วย game.keys() เก็บไว้ในตัวแปร แล้วเช็คว่ากด a หรือ up ไหม
    #         (keys มี attribute .a, .up — ดู bentogame.py:262)
    # TODO 2) ถ้ากด: ตั้ง bird_velocity ให้เท่ากับค่าคงที่ FLAP (ดีดขึ้น = ความเร็วติดลบ)
    #         แล้วเล่นเสียงด้วย game.sfx() โดยส่งชื่อเสียง "flap" เข้าไป
    # TODO 3) ทุกเฟรม (นอก if กด): บวก GRAVITY เข้า bird_velocity เพื่อให้โน้มถ่วงดึงลง
    #         แล้วบวก bird_velocity เข้า bird_y เพื่อเลื่อนนกตามความเร็ว
    # TODO 4) กันชนเพดาน: ถ้า bird_y น้อยกว่า 0 ให้รีเซ็ต bird_y และ bird_velocity เป็น 0
    # TODO 5) ตกพื้นจบเกม: ถ้า bird_y มากกว่า game.HEIGHT - bird.h
    #         ให้แสดงข้อความ GAME OVER ด้วย game.Text(...) แล้ว return False
    pass   # <- ลบ pass ออกเมื่อเริ่มเขียน (เป็น placeholder ให้รันได้เฉยๆ)
    bird.move_to(bird.x, bird_y)

game.run(on_each_frame, fps=50)
