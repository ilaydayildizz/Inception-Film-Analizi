import pandas as pd
import time
from deep_translator import GoogleTranslator

# =========================
# EXCEL DOSYASINI OKU
# =========================
df = pd.read_excel("tum_yorumlar_with_language.xlsx")

translator = GoogleTranslator(source="auto", target="en")

total = len(df)
start_time = time.time()

def translate_if_needed(text, language):
    try:
        if pd.isna(text) or len(str(text).strip()) < 2:
            return ""

        # Zaten İngilizceyse çevirme
        if language == "en":
            return text

        # Dil tespit edilemediyse (emoji vs.)
        if language == "unknown":
            return ""

        # İngilizce olmayanları çevir
        return translator.translate(text)

    except Exception:
        return ""

translated_texts = []

for i, row in enumerate(df.itertuples(index=False), start=1):
    translated_texts.append(
        translate_if_needed(row.yorum, row.language)
    )

    # -------- İLERLEME ÇIKTISI --------
    elapsed = time.time() - start_time
    avg_per_item = elapsed / i
    remaining = avg_per_item * (total - i)
    percent = (i / total) * 100

    print(
        f"\r🔄 {i}/{total} (%{percent:.2f}) | "
        f"Geçen: {elapsed/60:.1f} dk | "
        f"Kalan: {remaining/60:.1f} dk",
        end=""
    )

    # Google ban riskine karşı yavaşlat
    if row.language != "en" and i % 20 == 0:
        time.sleep(1)

print()  # satır atlat

# =========================
# YENİ SÜTUN EKLE & KAYDET
# =========================
df["yorum_english"] = translated_texts

df.to_excel("tum_yorumlar_translated_en.xlsx", index=False)

print("✅ İngilizce dışındaki tüm yorumlar İngilizceye çevrildi.")
print("📁 tum_yorumlar_translated_en.xlsx oluşturuldu")
