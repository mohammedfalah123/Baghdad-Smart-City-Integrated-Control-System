# ==================== صورة Python خفيفة ====================
FROM python:3.9-slim

# ==================== تثبيت متطلبات النظام الأساسية فقط ====================
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ==================== إنشاء مستخدم غير جذري ====================
RUN useradd -m -u 1000 user
USER user

# ==================== إعداد متغيرات البيئة ====================
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONPATH=/home/user/app:$PYTHONPATH \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=42 \
    OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1

# ==================== إنشاء مجلد العمل ====================
WORKDIR $HOME/app

# ==================== ترقية pip ====================
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# ==================== تثبيت pytest أولاً ====================
RUN pip install --no-cache-dir pytest==7.4.0

# ==================== تثبيت numpy و pandas أولاً ====================
RUN pip install --no-cache-dir numpy==1.24.3 pandas==2.0.3

# ==================== تثبيت pandapower ====================
RUN pip install --no-cache-dir pandapower==2.12.0

# ==================== تثبيت huggingface_hub أولاً ====================
RUN pip install --no-cache-dir huggingface-hub==0.23.4

# ==================== تثبيت باقي المكتبات ====================
RUN pip install --no-cache-dir \
    scipy==1.11.1 \
    matplotlib==3.7.2 \
    plotly==5.17.0 \
    mealpy==3.0.1 \
    gradio==4.44.1 \
    requests==2.31.0 \
    psutil==5.9.0 \
    typing-extensions==4.7.1 \
    python-dateutil==2.8.2 \
    pytz==2023.3

# ==================== تنظيف ذاكرة التخزين المؤقت ====================
RUN pip cache purge

# ==================== نسخ الكود ====================
COPY --chown=user . $HOME/app

# ==================== تشغيل التطبيق ====================
CMD ["python", "app.py"]
