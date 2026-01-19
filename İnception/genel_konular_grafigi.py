import matplotlib.pyplot as plt
import seaborn as sns

# 🎨 Grafik Stili
plt.style.use('ggplot')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# ==========================================
# GİRİLEN VERİLER (Kullanıcı tarafından sağlanan)
# ==========================================

topic_data = {
    "dream": 12211,
    "time": 9663,
    "one": 8455,
    "like": 8145,
    "inception": 7609,
    "nolan": 7065,
    "music": 5880,
    "make": 5056,
    "best": 5025,
    "life": 4480,
    "song": 4408,
    "think": 4373,
    "zimmer": 4363,
    "people": 4091,
    "know": 4026,
    "han": 3904,
    "good": 3893,
    "see": 3869,
    "get": 3692,
    "cobb": 3642,
    "great": 3570,
    "world": 3535,
    "mind": 3385,
    "really": 3368,
    "still": 3366,
    "love": 3356,
    "would": 3314,
    "watch": 3238,
    "ever": 3199,
    "reality": 3179
}

def create_topic_chart():
    print("📊 Genel konular grafiği oluşturuluyor...")
    
    # Verileri sırala (En çoktan en aza)
    sorted_items = sorted(topic_data.items(), key=lambda x: x[1], reverse=True)
    keys = [x[0] for x in sorted_items]
    vals = [x[1] for x in sorted_items]
    
    # Grafik Boyutu (Veri çok olduğu için yüksek yapıyoruz)
    plt.figure(figsize=(12, 12))
    
    # Yatay Bar Grafiği (Daha okunaklı olması için)
    sns.barplot(x=vals, y=keys, palette="viridis")
    
    plt.title("Kullanıcıların En Çok Konuştuğu Konular / Kelimeler", fontsize=16)
    plt.xlabel("Frekans", fontsize=12)
    plt.ylabel("Kelimeler", fontsize=12)
    plt.tight_layout()
    plt.savefig("ozel_genel_konular.png")
    print("✅ Kaydedildi: ozel_genel_konular.png")
    plt.close()

if __name__ == "__main__":
    create_topic_chart()
