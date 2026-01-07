# logchatbot.py  — ง่ายสุด, ไม่ต้องพิมพ์พาธยาว
import pandas as pd, numpy as np
from pathlib import Path

# อ่าน Excel ที่อยู่โฟลเดอร์เดียวกับสคริปต์
BASE = Path(__file__).parent
excel_path = BASE / "Logs (2).xlsx"     # ต้องมีไฟล์ชื่อนี้อยู่ใน Downloads

# โหลดข้อมูล
df = pd.read_excel(excel_path, sheet_name=0, engine="openpyxl")

# เดาชื่อคอลัมน์ "คำตอบของบอท" แบบอัตโนมัติ (ถ้าไม่เจอใช้คอลัมน์ที่ 3)
def pick_bot_col(cols):
    for c in cols:
        cl = str(c).lower()
        if any(k in cl for k in ["bot", "answer", "ตอบ", "คำตอบ"]):
            return c
    return cols[2]  # fallback = คอลัมน์ C

BOT_COL = pick_bot_col(df.columns)

# แพตเทิร์นตามสูตร Google Sheets เดิม
P_BAD = r"(กรุณาใช้ถ้อยคำ|กรุณาพิมพ์คำที่สุภาพ)"
P_NOTUN = r"(ขอโทษค่ะ ฉันยังไม่ค่อยเข้าใจ|ฉันไม่เข้าใจความหมาย|ฉันไม่เข้าใจค่ะ|ฉันสับสน|ว่ายังไงนะคะ)"
P_FB = r"(ขอบคุณสำหรับความคิดเห็น|เสนอแนะ/เสนอความเห็น)"
P_REPEAT = r"(คุณได้ทำการเลือกแล้ว)"

def label(series):
    s = series.astype(str)
    conds, choices = [], []
    conds.append(s.str.strip().str.upper().eq("N/A")); choices.append("เข้าใจข้อคำถาม")
    conds.append(s.str.contains(P_BAD,   case=False, regex=True, na=False)); choices.append("ใช้ถ้อยคำไม่เหมาะสม")
    conds.append(s.str.contains(P_NOTUN, case=False, regex=True, na=False)); choices.append("ไม่เข้าใจข้อคำถาม")
    conds.append(s.str.contains(P_FB,    case=False, regex=True, na=False)); choices.append("ข้อเสนอแนะ/ความคิดเห็น")
    conds.append(s.str.contains(P_REPEAT,case=False, regex=True, na=False)); choices.append("เลือกซ้ำ")
    return np.select(conds, choices, default="เข้าใจข้อคำถาม")

df["Label"] = label(df[BOT_COL])
df["Understood"] = (df["Label"] == "เข้าใจข้อคำถาม").astype(int)

# บันทึกผลไว้ที่โฟลเดอร์เดียวกับสคริปต์
(df).to_csv(BASE / "logs_cleaned.csv", index=False, encoding="utf-8-sig")
(df["Label"].value_counts().rename_axis("Label").reset_index(name="Count")
 ).to_csv(BASE / "label_summary.csv", index=False, encoding="utf-8-sig")

print("✅ เสร็จแล้ว → logs_cleaned.csv, label_summary.csv")
