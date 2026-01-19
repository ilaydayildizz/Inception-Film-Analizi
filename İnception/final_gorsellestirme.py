import matplotlib.pyplot as plt
import seaborn as sns

# 🎨 Grafik Stili
plt.style.use('ggplot')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# ==========================================
# 1. VERİLER (Kullanıcı tarafından sağlanan)
# ==========================================

# Duygu Dağılımı (VADER)
sentiment_counts = {
    "Positive": 32961,
    "Neutral": 17040,
    "Negative": 9360
}

# Pozitif Kelimeler (VADER) - En Çok Geçenler
positive_words = {
    "nolan": 3552, "great": 3211, "love": 3143, "story": 2208,
    "masterpiece": 1818, "amazing": 1717, "perfect": 1430, "plot": 1201,
    "soundtrack": 1110, "acting": 965, "visual": 842, "deep": 833
}

# Negatif Kelimeler (VADER)
negative_words = {
    "bad": 338, "hate": 270, "problem": 110, "boring": 91,
    "worst": 83, "mess": 83, "waste": 76, "slow": 74,
    "confused": 73, "confusing": 59
}

# Segmentasyon Verileri
segments = {
    "Segment 0 (Hayranlar)": 2145,
    "Segment 1 (Teorisyenler)": 4545,
    "Segment 2 (Genel İzleyici)": 52671
}

# Segment Sentiment Dağılımları (Yaklaşık oranlar veya net sayılar)
# Segment 0: 2118 Pos, 22 Neg, 5 Neu
# Segment 1: 3894 Pos, 541 Neg, 110 Neu
# Segment 2: 26949 Pos, 8797 Neg, 16925 Neu
segment_sentiments = {
    "Hayranlar": [2118, 22, 5],      # Pos, Neg, Neu
    "Teorisyenler": [3894, 541, 110],
    "Genel İzleyici": [26949, 8797, 16925]
}

# Konu / Özellik Karşılaştırması (konu.py çıktısı)
features_scores = {
    "Senaryo Derinliği": 30119,
    "Görsel Efekt": 15660
}

# Senaryo/Teknik Olumlu-Olumsuz Dağılımı (Yaklaşık toplamlardan çıkarım)
# Senaryo (Positive): ~20,000 kelime, (Negative): ~3,000
# Görsel (Positive): ~12,000 kelime, (Negative): ~1,500
feature_sentiment = {
    "Kategori": ["Senaryo/Hikaye", "Senaryo/Hikaye", "Görsel/Teknik", "Görsel/Teknik"],
    "Duygu": ["Pozitif", "Negatif", "Pozitif", "Negatif"],
    "Frekans": [21000, 3000, 12000, 1500] 
}


# ==========================================
# 2. GRAFİK OLUŞTURMA FONKSİYONLARI
# ==========================================

def plot_sentiment():
    print("📊 Duygu dağılımı (VADER) oluşturuluyor...")
    plt.figure(figsize=(10, 6))
    colors = ['#2ecc71', '#95a5a6', '#e74c3c'] # Pos, Neu, Neg
    
    # Bar Chart'a dönüştürüldü
    sns.barplot(x=list(sentiment_counts.keys()), y=list(sentiment_counts.values()), palette=colors)
            
    plt.title("Genel Duygu Dağılımı (VADER)", fontsize=16)
    plt.xlabel("Duygu Durumu")
    plt.ylabel("Yorum Sayısı")
    plt.tight_layout()
    plt.savefig("duygu_dagilimi_final.png")
    plt.close()

def plot_words():
    print("🔤 Kelime grafikleri oluşturuluyor...")
    
    # Pozitif
    plt.figure(figsize=(12, 6))
    keys = list(positive_words.keys())
    vals = list(positive_words.values())
    sns.barplot(x=vals, y=keys, palette="viridis")
    plt.title("Pozitif Yorumlarda En Sık Kullanılan Kelimeler", fontsize=14)
    plt.xlabel("Frekans")
    plt.tight_layout()
    plt.savefig("pozitif_kelimeler_final.png")
    plt.close()

    # Negatif
    plt.figure(figsize=(12, 6))
    keys = list(negative_words.keys())
    vals = list(negative_words.values())
    sns.barplot(x=vals, y=keys, palette="magma")
    plt.title("Negatif Yorumlarda En Sık Kullanılan Kelimeler", fontsize=14)
    plt.xlabel("Frekans")
    plt.tight_layout()
    plt.savefig("negatif_kelimeler_final.png")
    plt.close()

def plot_segments():
    print("👥 Segmentasyon grafikleri oluşturuluyor...")
    
    # Bar Chart (Segment Boyutları) - Pasta grafiği yerine
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(segments.keys()), y=list(segments.values()), palette="Set2")
    plt.title("İzleyici Segment Dağılımı", fontsize=15)
    plt.xlabel("Segmentler")
    plt.ylabel("Kullanıcı Sayısı")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("segment_dagilimi_final.png")
    plt.close()

    # Stacked Bar (Segment Sentiment)
    import numpy as np
    labels = list(segment_sentiments.keys())
    positives = [v[0] for v in segment_sentiments.values()]
    negatives = [v[1] for v in segment_sentiments.values()]
    neutrals = [v[2] for v in segment_sentiments.values()]
    
    x = np.arange(len(labels))
    width = 0.5
    
    plt.figure(figsize=(10, 6))
    plt.bar(x, positives, width, label='Pozitif', color='#2ecc71')
    plt.bar(x, neutrals, width, bottom=positives, label='Nötr', color='#95a5a6')
    plt.bar(x, negatives, width, bottom=np.array(positives)+np.array(neutrals), label='Negatif', color='#e74c3c')
    
    plt.xlabel('Segmentler')
    plt.ylabel('Yorum Sayısı')
    plt.title('Segmentlere Göre Duygu Dağılımı')
    plt.xticks(x, labels)
    plt.legend()
    plt.tight_layout()
    plt.savefig("segment_sentiment_final.png")
    plt.close()

def plot_features():
    print("🎬 Özellik karşılaştırma grafikleri oluşturuluyor...")
    
    # Genel Özellik Skoru
    plt.figure(figsize=(8, 6))
    sns.barplot(x=list(features_scores.keys()), y=list(features_scores.values()), palette="coolwarm")
    plt.title("İzleyicilerin Odaklandığı Alanlar (Kelime Sıklığı)", fontsize=14)
    plt.ylabel("Frekans")
    plt.tight_layout()
    plt.savefig("konu_karsilastirma_final.png")
    plt.close()


if __name__ == "__main__":
    plot_sentiment()
    plot_words()
    plot_segments()
    plot_features()
    print("✅ Tüm grafikler (final) oluşturuldu.")
