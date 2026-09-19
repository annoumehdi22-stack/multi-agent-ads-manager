from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3 # هادي هي المكتبة اللي غتخدم لينا SQL

app = FastAPI(title="Multi-Agent Ads Manager API")

# 1. هاد الدالة كتصايب قاعدة البيانات والطابلو إيلا ماكانوش
def init_db():
    conn = sqlite3.connect("ads_data.db") # غيكريي هاد الفيشي فـ الدوسي ديالك
    cursor = conn.cursor()
    # كود SQL باش نصايبو الطابلو
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_name TEXT,
            spend REAL,
            clicks INTEGER,
            cpc REAL,
            purchases INTEGER,
            retour INTEGER
        )
    """)
    conn.commit()
    conn.close()

# كنعيطو للدالة باش تخدم غير نشعلو السيرفر
init_db()

# 2. القالب ديال الداتا اللي قادينا قبل
class CampaignData(BaseModel):
    campaign_name: str
    spend: float
    clicks: int
    cpc: float
    purchases: int
    retour: int

# 3. الاستقبال والتسجيل فـ SQL
@app.post("/api/v1/analyze-ads")
def analyze_ads_webhook(data: CampaignData):
    
    # كنحلو الباب لقاعدة البيانات باش نكتبو فيها
    conn = sqlite3.connect("ads_data.db")
    cursor = conn.cursor()
    
    # كود SQL باش ندخلو سطر جديد (INSERT)
    cursor.execute("""
        INSERT INTO campaigns (campaign_name, spend, clicks, cpc, purchases, retour)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data.campaign_name, data.spend, data.clicks, data.cpc, data.purchases, data.retour))
    
    conn.commit() # كنأكدو التسجيل
    conn.close()  # كنسدو الباب
    
    return {
        "status": "success", 
        "message": f"Data dyal {data.campaign_name} wslat o tsjlat f SQL mzian!",
        "received_data": data
    }
# مسار جديد باش الـ Agents يقراو الداتا
@app.get("/api/v1/campaigns")
def get_all_campaigns():
    # كنحلو الباب لقاعدة البيانات
    conn = sqlite3.connect("ads_data.db")
    
    # هاد السطر كيخلي الداتا ترجع مقادة بالسميات ديالها (بحال JSON) ماشي غير أرقام مرونة
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    # كود SQL باش نجبدو كاع الإعلانات اللي مسجلة (SELECT)
    cursor.execute("SELECT * FROM campaigns")
    rows = cursor.fetchall()
    conn.close() # كنسدو الباب
    
    # كنحولو الداتا لـ List باش يفهمها الذكاء الاصطناعي
    campaigns_list = [dict(row) for row in rows]
    
    # كنرجعو النتيجة للـ Agent
    return {
        "status": "success",
        "total_campaigns": len(campaigns_list),
        "data": campaigns_list
    }