# 🤖 End-to-End LINE Chatbot Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Google Sheets](https://img.shields.io/badge/Google_Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white)

## 📌 Project Overview
**"Optimizing User Experience through Data-Driven Insights & Automated Pipeline"**

โปรเจกต์นี้มีเป้าหมายเพื่อแก้ปัญหา Chatbot ตอบไม่ตรงคำถาม (Fallback Rate สูง) โดยการพัฒนาระบบ **End-to-End Data Pipeline** ตั้งแต่การดึงข้อมูล Real-time ผ่าน Webhook, การทำ Data Cleaning ขั้นสูงด้วย **Python (Pandas & NumPy)** เพื่อจัดการข้อความภาษาไทยที่มีความซับซ้อน และแสดงผลผ่าน **Power BI Dashboard** เพื่อเปลี่ยนข้อมูลดิบให้เป็น Actionable Insights สำหรับการตัดสินใจทางธุรกิจ

---

## 🧭 Executive Summary & Business Impact

| Metric | Before (Manual Process) | After (Automated Analytics) | Improvement |
| :--- | :--- | :--- | :--- |
| **Understanding Rate** | 75.0% | **88.9%** | 🔺 +13.9% |
| **Fallback Rate** | 25.0% | **11.1%** | 🔻 -13.9% |
| **Workflow Efficiency** | Manual Excel Export | **Python Automation** | ⚡ 100% Automated |

---

## 🛑 Business Problem & Solution
* **The Pain Point:** ทีมงานไม่ทราบว่าผู้ใช้ถามอะไรบอทบ้าง และการตรวจสอบ Log เดิมทำได้ยากเนื่องจากข้อมูลเป็นข้อความดิบ (Unstructured Text) ที่ไม่มีการจัดหมวดหมู่
* **The Solution:** สร้าง Automated Pipeline ที่ใช้ Python จัดกลุ่มประโยคสนทนาอัตโนมัติ (Auto-Labeling) และเชื่อมต่อกับ Power BI เพื่อดูแนวโน้มปัญหาได้ทันที

---

## 🏗️ Technical Architecture & My Role

**(1) Data Ingestion (Real-time Logging)**
* เขียน **Google Apps Script** เป็น Webhook Middleware ดักจับ Events จาก LINE OA
* บันทึก Log การสนทนาลง Google Sheets โดยอัตโนมัติแบบ Real-time

**(2) Data Processing (Python Automation)**
* **Extract:** โหลดข้อมูลจาก Excel/CSV ผ่าน Python script (`logchatbot.py`)
* **Transform:**
    * **Vectorization:** ใช้ `numpy.select` แทนการวนลูป (Loop) เพื่อประสิทธิภาพในการประมวลผลข้อมูลขนาดใหญ่
    * **Thai NLP Regex:** กำหนด Pattern Regex ภาษาไทยเพื่อจับกลุ่ม Intent เช่น "ไม่เข้าใจ", "ใช้คำไม่สุภาพ"
* **Load:** ส่งออกไฟล์ `logs_cleaned.csv` ที่พร้อมใช้งานเข้าสู่ Power BI

**(3) Data Modeling & Visualization**
* สร้าง **Star Schema** ใน Power BI เชื่อมโยงข้อมูล `Chat Logs` กับ `Student Profile`
* เขียน **DAX Measures** เพื่อคำนวณ KPIs ที่ซับซ้อน เช่น *Dynamic Fallback Rate* และ *Peak Hour Analysis*

---

## 💻 Technical Implementation Highlights

### A. Advanced Data Labeling with NumPy & Regex
> *Code Snippet จริงจากไฟล์ `logchatbot.py` ที่ใช้การจัดการข้อมูลแบบ Vectorized Operation เพื่อความแม่นยำและรวดเร็ว*

```python
import pandas as pd
import numpy as np
from pathlib import Path

# กำหนด Regex Pattern สำหรับภาษาไทย (Thai Regex Patterns)
P_BAD = r"(กรุณาใช้ถ้อยคำ|กรุณาพิมพ์คำที่สุภาพ)"
P_NOTUN = r"(ขอโทษค่ะ ฉันยังไม่ค่อยเข้าใจ|ฉันไม่เข้าใจความหมาย|ฉันไม่เข้าใจค่ะ|ฉันสับสน|ว่ายังไงนะคะ)"
P_FB = r"(ขอบคุณสำหรับความคิดเห็น|เสนอแนะ/เสนอความเห็น)"
P_REPEAT = r"(คุณได้ทำการเลือกแล้ว)"

def label(series):
    s = series.astype(str)
    conds, choices = [], []
    
    # Condition 1: Handle N/A as Understood
    conds.append(s.str.strip().str.upper().eq("N/A")); choices.append("เข้าใจข้อคำถาม")
    
    # Condition 2-5: Regex Matching using Vectorized Operations
    conds.append(s.str.contains(P_BAD,   case=False, regex=True, na=False)); choices.append("ใช้ถ้อยคำไม่เหมาะสม")
    conds.append(s.str.contains(P_NOTUN, case=False, regex=True, na=False)); choices.append("ไม่เข้าใจข้อคำถาม")
    conds.append(s.str.contains(P_FB,    case=False, regex=True, na=False)); choices.append("ข้อเสนอแนะ/ความคิดเห็น")
    conds.append(s.str.contains(P_REPEAT,case=False, regex=True, na=False)); choices.append("เลือกซ้ำ")
    
    # Use np.select for high performance on large datasets
    return np.select(conds, choices, default="เข้าใจข้อคำถาม")

# Apply logic and create flag
df["Label"] = label(df[BOT_COL])
df["Understood"] = (df["Label"] == "เข้าใจข้อคำถาม").astype(int)
```
### B. DAX for Dynamic KPIs
> *การสร้างสูตรคำนวณอัตราความเข้าใจของบอท (Understanding Rate) เพื่อวัดผลประสิทธิภาพโมเดล*
---


