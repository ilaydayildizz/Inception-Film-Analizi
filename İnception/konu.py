import pandas as pd
from collections import Counter
import re

# Dosyayı oku
df = pd.read_excel("yorumlar_sentiment_guncel.xlsx")
df["temiz_yorum"] = df["temiz_yorum"].fillna("").astype(str)

# Tüm yorumları birleştir
all_text = " ".join(df["temiz_yorum"]).lower()

# Kelimeleri parçala
words = re.findall(r'\b\w+\b', all_text)

# Çok kısa veya anlamsız kelimeleri filtrele
stop_words = {"the", "a", "an", "and", "or", "is", "it", "to", "in", "of", "this", "was", "i", "you", "my", "on", "for", "with"}
filtered_words = [w for w in words if w not in stop_words and len(w) > 2]

# En sık geçen kelimeler
top_words = Counter(filtered_words).most_common(30)

print("✨ Kullanıcıların en çok konuştuğu konular / kelimeler:")
for w, c in top_words:
    print(f"{w}: {c}")
