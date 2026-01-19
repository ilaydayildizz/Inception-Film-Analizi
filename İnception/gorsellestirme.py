import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# 🎨 Grafik Stili ve Ayarlar
plt.style.use('ggplot')
sns.set_palette("husl")
# Türkçe karakter desteği için font ayarı gerekebilir, ancak varsayılan çoğu zaman yeterlidir.
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Dosya Yolu
INPUT_FILE = "yorumlar_sentiment_guncel.xlsx"

def verileri_yukle():
    print("📥 Veriler yükleniyor...")
    df = pd.read_excel(INPUT_FILE)
    df["temiz_yorum"] = df["temiz_yorum"].fillna("").astype(str)
    
    # Vader Label kontrolü
    if "vader_label" not in df.columns:
        print("⚠️ 'vader_label' sütunu bulunamadı, oluşturuluyor...")
        # Basit bir check, normalde bu dosyanın zaten işlenmiş olması beklenir
        df["vader_label"] = "neutral" 
    
    return df

# ==========================================
# 1. DUYGU ANALİZİ GRAFİKLERİ
# ==========================================
def duygu_dagilimi_grafigi(df):
    print("📊 Duygu dağılımı grafiği (VADER) oluşturuluyor...")
    plt.figure(figsize=(10, 6))
    
    counts = df["vader_label"].value_counts()
    colors = {'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#95a5a6'}
    
    # Pasta Grafiği
    plt.pie(counts, labels=counts.index.str.upper(), autopct='%1.1f%%', startangle=140, 
            colors=[colors.get(x, '#34495e') for x in counts.index],
            textprops={'fontsize': 12, 'weight': 'bold'}, explode=[0.05]*len(counts))
    
    plt.title("Yorumların Duygu Dağılımı (VADER Analizi)", fontsize=16)
    plt.tight_layout()
    plt.savefig("duygu_dagilimi_vader.png")
    print("✅ duygu_dagilimi_vader.png kaydedildi.")
    plt.close()

# ==========================================
# 2. KELİME FREKANS GRAFİKLERİ
# ==========================================
def kelime_frekans_grafigi(df):
    print("🔤 Kelime frekans grafikleri oluşturuluyor...")
    
    positive_words = [
        "amazing","great","excellent","masterpiece","brilliant","perfect",
        "love","loved","awesome","incredible","genius","mind blowing",
        "deep","smart","complex","legendary","visual","soundtrack",
        "acting","story","plot","cinematography","nolan"
    ]

    negative_words = [
        "bad","boring","confusing","overrated","terrible","worst",
        "hate","hated","disappointing","weak","mess","too long",
        "slow","predictable","pointless","hard to understand",
        "confused","not good","waste","problem"
    ]
    
    def count_specific_words(texts, keywords):
        counter = Counter()
        for t in texts:
            t = t.lower()
            for w in keywords:
                if w in t:
                    counter[w] += 1
        return counter

    # Pozitif
    pos_texts = df[df["vader_label"] == "positive"]["temiz_yorum"]
    pos_counts = count_specific_words(pos_texts, positive_words)
    
    plt.figure(figsize=(12, 6))
    common_pos = pos_counts.most_common(12)
    sns.barplot(x=[x[1] for x in common_pos], y=[x[0] for x in common_pos], palette="viridis")
    plt.title("Pozitif Yorumlarda En Sık Geçen Kelimeler", fontsize=14)
    plt.xlabel("Frekans")
    plt.tight_layout()
    plt.savefig("pozitif_kelimeler.png")
    print("✅ pozitif_kelimeler.png kaydedildi.")
    plt.close()

    # Negatif
    neg_texts = df[df["vader_label"] == "negative"]["temiz_yorum"]
    neg_counts = count_specific_words(neg_texts, negative_words)

    plt.figure(figsize=(12, 6))
    common_neg = neg_counts.most_common(12)
    sns.barplot(x=[x[1] for x in common_neg], y=[x[0] for x in common_neg], palette="magma")
    plt.title("Negatif Yorumlarda En Sık Geçen Kelimeler", fontsize=14)
    plt.xlabel("Frekans")
    plt.tight_layout()
    plt.savefig("negatif_kelimeler.png")
    print("✅ negatif_kelimeler.png kaydedildi.")
    plt.close()

# ==========================================
# 3. GENEL KONULAR GRAFİĞİ (konu.py)
# ==========================================
def genel_konular_grafigi(df):
    print("🗣️ Genel konular grafiği oluşturuluyor...")
    all_text = " ".join(df["temiz_yorum"]).lower()
    words = re.findall(r'\b\w+\b', all_text)
    stop_words = {"the", "a", "an", "and", "or", "is", "it", "to", "in", "of", "this", "was", "i", "you", "my", "on", "for", "with", "movie", "film", "inception"}
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    
    top_words = Counter(filtered_words).most_common(15)
    
    plt.figure(figsize=(12, 7))
    sns.barplot(x=[x[1] for x in top_words], y=[x[0] for x in top_words], palette="coolwarm")
    plt.title("İzleyicilerin En Çok Konuştuğu Genel Konular", fontsize=15)
    plt.xlabel("Bahsedilme Sayısı")
    plt.tight_layout()
    plt.savefig("genel_konular.png")
    print("✅ genel_konular.png kaydedildi.")
    plt.close()

