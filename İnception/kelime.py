import pandas as pd
from collections import Counter

# ===============================
# 1️⃣ Dosyayı yükle
# ===============================
INPUT_FILE = "yorumlar_sentiment_guncel.xlsx"
df = pd.read_excel(INPUT_FILE)
df["temiz_yorum"] = df["temiz_yorum"].fillna("").astype(str)

# ===============================
# 2️⃣ Kelime listeleri
# ===============================
positive_words = [
    "amazing","great","excellent","masterpiece","brilliant","perfect",
    "love","loved","awesome","incredible","genius","mind blowing",
    "deep","smart","complex","legendary","visual","soundtrack",
    "acting","story","plot","cinematography","nolan"
]

negative_words = [
    "bad","boring","confusing","overrated","terrible","worst",
    "hate","hated","disappointing","weak","mess","too long",
    "slow","predictable","pointless","hard to understand",
    "confused","not good","waste","problem"
]

# ===============================
# 3️⃣ Kelime sayma fonksiyonu
# ===============================
def count_words(texts, keywords):
    counter = Counter()
    for t in texts:
        t = t.lower()
        for w in keywords:
            if w in t:
                counter[w] += 1
    return counter

# ===============================
# 4️⃣ Grupları ayır (VADER etiketine göre)
# ===============================
positive_texts = df[df["vader_label"]=="positive"]["temiz_yorum"]
negative_texts = df[df["vader_label"]=="negative"]["temiz_yorum"]
neutral_texts  = df[df["vader_label"]=="neutral"]["temiz_yorum"]

# ===============================
# 5️⃣ Kelime sayısını al
# ===============================
positive_counts = count_words(positive_texts, positive_words)
negative_counts = count_words(negative_texts, negative_words)
neutral_counts  = count_words(neutral_texts, positive_words + negative_words)

# ===============================
# 6️⃣ Sonuçları göster
# ===============================
print("✨ POSITIVE (VADER) YORUMLARDA KELİME SAYISI")
for k,v in positive_counts.most_common():
    print(k, ":", v)

print("\n💢 NEGATIVE (VADER) YORUMLARDA KELİME SAYISI")
for k,v in negative_counts.most_common():
    print(k, ":", v)

print("\n😐 NEUTRAL (VADER) YORUMLARDA KELİME SAYISI")
for k,v in neutral_counts.most_common():
    print(k, ":", v)
