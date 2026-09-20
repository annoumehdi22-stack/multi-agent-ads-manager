from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import sqlite3
import requests

app = FastAPI(title="Multi-Agent Ads Manager API")

# --- 1. إعداد قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect("ads_data.db")
    cursor = conn.cursor()
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

init_db()

# --- 2. قوالب الداتا ---
class CampaignData(BaseModel):
    campaign_name: str
    spend: float
    clicks: int
    cpc: float
    purchases: int
    retour: int

class AgentResult(BaseModel):
    campaign_name: str
    analysis_summary: str
    action_recommended: str

# --- 3. المسارات (Endpoints) ---

@app.post("/api/v1/analyze-ads")
def analyze_ads_webhook(data: CampaignData, background_tasks: BackgroundTasks):
    # تسجيل الداتا فـ SQLite
    conn = sqlite3.connect("ads_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO campaigns (campaign_name, spend, clicks, cpc, purchases, retour)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data.campaign_name, data.spend, data.clicks, data.cpc, data.purchases, data.retour))
    conn.commit()
    conn.close()

    # دالة باش نصيفطو الداتا للـ Agent فـ الخلفية
    def send_to_agent(payload):
        try:
            # الرابط ديال الـ Agent ديال صاحبك وسط Docker
            requests.post("http://ai_agents:5000/process", json=payload)
        except Exception as e:
            print(f"Agent mazal ma wajdch: {e}")

    background_tasks.add_task(send_to_agent, data.dict())

    return {"status": "success", "message": "Data wslat l SQL, o mchat l'Agent f lkhalfia!"}

@app.get("/api/v1/campaigns")
def get_all_campaigns():
    conn = sqlite3.connect("ads_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM campaigns")
    rows = cursor.fetchall()
    conn.close()
    return {"status": "success", "data": [dict(row) for row in rows]}

@app.post("/api/v1/results")
def receive_agent_results(result: AgentResult, background_tasks: BackgroundTasks):
    
    # دالة باش نصيفطو الخلاصة لـ Slack عبر Make.com
    def send_to_make(payload):
        make_webhook_url = "https://hook.eu2.make.com/gibqhe237i473ggc1xv14sm0npjc67r6"
        try:
            requests.post(make_webhook_url, json=payload)
        except Exception as e:
            print(f"Mochkil f tsifit l Make: {e}")
            
    background_tasks.add_task(send_to_make, result.dict())
    return {"status": "success", "message": "Natija wslat o mchat l Make.com!"}