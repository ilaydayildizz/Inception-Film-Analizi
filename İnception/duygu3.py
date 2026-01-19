from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import nltk
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

# -----------------------------
# 1️⃣ Veriyi Oku
# -----------------------------
df = pd.read_excel("yorumlar_sentiment_temiz.xlsx")
df['temiz_yorum'] = df['temiz_yorum'].fillna("").astype(str)

# -----------------------------
# 2️⃣ VADER ile etiketleme
# -----------------------------
def vader_label(text):
    score = sia.polarity_scores(text)['compound']
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

df['vader_label'] = df['temiz_yorum'].apply(vader_label)

# -----------------------------
# 3️⃣ Uyumsuzluk kontrolü ve düzeltme
# -----------------------------
def correct_label(row):
    if row['sentiment_clean'] != row['vader_label']:
        return row['vader_label']  # VADER’a göre düzelt
    return row['sentiment_clean']

df['sentiment_clean'] = df.apply(correct_label, axis=1)

# -----------------------------
# 4️⃣ Kaç yorum değişti?
# -----------------------------
changed = (df['sentiment_clean'] != df['vader_label']).sum()
print(f"⚠️ Toplam {changed} yorum düzeltildi VADER ile.")

# -----------------------------
# 5️⃣ Duygu dağılımı
# -----------------------------
print("\n📊 GÜNCEL DUYGU DAĞILIMI")
counts = df['sentiment_clean'].value_counts()
for label, count in counts.items():
    print(f"{label.upper()}: {count} adet yorum")

# -----------------------------
# 6️⃣ Kaydet
# -----------------------------
df.to_excel("yorumlar_sentiment_guncel.xlsx", index=False)
print("\n✅ Güncelleme tamamlandı. Sonuçlar 'yorumlar_sentiment_guncel.xlsx' dosyasına kaydedildi.")
