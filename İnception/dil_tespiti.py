
import pandas as pd
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Sonuçlar her çalıştırmada aynı olsun
DetectorFactory.seed = 0

# 🔹 Yeni birleşik Excel dosyasını oku
df = pd.read_excel("tum_yorumlar.xlsx")

def detect_language(text):
    try:
        if pd.isna(text) or len(str(text).strip()) < 3:
            return "unknown"
        return detect(text)
    except LangDetectException:
        return "unknown"

# 🔹 'yorum' sütunu üzerinden dil tespiti
df["language"] = df["yorum"].apply(detect_language)

# 🔹 Yeni Excel olarak kaydet
df.to_excel("tum_yorumlar_with_language.xlsx", index=False)

print("✅ Dil tespiti bitti.")
print("📁 tum_yorumlar_with_language.xlsx oluşturuldu")
