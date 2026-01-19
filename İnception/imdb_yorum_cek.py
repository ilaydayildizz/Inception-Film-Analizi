from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import pandas as pd
import time

URL = "https://www.imdb.com/title/tt1375666/reviews/"
TOPLAM_YORUM = 5903   # IMDb'de görünen sayı

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

print("🌐 IMDb sayfası açılıyor...")
driver.get(URL)
time.sleep(5)

yorumlar = []
onceki_sayi = 0

pbar = tqdm(total=TOPLAM_YORUM, desc="🚀 Yorumlar çekiliyor")

while True:
    # 🔽 Scroll (IMDb yüklemeden DOM'a eklemiyor)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # ✅ DOĞRU SELECTOR
    elements = driver.find_elements(
        By.CSS_SELECTOR,
        'div[data-testid="review-overflow"]'
    )

    # Yeni yorumlar
    for el in elements[onceki_sayi:]:
        text = el.text.strip()
        if text:
            yorumlar.append(text)
            pbar.update(1)

    # Sayıyı güncelle
    if len(elements) == onceki_sayi:
        print("➡️ Yeni yorum yüklenmedi")
    onceki_sayi = len(elements)

    # Load More butonu
    try:
        load_more = driver.find_element(
            By.CSS_SELECTOR,
            'button.ipc-see-more__button'
        )
        driver.execute_script("arguments[0].click();", load_more)
        time.sleep(3)
    except:
        print("➡️ Load More bitti")
        break

driver.quit()
pbar.close()

# ======================
# EXCEL'E KAYDET
# ======================
df = pd.DataFrame({"yorum": yorumlar})
df.to_excel("imdb_yorumlar.xlsx", index=False)

print(f"\n✅ TOPLAM ÇEKİLEN YORUM: {len(yorumlar)}")
print("📁 imdb_yorumlar.xlsx oluşturuldu")
