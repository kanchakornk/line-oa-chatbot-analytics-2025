import pandas as pd, numpy as np

# 1) โหลดไฟล์
df = pd.read_excel("Downloads/Logs.xlsx", sheet_name=0)

# 2) ชื่อคอลัมน์ "Bot Answer" (แทน C2 ในสูตร) — ถ้าชื่อไม่ตรง ปรับตามไฟล์จริง
bot_col = "Bot Answer"

# 3) กำหนดแพตเทิร์น (รวมวลีที่ให้มา)
P_BAD_WORDS       = r"(กรุณาใช้ถ้อยคำ|กรุณาพิมพ์คำที่สุภาพ)"
P_NOT_UNDERSTAND  = r"(ขอโทษค่ะ ฉันยังไม่ค่อยเข้าใจ|ฉันไม่เข้าใจความหมาย|ฉันไม่เข้าใจค่ะ|ฉันสับสน|ว่ายังไงนะคะ)"
P_FEEDBACK        = r"(ขอบคุณสำหรับความคิดเห็น|เสนอแนะ/เสนอความเห็น)"
P_REPEAT          = r"(คุณได้ทำการเลือกแล้ว)"

def label_bot_answer(series, na_means_understood=True):
    s = series.astype(str)  # แปลงให้เป็นข้อความเสมอ
    conds, choices = [], []

    # IF(C="N/A","เข้าใจข้อคำถาม", ...)
    if na_means_understood:
        conds.append(s.str.strip().str.upper().eq("N/A"))
        choices.append("เข้าใจข้อคำถาม")

    # IFS(...) — ลำดับมีความสำคัญ (เหมือนในสูตร)
    conds.append(s.str.contains(P_BAD_WORDS, case=False, regex=True, na=False))
    choices.append("ใช้ถ้อยคำไม่เหมาะสม")

    conds.append(s.str.contains(P_NOT_UNDERSTAND, case=False, regex=True, na=False))
    choices.append("ไม่เข้าใจข้อคำถาม")

    conds.append(s.str.contains(P_FEEDBACK, case=False, regex=True, na=False))
    choices.append("ข้อเสนอแนะ/ความคิดเห็น")

    conds.append(s.str.contains(P_REPEAT, case=False, regex=True, na=False))
    choices.append("เลือกซ้ำ")

    # default: ถ้าไม่เข้าข้อไหนเลย → "เข้าใจข้อคำถาม"
    return np.select(conds, choices, default="เข้าใจข้อคำถาม")

# 4) ใช้งานฟังก์ชันติดป้าย
df["Label"] = label_bot_answer(df[bot_col])

# 5) ทำธงสำหรับ KPI: เข้าใจ/ไม่เข้าใจ
df["Understood"] = (df["Label"] == "เข้าใจข้อคำถาม").astype(int)

# 6) (ตัวเลือก) ถ้ามีคอลัมน์เวลา สรุป Understanding รายวันได้
# ts_col = "Timestamp"
# df["_ts"] = pd.to_datetime(df[ts_col], errors="coerce")
# daily = (df.dropna(subset=["_ts"])
#            .assign(date=lambda d: d["_ts"].dt.date)
#            .groupby("date")
#            .agg(understanding_rate=("Understood","mean"),
#                 messages=("Understood","size"))
#            .reset_index())

# 7) บันทึกเป็น CSV พร้อมใช้ต่อใน BI
df.to_csv("logs_cleaned.csv", index=False, encoding="utf-8-sig")
(df["Label"].value_counts()
   .rename_axis("Label").reset_index(name="Count")
).to_csv("label_summary.csv", index=False, encoding="utf-8-sig")
