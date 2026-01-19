import pandas as pd

# ===============================
# DOSYA YOLLARI
# ===============================
excel_1 = "all_comments.xlsx"   # içinde: videoId, author, text, publishedAt
excel_2 = "imdb_yorumlar.xlsx"      # içinde: yorum

# ===============================
# EXCELLERİ OKU
# ===============================
df1 = pd.read_excel(excel_1)
df2 = pd.read_excel(excel_2)

# ===============================
# SADECE GEREKLİ SÜTUNLARI AL
# ===============================
df1_text = df1[["text"]].rename(columns={"text": "yorum"})
df2_text = df2[["yorum"]]

# ===============================
# ALT ALTA BİRLEŞTİR
# ===============================
birlesik_df = pd.concat([df1_text, df2_text], ignore_index=True)

# ===============================
# BOŞ SATIRLARI TEMİZLE
# ===============================
birlesik_df = birlesik_df.dropna()
birlesik_df = birlesik_df[birlesik_df["yorum"].str.strip() != ""]

# ===============================
# YENİ EXCEL'E KAYDET
# ===============================
birlesik_df.to_excel("tum_yorumlar.xlsx", index=False)

print(f"✅ Toplam yorum sayısı: {len(birlesik_df)}")
print("📁 tum_yorumlar.xlsx oluşturuldu")
