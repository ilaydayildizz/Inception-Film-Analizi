import pandas as pd

# Dosyayı oku
df = pd.read_excel("yorumlar_sentiment_hizli.xlsx")

def temizle_sentiment(text):
    if not isinstance(text, str):
        return "neutral"

    t = text.lower()

    if "positive" in t:
        return "positive"
    elif "negative" in t:
        return "negative"
    elif "neutral" in t:
        return "neutral"
    else:
        return "neutral"

# Temizlenmiş sütun
df["sentiment_clean"] = df["sentiment"].apply(temizle_sentiment)

# Kontrol
print(df["sentiment_clean"].value_counts())

# Yeni dosya
df.to_excel("yorumlar_sentiment_temiz.xlsx", index=False)

print("✅ Temizleme tamamlandı → yorumlar_sentiment_temiz.xlsx")
