import matplotlib.pyplot as plt
import seaborn as sns

# 🎨 Grafik Stili
plt.style.use('ggplot')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# ==========================================
# GİRİLEN VERİLER (TAM LİSTE)
# ==========================================

positive_words = {
    "nolan": 3552, "great": 3211, "love": 3143, "story": 2208,
    "masterpiece": 1818, "amazing": 1717, "perfect": 1430, "plot": 1201,
    "soundtrack": 1110, "acting": 965, "visual": 842, "deep": 833,
    "complex": 779, "brilliant": 732, "awesome": 662, "genius": 602,
    "loved": 463, "incredible": 455, "excellent": 404, "cinematography": 379,
    "smart": 272, "mind blowing": 229, "legendary": 77
}

negative_words = {
    "bad": 338, "hate": 270, "problem": 110, "boring": 91,
    "worst": 83, "mess": 83, "waste": 76, "slow": 74,
    "confused": 73, "confusing": 59, "weak": 49, "terrible": 39,
    "hated": 30, "overrated": 27, "pointless": 22, "disappointing": 9,
    "predictable": 6, "too long": 2
}

neutral_words = {
    "nolan": 549, "soundtrack": 265, "genius": 207, "story": 137,
    "deep": 126, "incredible": 96, "slow": 43, "plot": 38,
    "legendary": 37, "overrated": 31, "mess": 29, "acting": 28,
    "love": 27, "mind blowing": 27, "hate": 26, "great": 25,
    "bad": 24, "complex": 19, "visual": 12, "amazing": 10,
    "awesome": 9, "waste": 9, "problem": 8, "pointless": 6,
    "perfect": 5, "boring": 5, "cinematography": 5, "loved": 4,
    "smart": 4, "confusing": 4, "masterpiece": 4, "predictable": 3,
    "hated": 2, "worst": 2, "weak": 2, "excellent": 2,
    "confused": 2, "disappointing": 1, "terrible": 1
}

def create_bar_chart(data, title, color_palette, filename):
    print(f"📊 {title} oluşturuluyor...")
    # Veri sayısı çok olduğu için boyutu biraz büyütelim
    plt.figure(figsize=(14, 8))
    
    # Verileri sırala
    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    keys = [x[0] for x in sorted_items]
    vals = [x[1] for x in sorted_items]
    
    # Grafik Çiz
    sns.barplot(x=vals, y=keys, palette=color_palette)
    
    plt.title(title, fontsize=16)
    plt.xlabel("Frekans", fontsize=12)
    plt.yticks(fontsize=10) # Kelimeler çok olduğu için fontu biraz küçültelim
    plt.tight_layout()
    plt.savefig(filename)
    print(f"✅ Kaydedildi: {filename}")
    plt.close()

if __name__ == "__main__":
    create_bar_chart(positive_words, "Pozitif Yorumlarda En Çok Geçen Kelimeler (Tam Liste)", "viridis", "kelime_pozitif_manual.png")
    create_bar_chart(negative_words, "Negatif Yorumlarda En Çok Geçen Kelimeler (Tam Liste)", "magma", "kelime_negatif_manual.png")
    create_bar_chart(neutral_words, "Nötr Yorumlarda En Çok Geçen Kelimeler (Tam Liste)", "cividis", "kelime_notr_manual.png")
