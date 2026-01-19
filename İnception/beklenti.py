import pandas as pd
from collections import Counter
import re

# ==========================
# 1️⃣ Dosyayı oku
# ==========================
INPUT_FILE = "yorumlar_segmented_sentiment.xlsx"
df = pd.read_excel(INPUT_FILE)
df["temiz_yorum"] = df["temiz_yorum"].fillna("").astype(str)
df["segment"] = df["segment"].fillna(-1).astype(int)
df["sentiment_clean"] = df["sentiment_clean"].fillna("neutral").astype(str)

# ==========================
# 2️⃣ Kelime temizleme fonksiyonu
# ==========================
def get_top_words(texts, top_n=20):
    all_text = " ".join(texts).lower()
    words = re.findall(r'\b\w+\b', all_text)
    stop_words = {"the","a","an","and","or","is","it","to","in","of","this","was","i","you","my","on","for","with","movie","film"}
    filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
    return Counter(filtered_words).most_common(top_n)

# ==========================
# 3️⃣ Genel analiz (tüm yorumlar)
# ==========================
print("🔹 GENEL İZLEYİCİ ORTAK ÖZELLİKLER VE BEKLENTİLER")
top_general = get_top_words(df["temiz_yorum"])
for w, c in top_general:
    print(f"{w}: {c}")

# ==========================
# 4️⃣ Segment bazlı analiz
# ==========================
segments = df["segment"].unique()
for seg in segments:
    seg_df = df[df["segment"] == seg]
    print(f"\n🟢 SEGMENT {seg} ORTAK ÖZELLİKLER VE BEKLENTİLER")
    top_seg = get_top_words(seg_df["temiz_yorum"])
    for w, c in top_seg:
        print(f"{w}: {c}")
