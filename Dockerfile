# كنجيبو نسخة خفيفة ديال بايثون
FROM python:3.9-slim

# كنحددو مسار العمل لداخل فـ الصندوق
WORKDIR /app

# كنكوبيو ملف المكتبات وكنأنسطاليوهوم
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# كنكوبيو الكود ديالك كامل للصندوق
COPY . .

# كنحلو الباب رقم 8000
EXPOSE 8000

# الكوموند باش يخدم السيرفر أوتوماتيكياً
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]