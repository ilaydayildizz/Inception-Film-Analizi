import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

# ==========================
# 1️⃣ Veriyi oku
# ==========================
INPUT_FILE = "yorumlar_sentiment_guncel.xlsx"
OUTPUT_FILE = "yorumlar_segmented_sentiment.xlsx"

df = pd.read_excel(INPUT_FILE)
df["temiz_yorum"] = df["temiz_yorum"].fillna("").astype(str)
df["vader_label"] = df["vader_label"].fillna("neutral").astype(str)

# Kullanıcı sütunu yoksa yorum indeksini kullanıcı varsay
if 'kullanici_id' not in df.columns:
    df['kullanici_id'] = df.index

# ==========================
# 2️⃣ TF-IDF ile vektörle
# ==========================
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X = vectorizer.fit_transform(df["temiz_yorum"])

# ==========================
# 3️⃣ Kümeleme (segmentasyon)
# ==========================
k = 3  # segment sayısı
kmeans = KMeans(n_clusters=k, random_state=42)
df["segment"] = kmeans.fit_predict(X)

# ==========================
# 4️⃣ Segment bazlı sentiment ve kelime analizi
# ==========================
segment_summary = []

for i in range(k):
    seg_df = df[df["segment"] == i]
    sentiment_counts = seg_df["vader_label"].value_counts()
    
    positive_texts = seg_df[seg_df["vader_label"]=="positive"]["temiz_yorum"].tolist()
    negative_texts = seg_df[seg_df["vader_label"]=="negative"]["temiz_yorum"].tolist()
    neutral_texts  = seg_df[seg_df["vader_label"]=="neutral"]["temiz_yorum"].tolist()
    
    def top_words(texts, top_n=10):
        all_words = " ".join(texts).lower().split()
        return Counter(all_words).most_common(top_n)
    
    top_positive = top_words(positive_texts)
    top_negative = top_words(negative_texts)
    top_neutral  = top_words(neutral_texts)
    
    unique_users = seg_df["kullanici_id"].nunique()
    
    segment_summary.append({
        "segment": i,
        "size": len(seg_df),
        "unique_users": unique_users,
        "sentiment_counts": sentiment_counts.to_dict(),
        "top_positive": top_positive,
        "top_negative": top_negative,
        "top_neutral": top_neutral
    })

# ==========================
# 5️⃣ Sonuçları yazdır
# ==========================
for s in segment_summary:
    print(f"\n🟢 Segment {s['segment']} ({s['size']} yorum, {s['unique_users']} kullanıcı)")
    print("Sentiment dağılımı:", s["sentiment_counts"])
    print("✨ En çok beğenilen kelimeler:", s["top_positive"])
    print("💢 En çok beğenilmeyen kelimeler:", s["top_negative"])
    print("😐 Kararsız kalınan kelimeler:", s["top_neutral"])

# ==========================
# 6️⃣ Segment bilgilerini kaydet
# ==========================
df.to_excel(OUTPUT_FILE, index=False)
print(f"\n✅ Segmentasyon ve sentiment özetleri kaydedildi: {OUTPUT_FILE}")