# ==========================================
# 4. MÜŞTERİ AYRIMI / SEGMENTASYON (müşteri ayrımı.py)
# ==========================================
def segmentasyon_analizi(df):
    print("👥 Müşteri segmentasyonu analizi ve görselleştirme yapılıyor...")
    
    # Basit bir kümeleme yapalım (daha önce analiz edilmiş dosyada segment yoksa)
    if "segment" not in df.columns:
        print("   ⚙️ Segmentasyon hesaplanıyor (K-Means)...")
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        X = vectorizer.fit_transform(df["temiz_yorum"])
        kmeans = KMeans(n_clusters=3, random_state=42)
        df["segment"] = kmeans.fit_predict(X)
    
    # 4.1 Segment Büyüklükleri
    plt.figure(figsize=(8, 6))
    seg_counts = df["segment"].value_counts().sort_index()
    sns.barplot(x=seg_counts.index, y=seg_counts.values, palette="Set2")
    plt.title("İzleyici Segmentlerinin Dağılımı", fontsize=14)
    plt.xlabel("Segment")
    plt.ylabel("Kişi Sayısı")
    plt.xticks(seg_counts.index, [f"Segment {i}" for i in seg_counts.index])
    plt.tight_layout()
    plt.savefig("segment_dagilimi.png")
    print("✅ segment_dagilimi.png kaydedildi.")
    plt.close()
    
    # 4.2 Segment Bazlı Sentiment
    plt.figure(figsize=(10, 6))
    sns.countplot(x="segment", hue="vader_label", data=df, palette="husl")
    plt.title("Segmentlere Göre Duygu Dağılımı", fontsize=14)
    plt.xlabel("Segment")
    plt.ylabel("Yorum Sayısı")
    plt.legend(title="Duygu Durumu")
    plt.tight_layout()
    plt.savefig("segment_sentiment.png")
    print("✅ segment_sentiment.png kaydedildi.")
    plt.close()

# ==========================================
# 5. SENARYO VE KONU ÖZELLİK ANALİZİ (senaryokonu.py)
# ==========================================
def senaryo_konu_analizi(df):
    print("🎬 Senaryo ve konu detay analizi yapılıyor...")
    features = {
        "Senaryo/Hikaye": ["dream", "mind", "plot", "story", "complex", "ending", "reality", "layer"],
        "Görsel/Teknik": ["visual", "cinematography", "music", "soundtrack", "zim-mer", "acting", "nolan", "effect"]
    }
    
    results = []
    
    for category, keywords in features.items():
        # Pozitif Yorumlarda
        pos_df = df[df["vader_label"] == "positive"]
        pos_count = sum(pos_df["temiz_yorum"].str.contains("|".join(keywords), case=False).sum() for kw in keywords) # Basit toplama yerine daha doğru count
        # Daha doğru bir yaklaşım: her kelime için sayıp topla
        pos_total = 0
        neg_total = 0
        
        for k in keywords:
             pos_total += df[df["vader_label"] == "positive"]["temiz_yorum"].str.count(k).sum()
             neg_total += df[df["vader_label"] == "negative"]["temiz_yorum"].str.count(k).sum()
        
        results.append({"Kategori": category, "Duygu": "Pozitif", "Frekans": pos_total})
        results.append({"Kategori": category, "Duygu": "Negatif", "Frekans": neg_total})
        
    res_df = pd.DataFrame(results)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Kategori", y="Frekans", hue="Duygu", data=res_df, palette={"Pozitif": "#2ecc71", "Negatif": "#e74c3c"})
    plt.title("Senaryo ve Teknik Konuların Duygusal Yansıması", fontsize=14)
    plt.ylabel("Bahsedilme Sıklığı")
    plt.tight_layout()
    plt.savefig("senaryo_teknik_analiz.png")
    print("✅ senaryo_teknik_analiz.png kaydedildi.")
    plt.close()

if __name__ == "__main__":
    try:
        df = verileri_yukle()
        
        duygu_dagilimi_grafigi(df)
        kelime_frekans_grafigi(df)
        genel_konular_grafigi(df)
        segmentasyon_analizi(df)
        senaryo_konu_analizi(df)
        
        print("\n🎉 Tüm Gelişmiş Grafikler Başarıyla Oluşturuldu!")
    except Exception as e:
        print(f"❌ Bir hata oluştu: {e}")
