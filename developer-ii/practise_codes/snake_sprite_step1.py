# โครงเริ่มต้น — เฉลย: starter/snake_sprite_step1.py / ใบ้: ในใบงาน session
# (ขั้นนี้ยังไม่มีส่วนที่ต้องเติมเอง แค่รันดูผลงานวาด: เปลี่ยน Box เป็น Sprite จริง)
#
# snake_sprite_step1.py — คาบ 4 (ช่วง B): กล่อง เป็น sprite จริง (ภาพนิ่ง)
#
# ไฟล์นี้คือ snake_step1.py (วาดสนาม ตัวงู อาหารแบบภาพนิ่ง) แต่เราเปลี่ยนวิธีวาด
# จาก game.Box(...) เป็น game.Sprite("ชื่อรูป", x, y) เพื่อให้งูเป็น
# พิกเซลอาร์ตตัวเดียวกับเกม C (ขั้นนี้ยังไม่มี logic การเดิน เราแค่เปลี่ยนตัววาดก่อน)
#
# สองจุดที่ต่างจากเวอร์ชันกล่อง:
#   1) Box(...)  ->  Sprite("ชื่อรูป", x, y)   (หัว/ตัว/อาหาร เป็นรูปจริง)
#   2) CELL = 26 -> CELL = 16                  (ขนาดช่อง = SNAKE_CELL_PX ในเกม C)
#
# บนฮาร์ดแวร์จริง = รูปพิกเซลตรงกับเกม C
# บน sim บนคอม    = กล่องเขียว GB เล็ก ๆ (fallback) ตรรกะเหมือนกันทุกอย่าง
import bentogame as game

CELL = 16                        # ตรงกับเกม C เป๊ะ (SNAKE_CELL_PX = 16)
COLS = game.WIDTH // CELL         # หน้าจอกว้างกี่ช่อง
ROWS = game.HEIGHT // CELL        # หน้าจอสูงกี่ช่อง

game.start()                     # ล้างจอ + ปลุกจอย (เรียกครั้งเดียว)

# ตัวงู: หัวอยู่ช่องแรกของ list
body = [[6, 8], [5, 8], [4, 8]]

# กฎกัน 32 widget: เตรียมปล้องตัวงูไว้ล่วงหน้าเป็น pool ครั้งเดียว
# (ห้ามสร้าง Sprite ใหม่ในลูป — พอเกิน 32 จอจะหยุดวาดเงียบ ๆ)
POOL = 26
seg_pool = game.pool("snake_body", POOL)    # สร้างครั้งเดียว — คืน list ของปล้องที่ซ่อนไว้

# หัวงูแยกออกมา 1 ตัว (รูปหันขวา) — สร้างครั้งเดียว
head = game.Sprite("snake_head_r", 0, 0)

# อาหารเป็นรูป sprite จริง (เดิมเป็น Box)
food = game.Sprite("snake_food", 7 * CELL, 4 * CELL)

# คะแนน (ยังเป็นข้อความปกติ)
score = 0
score_text = game.Text("Score: 0", 10, 8, game.WHITE)


def draw():
    """วาดงูแบบภาพนิ่งจาก list `body` โดยใช้ head + pool (ไม่สร้าง sprite ใหม่)"""
    # หัวงู: ช่องแรกของ body
    head.move_to(body[0][0] * CELL, body[0][1] * CELL)
    # ปล้องตัว: body[1:] -> เอาจาก pool มาโชว์เท่าที่ใช้ ที่เหลือซ่อน
    for i in range(POOL):
        if i + 1 < len(body):
            seg_pool[i].show()
            seg_pool[i].move_to(body[i + 1][0] * CELL, body[i + 1][1] * CELL)
        else:
            seg_pool[i].hide()


draw()                           # วาดงูหนึ่งครั้งก่อนเริ่ม loop (ให้งูโผล่ทันที)


# ภาพยังนิ่ง — แต่ยังให้ "กด Start = ออก" เหมือนทุกเกม
def update():
    if game.keys().start:        # กด Start = ออกจากเกม
        return False


game.run(update, fps=9)
