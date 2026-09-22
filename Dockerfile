# 1. جلب نسخة بايثون الأساسية
FROM python:3.10-slim

# 2. تحديد المجلد الرئيسي داخل الحاوية
WORKDIR /app

# 3. نسخ ملف المكتبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. نسخ باقي ملفات المشروع للداخل
COPY . .

# 5. فتح المنفذ (Port)
EXPOSE 8000

# 6. الأمر المسؤول عن تشغيل السيرفر تلقائياً
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]