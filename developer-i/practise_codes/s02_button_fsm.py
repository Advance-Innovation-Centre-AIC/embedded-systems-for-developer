# s02_button_fsm.py — ปุ่ม + debounce + FSM (ไฟจราจร)  [ฉบับฝึก เติมช่องว่าง]
#
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกด "Program to Device"
#
# เป้าหมายของแล็บนี้: ฝึกแกนของ game loop จริง ๆ คือ
#   อ่าน input (ปุ่ม) -> กรองสัญญาณรบกวน (debounce) -> เปลี่ยน state (FSM) -> แสดงผล (LED)
# กดปุ่ม SW1 หนึ่งครั้ง = เปลี่ยนสถานะไฟจราจรไปทีละขั้น: เขียว -> เหลือง -> แดง -> วนกลับ
#
# มีช่องว่าง 4 จุด มองหาคำว่า "เติม:" แล้วเขียนโค้ดตามคำใบ้

import gpio
import time

# ขอใช้ปุ่มดวงแรก (index 0 = SW1 บนบอร์ด) และไฟ LED 2 ดวงไว้บอกสถานะ
# ใช้ LED2 (เขียว) + RGB_RED — เลี่ยง LED1 (แดง, index 0) ที่ระบบหลักใช้
btn = gpio.button(0)
led_a = gpio.led(1)   # LED2 (เขียว)
led_b = gpio.led(2)   # RGB_RED

# นิยาม state ของ FSM ให้อ่านง่าย แทนที่จะใช้ตัวเลขลอย ๆ
GREEN, YELLOW, RED = 0, 1, 2
state = GREEN

LED_PATTERN = {
    GREEN:  (True,  False),
    YELLOW: (True,  True),
    RED:    (False, True),
}
NAME = {GREEN: "GREEN", YELLOW: "YELLOW", RED: "RED"}


def show(s):
    a_on, b_on = LED_PATTERN[s]
    # เติม: เปิด/ปิด led_a ตามค่า a_on  (ใช้ led_a.on() เมื่อ a_on เป็น True, ไม่งั้น led_a.off())
    pass
    # เติม: เปิด/ปิด led_b ตามค่า b_on  (ใช้ led_b.on() / led_b.off())
    pass
    print("STATE =", NAME[s])


# debounce: จำสถานะปุ่มรอบก่อน เพื่อจับ "ขอบขาลง" (กดลงครั้งเดียว)
# เติม: อ่านสถานะปุ่มปัจจุบันด้วย btn.is_pressed() มาเก็บไว้ใน prev_pressed
prev_pressed = False
show(state)

print("กดปุ่ม SW1 เพื่อเปลี่ยนไฟจราจร (Ctrl+C เพื่อหยุด)")
while True:
    pressed = btn.is_pressed()

    # debounce แบบง่าย: นับเป็น "กด" เฉพาะตอนเพิ่งเปลี่ยนจากปล่อย -> กด (edge detection)
    if pressed and not prev_pressed:
        # เติม: เลื่อน FSM ไปสถานะถัดไปแบบวนรอบ -> state = (state + 1) % 3
        pass
        show(state)
        time.sleep_ms(50)   # หน่วงสั้น ๆ ให้สัญญาณปุ่มนิ่งก่อนอ่านต่อ

    prev_pressed = pressed
    time.sleep_ms(10)       # คุมจังหวะ loop ไม่ให้ busy เกินจำเป็น
