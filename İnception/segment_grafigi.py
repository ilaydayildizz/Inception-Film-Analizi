import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 🎨 Grafik Stili
plt.style.use('ggplot')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# ==========================================
# GİRİLEN VERİLER (Müşteri Ayrımı Sonuçları)
# ==========================================

# 1. Segment Büyüklükleri
segment_sizes = {
    "Segment 0": 2145,
    "Segment 1": 4545,
    "Segment 2": 52671
}

# 2. Segment Duygu Dağılımları
segment_sentiments = {
    "Segment 0": {"positive": 2118, "negative": 22, "neutral": 5},
    "Segment 1": {"positive": 3894, "negative": 541, "neutral": 110},
    "Segment 2": {"positive": 26949, "negative": 8797, "neutral": 16925}
}

# 3. Segmentlerin En Karakteristik Pozitif Kelimeleri (İlk 5)
segment_top_words = {
    "Segment 0": {"best": 2543, "ever": 871, "one": 610, "time": 307, "movie": 283},
    "Segment 1": {"dream": 9888, "inception": 2356, "nolan": 2026, "cobb": 2015, "reality": 1738},
    "Segment 2": {"like": 5630, "time": 5340, "one": 4791, "inception": 3923, "nolan": 3900}
}

def plot_segment_sizes():
    print("📊 Segment büyüklükleri grafiği oluşturuluyor...")
    plt.figure(figsize=(10, 6))
    
    sns.barplot(x=list(segment_sizes.keys()), y=list(segment_sizes.values()), palette="viridis")
    
    # Değerleri yaz
    for i, v in enumerate(segment_sizes.values()):
        plt.text(i, v, str(v), color='black', ha="center", va="bottom", fontweight='bold')
        
    plt.title("İzleyici Segment Büyüklükleri", fontsize=15)
    plt.ylabel("Kullanıcı Sayısı")
    plt.tight_layout()
    plt.savefig("ozel_segment_boyutlari.png")
    print("✅ Kaydedildi: ozel_segment_boyutlari.png")
    plt.close()

def plot_segment_sentiments():
    print("📊 Segment duygu dağılımı grafiği oluşturuluyor...")
    
    labels = list(segment_sentiments.keys())
    positives = [segment_sentiments[k]["positive"] for k in labels]
    negatives = [segment_sentiments[k]["negative"] for k in labels]
    neutrals = [segment_sentiments[k]["neutral"] for k in labels]
    
    x = np.arange(len(labels))
    width = 0.25
    
    plt.figure(figsize=(12, 7))
    
    # Yan yana barlar
    plt.bar(x - width, positives, width, label='Pozitif', color='#2ecc71')
    plt.bar(x, neutrals, width, label='Nötr', color='#95a5a6')
    plt.bar(x + width, negatives, width, label='Negatif', color='#e74c3c')
    
    plt.xlabel('Segmentler')
    plt.ylabel('Yorum Sayısı')
    plt.title('Segmentlere Göre Duygu Dağılımı', fontsize=15)
    plt.xticks(x, labels)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig("ozel_segment_sentiment_dagilimi.png")
    print("✅ Kaydedildi: ozel_segment_sentiment_dagilimi.png")
    plt.close()

def plot_segment_words():
    print("🔤 Segment kelime grafikleri oluşturuluyor...")
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    colors = ["#3498db", "#9b59b6", "#e67e22"]
    
    for i, (seg, words) in enumerate(segment_top_words.items()):
        ax = axes[i]
        vals = list(words.values())
        keys = list(words.keys())
        
        sns.barplot(x=vals, y=keys, ax=ax, color=colors[i])
        ax.set_title(f"{seg} En Sık Kelimeler")
        ax.set_xlabel("Frekans")
    
    plt.suptitle("Segmentlerin Karakteristik Kelimeleri", fontsize=16)
    plt.tight_layout()
    plt.savefig("ozel_segment_kelimeleri.png")
    print("✅ Kaydedildi: ozel_segment_kelimeleri.png")
    plt.close()

if __name__ == "__main__":
    plot_segment_sizes()
    plot_segment_sentiments()
    plot_segment_words()
