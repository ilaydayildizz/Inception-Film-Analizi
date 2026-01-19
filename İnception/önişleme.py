import pandas as pd
import re
import nltk
import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ===============================
# NLTK SETUP
# ===============================
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Film için anlamsal katkısı düşük kelimeler
domain_stopwords = {"movie", "film"}

def on_isleme(metin):
    if pd.isna(metin) or len(str(metin).strip()) < 2:
        return ""

    metin = str(metin)

    # 1️⃣ Emoji temizleme
    metin = emoji.replace_emoji(metin, replace=" ")

    # 2️⃣ URL / mention / hashtag temizleme
    metin = re.sub(r"http\S+|www\.\S+", " ", metin)
    metin = re.sub(r"[@#]\w+", " ", metin)

    # 3️⃣ Küçük harf
    metin = metin.lower()

    # 4️⃣ Negatif yapıları koru (ÇOK ÖNEMLİ)
    metin = re.sub(r'\bnot (\w+)\b', r'not_\1', metin)

    # 5️⃣ Noktalama & sayı temizleme
    metin = re.sub(r'[^\w\s]', ' ', metin)
    metin = re.sub(r'\d+', ' ', metin)

    # 6️⃣ ASCII dışı karakterleri sil
    metin = metin.encode("utf-8", "ignore").decode("ascii", "ignore")

    # 7️⃣ Stopword + Lemmatization
    kelimeler = metin.split()
    temiz_kelimeler = [
        lemmatizer.lemmatize(k)
        for k in kelimeler
        if k not in stop_words and k not in domain_stopwords
    ]

    metin = " ".join(temiz_kelimeler)

    # 8️⃣ Boşluk düzenleme
    metin = re.sub(r'\s+', ' ', metin).strip()

    return metin


# ===============================
# ANA İŞLEM
# ===============================
print("📥 Excel yükleniyor...")
df = pd.read_excel("tum_yorumlar_translated_en.xlsx")

print("🧹 Ön işleme uygulanıyor...")
df["temiz_yorum"] = df["yorum_english"].apply(on_isleme)

# Çok kısa / anlamsız yorumları sil
df = df[df["temiz_yorum"].str.split().str.len() > 1]

print("💾 Kaydediliyor...")
df.to_excel("temizlenmis_yorumlar_final.xlsx", index=False)

print("🎉 Bitti! Analize %100 hazır.")
