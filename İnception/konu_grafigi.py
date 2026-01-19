import matplotlib.pyplot as plt
import seaborn as sns

# 🎨 Grafik Stili
plt.style.use('ggplot')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# ==========================================
# GİRİLEN VERİLER (senaryokonu.py çıktısı)
# ==========================================

data = {
    "Senaryo Derinliği": 30119,
    "Görsel Efekt": 15660
}

def create_feature_chart():
    print("📊 Senaryo vs Görsel Efekt grafiği oluşturuluyor...")
    plt.figure(figsize=(8, 6))
    
    # Sütun grafiği
    bars = plt.bar(data.keys(), data.values(), color=['#3498db', '#e74c3c'], width=0.5)
    
    # Değerleri yaz
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.title("İzleyicilerin Odaklandığı Alanlar (Bahsedilme Sayısı)", fontsize=14)
    plt.ylabel("Yorum Sayısı")
    plt.ylim(0, max(data.values()) * 1.15)
    plt.tight_layout()
    plt.savefig("ozel_konu_karsilastirma.png")
    print("✅ Kaydedildi: ozel_konu_karsilastirma.png")
    plt.close()

if __name__ == "__main__":
    create_feature_chart()