```dax
Understanding Rate % = 
VAR GoodAnswers = CALCULATE(COUNTROWS('ChatLogs'), 'ChatLogs'[Understood] = 1)
VAR TotalMsg = COUNTROWS('ChatLogs')
RETURN 
DIVIDE(GoodAnswers, TotalMsg, 0)

```

---

## 🎯 Key Insights & Strategic Actions

### 📈 Insight #1: Seasonal Peak Management

* **🧐 Finding:** ยอดการใช้งานพุ่งสูงผิดปกติในวันที่ **24 พ.ค.** (+300% จากค่าเฉลี่ย) ซึ่งตรงกับช่วงวันลงทะเบียนเรียนวันแรก
* **🚀 Action:** ปรับ UX ของ Chatbot เป็น **Dynamic Menu** โดยย้ายปุ่ม "ลงทะเบียนเรียน" ขึ้นมาเป็นอันดับ 1 เฉพาะในช่วงสัปดาห์นั้น เพื่อลดเวลาในการค้นหาข้อมูลของผู้ใช้

### 🧩 Insight #2: Hidden Intent Discovery

* **🧐 Finding:** บอทตอบ "ไม่เข้าใจ" บ่อยที่สุดในหมวดคำถามเกี่ยวกับ **"ปฏิทินการศึกษา"** เนื่องจากผู้ใช้ใช้ Keyword ที่หลากหลายเกินกว่า Rule เดิมที่ตั้งไว้
* **🚀 Action:** ปรับปรุง Knowledge Base โดยเพิ่ม **Training Phrases** ที่เกี่ยวข้อง และตั้งค่าให้บอทส่งลิงก์รูปภาพปฏิทินทันทีแทนการตอบเป็นข้อความยาวๆ

### 🎓 Insight #3: Demographic Targeting

* **🧐 Finding:** ผู้ใช้งานหลักคือ **นักศึกษาชั้นปีที่ 4 (61%)** ซึ่งมักถามเรื่องการแจ้งจบการศึกษาและกำหนดการรับปริญญา
* **🚀 Action:** สร้าง Content Strategy ใหม่ เพิ่มเมนู **"Checklist ก่อนจบการศึกษา"** เข้าไปใน Flow หลัก เพื่อ Proactive ให้ข้อมูลก่อนที่ผู้ใช้จะถาม

---

## 🛠️ Challenges & Problem Solving

| Challenge | What Happened (Situation) | Technical Solution (Action) | Business Outcome (Result) |
| --- | --- | --- | --- |
| **Unstructured Thai Text** | Log การสนทนาเป็นประโยคยาว, พิมพ์ผิด, และไม่มีโครงสร้างที่แน่นอน | ใช้ **Python Regex** จับ Pattern คำหลัก และสร้าง Logic **Auto-labeling** เพื่อจัดกลุ่ม | จัดหมวดหมู่ Intent ได้อัตโนมัติ แม่นยำกว่า 90% วัดผล KPI ได้ชัดเจน |
| **Scalability Issue** | สูตร Excel เดิม (Nested IFs) ประมวลผลช้ามากเมื่อข้อมูล Log เพิ่มขึ้นหลักหมื่นแถว | เปลี่ยนมาใช้ **NumPy `np.select**` (Vectorized Operation) แทนการวน Loop | ประมวลผลเร็วขึ้น **10x** และรองรับข้อมูลขนาดใหญ่ได้ในอนาคต |
| **DataSource Path Error** | เมื่อย้ายไฟล์ Script ไปรันเครื่องอื่น Power BI มักหาไฟล์ Source ไม่เจอ | ใช้ Library **`pathlib`** ใน Python เพื่อควบคุม Relative Path ให้ไฟล์ Output อยู่ที่เดียวกับ Script เสมอ | โปรเจกต์มีความยืดหยุ่น (**Portable**) สามารถย้ายโฟลเดอร์หรือแชร์ให้ทีมงานได้ทันทีโดยไม่ Error |

---

## 📁 Repository Structure

```plaintext
├── 📂 linechatbot_logs/
│   ├── 🐍 logchatbot.py                       # Main ETL Script (Extract-Transform-Load)
│   ├── 🐍 cleaninglog.py                      # Cleaning Logic & Regex Patterns module
│   ├── 📄 linechatbot_logs_clean_2025.csv       # Processed data ready for Power BI
│   └── 📄 linechatbot_logs_clean_2025_summary.csv # Aggregated stats / summary
├── 📂 dashboards/
│   └── 📊 linechatbot_analytics_2025.pbix       # Power BI project file
└── 📂 assets/
    └── 🖼️ architecture_diagram.png              # System architecture diagram

```
