# 1.jib Python 3.10 rasmi
FROM python:3.10-slim

# 2.dir working directory
WORKDIR /app

# 3.copia requirements w installihom
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4.copia l-kod kamal
COPY . .

# 5.Port li ghadi ykhdm fih (8002)
EXPOSE 8002

# 6.Command bash ych3l l-server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]