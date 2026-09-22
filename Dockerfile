<<<<<<< HEAD
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
=======
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
>>>>>>> a0f274d63754908b86e4bc06429976340bae7fbc
