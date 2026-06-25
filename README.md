# Embedded Systems for Developer

> เรียนรู้ **ระบบสมองกลฝังตัว (Embedded Systems)** จากของจริงบนบอร์ด **BENTO PSoC Edge** ด้วยภาษา **MicroPython** — แตะฮาร์ดแวร์จริง แล้วสร้างเกมและงาน IoT ได้ด้วยมือตัวเอง

### ดูสไลด์ออนไลน์ (ไม่ต้องติดตั้งอะไร)

**https://advance-innovation-centre-aic.github.io/embedded-systems-for-developer/**

---

## สำหรับใคร

หลักสูตรนี้ออกแบบสำหรับ **นิสิตภาควิชาวิศวกรรมระบบสมองกลฝังตัว และภาควิชาวิศวกรรมไฟฟ้า คณะวิศวกรรมศาสตร์ มหาวิทยาลัยบูรพา**

แนวคิดของเราคือ — embedded ไม่จำเป็นต้องเริ่มจากทฤษฎียาก ๆ หรือสู้กับ toolchain ของภาษา C ตั้งแต่วันแรก เราเริ่มจาก **MicroPython** ที่เห็นผลทันทีบน REPL สั่งฮาร์ดแวร์จริง (LED, ปุ่ม, เซนเซอร์, WiFi) แล้วค่อย ๆ ประกอบขึ้นเป็นเกมและระบบ IoT ที่เล่นและใช้งานได้จริง

หัวใจของทุกคาบคือสูตร **core 70% / เขียนเอง 30%** — เราเตรียม engine (70%) ไว้ให้ น้อง ๆ โฟกัสเขียนตรรกะสำคัญ (30%) เอง จึงได้ของที่เล่นได้ตั้งแต่คาบแรก ๆ และเข้าใจลึกขึ้นเรื่อย ๆ ตามเส้นทาง:

**เล่นได้ → แก้ได้ → สร้างได้ → ส่งจริง**

---

## หลักสูตร 3 ส่วน

| ส่วน | เนื้อหา | ทักษะหลัก | ลิงก์ |
|------|---------|-----------|-------|
| **Developer I** (14 คาบ) | รากฐาน embedded → LED · ปุ่ม · timer · เซนเซอร์ · เสียง · WiFi แล้วประกอบเป็น 2 เกม **Pong + Space Shooter** | GPIO, FSM, game loop, เวกเตอร์, การชน, AI พื้นฐาน, object pool, WiFi+MQTT | [เปิดหลักสูตร](https://advance-innovation-centre-aic.github.io/embedded-systems-for-developer/developer-i/roadmap.html) |
| **Developer II** (13 คาบ) | ต่อยอด → **Snake** (list/deque) + **Flappy Bird** (ฟิสิกส์แรงโน้มถ่วง) + interrupts | โครงสร้างข้อมูล, physics integration, delta-time, `Pin.irq`, IoT | [เปิดหลักสูตร](https://advance-innovation-centre-aic.github.io/embedded-systems-for-developer/developer-ii/roadmap.html) |
| **Extra — WiFi + MQTT** (10 โปรเจกต์) | IoT Extra Projects → leaderboard, เล่นข้ามบอร์ด, telemetry, แจ้งเตือน, รีโมตคุมข้ามบอร์ด | pub/sub, MQTT, IoT/Industry 4.0, multiplayer | [เปิด Extra Pack](https://advance-innovation-centre-aic.github.io/embedded-systems-for-developer/extra/index.html) |

---

## สิ่งที่น้อง ๆ จะได้

- เขียน **MicroPython** สั่งฮาร์ดแวร์จริงบน PSoC Edge — GPIO (LED/ปุ่ม), timer/interrupt, ADC, เซนเซอร์ I2C (accelerometer), เสียง, จอ
- เข้าใจ **game loop** (read → update → draw), ฟิสิกส์เวกเตอร์/แรงโน้มถ่วง, การชน (AABB), โครงสร้างข้อมูล (list/deque), object pool, และ AI คู่ต่อสู้ตัวแรก
- ต่อ **WiFi + MQTT** ทำงาน IoT จริง (ส่งเซนเซอร์ขึ้นคลาวด์, leaderboard, เล่นข้ามบอร์ด) — pattern เดียวกับ Industrial IoT
- ฝึก **DevOps เบื้องต้น** — branch, commit, release ส่งงานให้เพื่อนโหลดไปเล่นได้จริง

---

## เริ่มต้นอย่างไร

1. **อุปกรณ์**: บอร์ด **BENTO PSoC Edge** (AI Kit หรือ Eval Kit)
2. **เครื่องมือ**: ติดตั้ง **BENTO IDE** (ส่วนขยายบน VS Code) — ดูที่ https://ide.tesaiot.com/
3. **รันโค้ด**: เปิดไฟล์ `.py` ใน BENTO IDE แล้วกดปุ่ม **Program to Device**
4. **ต่อ WiFi** (สำหรับคาบ IoT): ต่อผ่านเมนู **Wi-Fi บนจอบอร์ด** ครั้งเดียว (เซฟรหัสไว้ บอร์ดจะ auto-connect ทุกครั้งที่เปิด) — คลื่น **2.4GHz** เท่านั้น

> สไลด์ทั้งหมดเปิดดูบนเว็บได้เลยจากลิงก์ด้านบน (ในห้องเรียนกดดูทีละหน้า หรือกด overview ดูภาพรวมแล้วคลิกข้ามหน้าได้)

---

## โครงสร้าง repo

```
embedded-systems-for-developer/        (เว็บไซต์ static — GitHub Pages)
├── index.html              หน้าแรก เลือก 3 ส่วน
├── developer-i/            สไลด์ Developer I (roadmap + คาบ 1–14)
├── developer-ii/           สไลด์ Developer II (roadmap + คาบ 1–13)
└── extra/                  สไลด์ Extra WiFi+MQTT (index + 10 โปรเจกต์)
```

ซอร์สต้นฉบับ (ไฟล์ `.md`, โค้ดตัวอย่าง `practise_codes/` · `solution_codes/`, เกมเต็ม) อยู่ที่รีโปหลักสูตร
[game-development-on-embedded-systems](https://github.com/Advance-Innovation-Centre-AIC/game-development-on-embedded-systems)

---

## ผู้จัดทำ

**BENTO & TESAIoT** · Advance Innovation Centre (AIC)
จัดทำสำหรับนิสิตคณะวิศวกรรมศาสตร์ มหาวิทยาลัยบูรพา

*BENTO : : Make Anything.*
