import matplotlib.pyplot as plt
import seaborn as sns

# 🎨 Grafik Stili
plt.style.use('ggplot')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# ==========================================
# GİRİLEN VERİLER (beklenti.py çıktısı)
# ==========================================

genel_beklenti = {
    "dream": 12211, "time": 9663, "one": 8455, "like": 8145, "inception": 7609,
    "nolan": 7065, "music": 5880, "make": 5056, "best": 5025, "life": 4480,
    "song": 4408, "think": 4373, "zimmer": 4363, "people": 4091, "know": 4026,
    "han": 3904, "good": 3893, "see": 3869, "get": 3692, "cobb": 3642
}

segment2_beklenti = {
    "time": 7906, "like": 6453, "one": 6136, "music": 5447, "inception": 4992,
    "nolan": 4727, "song": 4161, "make": 3970, "zimmer": 3859, "life": 3660,
    "han": 3457, "think": 3340, "good": 3308, "people": 3170, "know": 3161,
    "love": 2976, "great": 2960, "get": 2864, "see": 2784, "watch": 2728
}

segment1_beklenti = {
    "dream": 10728, "inception": 2414, "cobb": 2242, "nolan": 2077, "reality": 1965,
    "one": 1706, "like": 1619, "time": 1446, "real": 1373, "world": 1348,
    "mind": 1241, "idea": 1103, "see": 1029, "make": 1027, "think": 968,
    "scene": 965, "character": 921, "end": 911, "totem": 907, "people": 894
}

segment0_beklenti = {
    "best": 2577, "ever": 876, "one": 613, "time": 311, "zimmer": 281,
    "nolan": 261, "music": 260, "han": 244, "seen": 211, "inception": 203,
    "soundtrack": 192, "ending": 167, "song": 161, "made": 161, "christopher": 109,
    "life": 93, "director": 88, "still": 80, "love": 78, "world": 74
}

def create_bar_chart(data, title, filename, color_palette="viridis"):
    print(f"📊 {title} grafiği oluşturuluyor...")
    
    # Verileri sırala
    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    keys = [x[0] for x in sorted_items]
    vals = [x[1] for x in sorted_items]
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x=vals, y=keys, palette=color_palette)
    
    plt.title(title, fontsize=15)
    plt.xlabel("Frekans")
    plt.ylabel("Kelimeler")
    plt.tight_layout()
    plt.savefig(filename)
    print(f"✅ Kaydedildi: {filename}")
    plt.close()

if __name__ == "__main__":
    create_bar_chart(genel_beklenti, "Genel İzleyici Ortak Özellikler ve Beklentiler", "ozel_beklenti_genel.png", "mako")
    create_bar_chart(segment0_beklenti, "Segment 0 (Hayranlar): Ortak Özellikler ve Beklentiler", "ozel_beklenti_seg0.png", "rocket")
    create_bar_chart(segment1_beklenti, "Segment 1 (Teorisyenler): Ortak Özellikler ve Beklentiler", "ozel_beklenti_seg1.png", "viridis")
    create_bar_chart(segment2_beklenti, "Segment 2 (Genel): Ortak Özellikler ve Beklentiler", "ozel_beklenti_seg2.png", "magma")
