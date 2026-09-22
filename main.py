from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import sqlite3
import requests

# 1. Configuration dyal l'API
app = FastAPI(
    title="Multi-Agent Ads Manager API",
    description="Système central pour l'automatisation Meta Ads -> AI -> Slack",
    version="1.1.0"
)

# 2. Initialisation dyal la base de données
def init_db():
    conn = sqlite3.connect("ads_data.db")
    cursor = conn.cursor()
    
    # Table dyal les campagnes (Data li jaya mn Typeform/Make)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_name TEXT,
            spend REAL,
            clicks INTEGER,
            cpc REAL,
            purchases INTEGER,
            retour REAL
        )
    """)
    
    # Table dyal les résultats de l'IA (Archive)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_name TEXT,
            analysis_summary TEXT,
            action_recommended TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Nlanciw l'initialisation f l'démarrage
init_db()

# 3. Les Modèles de Données (Schemas Pydantic)
class CampaignData(BaseModel):
    campaign_name: str
    spend: float
    clicks: int
    cpc: float
    purchases: int
    retour: float

class AgentResult(BaseModel):
    campaign_name: str
    analysis_summary: str
    action_recommended: str

# 4. Les Endpoints dyal l'Application

@app.post("/api/v1/analyze-ads", tags=["Data Ingestion"])
def analyze_ads_webhook(data: CampaignData, background_tasks: BackgroundTasks):
    """Kyst9bel d-data mn Make.com w kaysiftha l'Agent f l'khalfia"""
    
    # a. Sauvegarde f SQLite
    try:
        conn = sqlite3.connect("ads_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO campaigns (campaign_name, spend, clicks, cpc, purchases, retour)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (data.campaign_name, data.spend, data.clicks, data.cpc, data.purchases, data.retour))
        conn.commit()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mochkil f base de données: {str(e)}")

    # b. Fonction li ghatmchi l'AI (Background Task)
    def send_to_agent(payload):
        try:
            # L'URL dyal l'Agent dyal Amine (f réseau Docker)
            requests.post("http://ai_agents:5000/process", json=payload, timeout=10)
        except Exception as e:
            print(f"Warning: L'Agent mazal ma wajdch wla t9t3at 3lih l'connexion -> {e}")

    # Lanci l'envoi bla ma t-bloki Make.com
    background_tasks.add_task(send_to_agent, data.dict())

    return {"status": "success", "message": "Data mchat l'SQLite w tsiftat l'Agent"}


@app.get("/api/v1/campaigns", tags=["Data Retrieval"])
def get_all_campaigns():
    """L'Agent y9dr yjib d-data l9dima mn hna ila bghaha"""
    conn = sqlite3.connect("ads_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM campaigns ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return {"status": "success", "data": [dict(row) for row in rows]}


@app.post("/api/v1/results", tags=["AI Results"])
def receive_agent_results(result: AgentResult, background_tasks: BackgroundTasks):
    """Kyst9bel l'analyse dyal l'AI, kaysjlha, w kaysiftha l Slack"""
    
    # a. Sauvegarde f SQLite (Archive AI)
    try:
        conn = sqlite3.connect("ads_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ai_results (campaign_name, analysis_summary, action_recommended)
            VALUES (?, ?, ?)
        """, (result.campaign_name, result.analysis_summary, result.action_recommended))
        conn.commit()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mochkil f base de données (AI): {str(e)}")

    # b. Envoi l'Make.com (Slack)
    def send_to_make(payload):
        # ⚠️ Bdel had l'URL b l'Webhook dyalk
        make_webhook_url = "https://hook.eu2.make.com/gibqhe237i473ggc1xv14sm0npjc67r6"
        try:
            requests.post(make_webhook_url, json=payload, timeout=10)
        except Exception as e:
            print(f"Erreur f tsifit l Make.com: {e}")
            
    background_tasks.add_task(send_to_make, result.dict())
    
    return {"status": "success", "message": "Résultat t-sauvegarda w tsift l Slack"}


@app.get("/api/v1/ai-results", tags=["AI Results"])
def get_ai_results_history():
    """Bach tchof l'archive dyal l'AI kaml"""
    conn = sqlite3.connect("ads_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ai_results ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return {"status": "success", "data": [dict(row) for row in rows]}