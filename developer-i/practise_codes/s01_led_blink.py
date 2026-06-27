# s01_led_blink.py - LED ดวงแรกของเรา (ฉบับฝึกเติมโค้ด)
# วิธีรัน: เปิดไฟล์นี้ใน BENTO IDE แล้วกด "Program to Device"
#
# เติมช่องว่างตามคำใบ้ให้ครบ แล้วลองรันบนบอร์ดจริง
# โมดูล gpio จัดการขา GPIO ที่ต่อกับ LED ให้เราเป็น output อยู่แล้ว

import gpio
import time

# ถามบอร์ดว่ามี LED กี่ดวง จะได้วนลูปไม่เกินจำนวนจริง
n = gpio.num_leds()
print("บอร์ดนี้มี LED ทั้งหมด", n, "ดวง")
print("ข้อมูลบอร์ด:", gpio.board_info())

# --- สเต็ป 1: เปิดแล้วปิด LED2 (สีเขียว, index 1) ---
# ใช้ LED2 (เขียว) เพราะ LED1 (แดง, index 0) มักถูกใช้เป็นไฟ status ของระบบหลัก
led = gpio.led(1)
# เติม: สั่งให้ LED2 ติด ด้วย led.on()
pass
time.sleep_ms(500)
# เติม: สั่งให้ LED2 ดับ ด้วย led.off()
pass
time.sleep_ms(500)

# --- สเต็ป 2: กะพริบเป็นจังหวะ 5 ครั้งด้วย toggle() ---
for i in range(5):
    # เติม: สลับสถานะ LED ด้วย led.toggle()  (ติด<->ดับ)
    pass
    time.sleep_ms(200)
led.off()

# --- สเต็ป 3: ไฟวิ่ง knight-rider ข้าม LED ทุกดวง ---
for sweep in range(3):
    # ไปข้างหน้า: 0, 1, 2, ...
    for i in range(n):
        # เติม: เปิด LED ดวงที่ i ด้วย gpio.led(i).on()
        pass
        time.sleep_ms(80)
        gpio.led(i).off()
    # ย้อนกลับ: ..., 2, 1
    for i in range(n - 2, 0, -1):
        gpio.led(i).on()
        time.sleep_ms(80)
        # เติม: ปิด LED ดวงที่ i ด้วย gpio.led(i).off()
        pass

print("จบแล้ว เก่งมาก ลองปรับเวลา sleep_ms ดูว่าจังหวะเปลี่ยนยังไง")
