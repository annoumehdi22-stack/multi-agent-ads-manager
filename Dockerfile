# جلب نسخة بايثون الأساسية
FROM python:3.10-slim

# تحديد المجلد الرئيسي داخل الحاوية
WORKDIR /app

# نسخ ملف المكتبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع للداخل
COPY . .

# فتح المنفذ (Port) الخاص بالسيرفر
EXPOSE 8000

# الأمر المسؤول عن تشغيل السيرفر أوتوماتيكياً
CMD ["uvicorn", "tool1_analyst:app", "--host", "0.0.0.0", "--port", "8000"]