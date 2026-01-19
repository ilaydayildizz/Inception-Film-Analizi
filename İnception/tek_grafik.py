import matplotlib.pyplot as plt
import seaborn as sns

# 🎨 Grafik Stili
plt.style.use('ggplot')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# ==========================================
# İSTENEN VERİLER
# ==========================================
sentiment_counts = {
    "Positive": 32961,
    "Neutral": 17040,
    "Negative": 9360
}

def ozel_grafik_olustur():
    print("📊 İstenen özel grafik oluşturuluyor...")
    
    plt.figure(figsize=(10, 7))
    colors = ['#2ecc71', '#95a5a6', '#e74c3c'] # Pos, Neu, Neg
    
    # Sütun Grafiği (Bar Chart)
    bars = plt.bar(sentiment_counts.keys(), sentiment_counts.values(), color=colors, width=0.6)
    
    # Değerleri sütunların üzerine yaz
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.title("Yorumların Duygu Durumu Dağılımı", fontsize=16, pad=20)
    plt.xlabel("Duygu Durumu", fontsize=12)
    plt.ylabel("Yorum Sayısı", fontsize=12)
    plt.ylim(0, max(sentiment_counts.values()) * 1.1) # Üstten biraz boşluk bırak
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    output_file = "ozel_duygu_grafigi.png"
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"✅ Grafik başarıyla kaydedildi: {output_file}")
    plt.close()

if __name__ == "__main__":
    ozel_grafik_olustur()
