import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 🎨 Grafik Stili
plt.style.use('ggplot')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# ==========================================
# GİRİLEN VERİLER (senaryokonu.py detay çıktısı)
# ==========================================

# 1. SENARYO DERİNLİĞİ VERİLERİ
senaryo_data = [
    # Olumsuz
    {"Word": "end", "Count": 966, "Sentiment": "Negatif"},
    {"Word": "dream", "Count": 806, "Sentiment": "Negatif"},
    {"Word": "mind", "Count": 360, "Sentiment": "Negatif"},
    {"Word": "inception", "Count": 357, "Sentiment": "Negatif"},
    {"Word": "reality", "Count": 312, "Sentiment": "Negatif"},
    {"Word": "cobb", "Count": 285, "Sentiment": "Negatif"},
    {"Word": "story", "Count": 162, "Sentiment": "Negatif"},
    {"Word": "plot", "Count": 85, "Sentiment": "Negatif"},
    {"Word": "complex", "Count": 31, "Sentiment": "Negatif"},
    # Olumlu
    {"Word": "dream", "Count": 5425, "Sentiment": "Pozitif"},
    {"Word": "end", "Count": 5416, "Sentiment": "Pozitif"},
    {"Word": "inception", "Count": 3338, "Sentiment": "Pozitif"},
    {"Word": "mind", "Count": 2211, "Sentiment": "Pozitif"},
    {"Word": "story", "Count": 2208, "Sentiment": "Pozitif"},
    {"Word": "reality", "Count": 1743, "Sentiment": "Pozitif"},
    {"Word": "cobb", "Count": 1655, "Sentiment": "Pozitif"},
    {"Word": "plot", "Count": 1201, "Sentiment": "Pozitif"},
    {"Word": "complex", "Count": 779, "Sentiment": "Pozitif"}
]

# 2. GÖRSEL EFEKT VERİLERİ
gorsel_data = [
    # Olumsuz
    {"Word": "music", "Count": 569, "Sentiment": "Negatif"},
    {"Word": "nolan", "Count": 287, "Sentiment": "Negatif"},
    {"Word": "scene", "Count": 263, "Sentiment": "Negatif"},
    {"Word": "soundtrack", "Count": 107, "Sentiment": "Negatif"},
    {"Word": "acting", "Count": 49, "Sentiment": "Negatif"},
    {"Word": "visual", "Count": 19, "Sentiment": "Negatif"},
    {"Word": "cinematography", "Count": 6, "Sentiment": "Negatif"},
    # Olumlu
    {"Word": "music", "Count": 3695, "Sentiment": "Pozitif"},
    {"Word": "nolan", "Count": 3552, "Sentiment": "Pozitif"},
    {"Word": "scene", "Count": 1665, "Sentiment": "Pozitif"},
    {"Word": "soundtrack", "Count": 1110, "Sentiment": "Pozitif"},
    {"Word": "acting", "Count": 965, "Sentiment": "Pozitif"},
    {"Word": "visual", "Count": 842, "Sentiment": "Pozitif"},
    {"Word": "cinematography", "Count": 379, "Sentiment": "Pozitif"},
    {"Word": "effects", "Count": 1, "Sentiment": "Pozitif"}
]

def plot_grouped_bar(data_list, title, filename):
    print(f"📊 {title} grafiği oluşturuluyor...")
    df = pd.DataFrame(data_list)
    
    plt.figure(figsize=(12, 7))
    
    # Grouped Bar Plot
    # Pozitif ve Negatif renkleri
    palette = {"Pozitif": "#2ecc71", "Negatif": "#e74c3c"}
    
    sns.barplot(data=df, x="Word", y="Count", hue="Sentiment", palette=palette)
    
    plt.title(title, fontsize=16)
    plt.xlabel("Kelimeler", fontsize=12)
    plt.ylabel("Frekans", fontsize=12)
    plt.legend(title="Duygu Durumu")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(filename)
    print(f"✅ Kaydedildi: {filename}")
    plt.close()

if __name__ == "__main__":
    plot_grouped_bar(senaryo_data, "Senaryo Derinliği: Kelimelerin Duygusal Dağılımı", "ozel_senaryo_detay.png")
    plot_grouped_bar(gorsel_data, "Görsel Efektler: Kelimelerin Duygusal Dağılımı", "ozel_gorsel_detay.png")
