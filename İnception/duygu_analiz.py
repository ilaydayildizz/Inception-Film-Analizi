import pandas as pd
import requests
import time
from collections import Counter
import os

# =====================================================
# 1️⃣ LM STUDIO AYARLARI
# =====================================================
LM_URL = "http://192.168.22.1:1234/v1/chat/completions"
MODEL_NAME = "meta-llama-3-8b-instruct"

INPUT_FILE = "temizlenmis_yorumlar_final.xlsx"
OUTPUT_FILE = "yorumlar_sentiment_hizli.xlsx"
CHECKPOINT_FILE = "checkpoint_sentiment.csv"

SAVE_EVERY = 500      # kaç yorumda bir kaydedilsin
LLM_LIMIT = 0.08      # sadece %8 yoruma LLM

# =====================================================
# 2️⃣ VERİYİ OKU
# =====================================================
print("📥 Veri yükleniyor...")
df = pd.read_excel(INPUT_FILE)
df["text"] = df["temiz_yorum"].fillna("").astype(str)

# checkpoint varsa devam et
if os.path.exists(CHECKPOINT_FILE):
    print("♻️ Kayıttan devam ediliyor...")
    saved = pd.read_csv(CHECKPOINT_FILE)
    df.loc[:len(saved)-1, "sentiment"] = saved["sentiment"]
    start_index = len(saved)
else:
    df["sentiment"] = ""
    start_index = 0

total = len(df)

# =====================================================
# 3️⃣ KELİME LİSTELERİ
# =====================================================
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

# =====================================================
# 4️⃣ KURAL TABANLI PUANLAMA
# =====================================================
def score_label(text):
    t = text.lower()
    pos = sum(w in t for w in positive_words)
    neg = sum(w in t for w in negative_words)

    if pos - neg >= 2:
        return "positive"
    if neg - pos >= 2:
        return "negative"
    return "check"

# =====================================================
# 5️⃣ LLaMA KARAR (SADECE AZ YORUM)
# =====================================================
def llama_decide(text):
    prompt = f"""
Classify the sentiment of the following movie comment.
Choose ONLY one word: positive, negative, neutral.

Comment:
{text}
"""
    try:
        r = requests.post(
            LM_URL,
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0,
                "max_tokens": 5
            },
            timeout=20
        )
        return r.json()["choices"][0]["message"]["content"].strip().lower()
    except:
        return "neutral"

# =====================================================
# 6️⃣ ANALİZ BAŞLIYOR
# =====================================================
print("🚀 Hızlı analiz başlıyor...\n")

llm_used = 0
llm_max = int(total * LLM_LIMIT)

for i in range(start_index, total):
    text = df.at[i, "text"]
    label = score_label(text)

    if label == "check" and llm_used < llm_max:
        label = llama_decide(text)
        llm_used += 1

    if label == "check":
        label = "neutral"

    df.at[i, "sentiment"] = label

    # ilerleme
    if (i+1) % 100 == 0:
        kalan = total - (i+1)
        print(f"İlerleme: {i+1}/{total} | Kalan: {kalan}")

    # checkpoint
    if (i+1) % SAVE_EVERY == 0:
        df.iloc[:i+1][["sentiment"]].to_csv(CHECKPOINT_FILE, index=False)

# =====================================================
# 7️⃣ KAYDET
# =====================================================
df.to_excel(OUTPUT_FILE, index=False)
print("\n✅ ANALİZ TAMAMLANDI")
print(f"📁 Kaydedildi: {OUTPUT_FILE}")

# =====================================================
# 8️⃣ EN ÇOK BEĞENİLEN / BEĞENİLMEYEN
# =====================================================
def extract_topics(texts, keywords, top_n=10):
    found = []
    for t in texts:
        t = t.lower()
        for w in keywords:
            if w in t:
                found.append(w)
    return Counter(found).most_common(top_n)

print("\n📊 SENTIMENT DAĞILIMI")
print(df["sentiment"].value_counts())

print("\n✨ EN ÇOK BEĞENİLENLER")
print(extract_topics(df[df.sentiment=="positive"]["text"], positive_words))

print("\n💢 EN ÇOK BEĞENİLMEYENLER")
print(extract_topics(df[df.sentiment=="negative"]["text"], negative_words))

print("\n😐 KARARSIZ KALINAN NOKTALAR")
print(extract_topics(df[df.sentiment=="neutral"]["text"], positive_words + negative_words))
