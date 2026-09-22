from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Meta Ads Action Plan Microservice", version="1.0")

class DeepAnalysis(BaseModel):
    cpa: float
    roas: float
    conversion_rate: float
    ctr: float
    cpc: float
    cpm: float

class CampaignInput(BaseModel):
    status: str
    campaign: str
    deep_analysis: DeepAnalysis

@app.post("/generate-action-plan")
def generate_action_plan(data: CampaignInput):
    try:
        metrics = data.deep_analysis
        actions = []
        
        # قواعد توليد خطط العمل بناءً على التحليل
        if metrics.roas < 2.0:
            actions.append("⚠️ ROAS منخفض: قم بإيقاف الحملات غير المربحة وركز على إعادة الاستهداف (Retargeting).")
        else:
            actions.append("✅ ROAS ممتاز: حافظ على الميزانية الحالية مع تجربة رفعها بنسبة 15% للتوسع.")
            
        if metrics.conversion_rate < 2.0:
            actions.append("🔍 نسبة التحويل هابطة: قم بتحسين صفحة الهبوط (Landing Page) وتسهيل عملية الشراء.")
        else:
            actions.append("🚀 مسار الشراء خدام بكفاءة عالية، استمر في نفس الاستراتيجية.")
            
        if metrics.cpc > 1.0:
            actions.append("💸 تكلفة النقرة مرتفعة: قم بتغيير التصميمات الإعلانية (Creatives) وجرب عناوين جديدة.")
        else:
            actions.append("🎯 تكلفة النقرة مستقرة ورخيصة، الاستهداف دقيق وناجح.")
            
        if metrics.cpm > 10.0:
            actions.append("📢 تكلفة ألف ظهور (CPM) مرتفعة: قم بتوسيع الجمهور المستهدف قليلاً لتخفيف الضغط.")

        return {
            "status": "success",
            "microservice": "action-plan-generator",
            "campaign": data.campaign,
            "total_actions": len(actions),
            "action_plan": actions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))