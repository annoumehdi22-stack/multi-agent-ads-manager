from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import json

app = FastAPI(title="Meta Ads Deep Data Analyst Tool")

import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class MetaAdDataRequest(BaseModel):
    campaign_name: str
    spend: float
    clicks: int
    impressions: int
    conversions: int
    cpc: float
    ctr: float

@app.post("/tool/meta-analyst")
def analyze_meta_ads(data: MetaAdDataRequest):
    try:
        # تجهيز الداتا للتحليل العميق
        prompt = f"""
        Campaign Name: {data.campaign_name}
        Spend: ${data.spend}
        Clicks: {data.clicks}
        Impressions: {data.impressions}
        Conversions: {data.conversions}
        CPC: ${data.cpc}
        CTR: {data.ctr}%
        """
        
        # استدعاء الموديل مع برومبت خاص بالتحليل العميق والدقيق
        completion = client.chat.completions.create(
            model="allam-2-7b",
            messages=[
                {
                    "role": "system", 
                    "content": """You are an expert Meta Ads deep data analyst. 
                    Calculate the following metrics accurately:
                    - CPA (Spend / Conversions) -> if conversions is 0, set to 0
                    - ROAS (Assume each conversion is worth $100: (Conversions * 100) / Spend) -> if spend is 0, set to 0
                    - Conversion Rate ((Conversions / Clicks) * 100)
                    - CPM ((Spend / Impressions) * 1000)
                    
                    You MUST return the result strictly as a valid JSON object. Do not add any extra text, markdown, or explanations.
                    Use this exact JSON format:
                    {
                        "cpa": 0.0, 
                        "roas": 0.0, 
                        "conversion_rate": 0.0, 
                        "ctr": 0.0,
                        "cpc": 0.0,
                        "cpm": 0.0,
                        "deep_insights": "Detailed 1 or 2 sentence diagnosis explaining funnel health, audience targeting, or ad performance based on these metrics."
                    }"""
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )

        raw_result = completion.choices[0].message.content
        analyst_data = json.loads(raw_result)

        # إرجاع التحليل العميق بوحده بشكل نقي
        return {
            "status": "success",
            "campaign": data.campaign_name,
            "deep_analysis": analyst_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"REAL ERROR: {str(e)}")

    