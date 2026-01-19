import requests
import pandas as pd
import time
import json
from pathlib import Path

# ================== API KEY LİSTESİ ==================
API_KEYS = [
    "AIzaSyCgjb9uIybJh5NaeHf9_GR55LTpFKFFetE",
    "AIzaSyBHrm9S9DDMBiWpxRiu8HZSVWhVC5f2auQ",
    "AIzaSyC69uFuYWmOhvnuD7q9lDJW3VECaxQvtBw"
]
api_index = 0

def get_api_key():
    return API_KEYS[api_index]

def rotate_api_key():
    global api_index
    api_index += 1
    if api_index >= len(API_KEYS):
        raise RuntimeError("❌ Tüm API key'lerin kotası doldu!")
    print(f"🔁 Yeni API KEY'e geçildi (index={api_index})")

# ================== VIDEO AYRIMI ==================
# ❌ Bunlar API'den tekrar çekilmeyecek
SKIP_FETCH_VIDEOS = [
    "RxabLA7UQ9k",
    "YoHD9XEInc0"
]

# ✅ Sadece bunun yorumları çekilecek
FETCH_VIDEOS = [
    "XQPy88-E2zo"
]

# ================== AYARLAR ==================
MAX_RESULTS = 100
SLEEP_TIME = 0.5
MAX_RETRIES = 5
TIMEOUT = 15

session = requests.Session()

# ================== YARDIMCI ==================
def fetch_json(url, params):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            params["key"] = get_api_key()
            r = session.get(url, params=params, timeout=TIMEOUT)
            data = r.json()

            if "error" in data:
                reason = data["error"]["errors"][0]["reason"]
                if reason == "quotaExceeded":
                    rotate_api_key()
                    continue
                else:
                    raise RuntimeError(data)

            r.raise_for_status()
            return data

        except Exception as e:
            wait = 2 ** attempt
            print(f"Hata ({attempt}/{MAX_RETRIES}): {e} → {wait}s bekleniyor")
            time.sleep(wait)

    return {}

def append_to_csv(rows, path):
    if not rows:
        return
    df = pd.DataFrame(rows)
    if not Path(path).exists():
        df.to_csv(path, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(path, mode="a", header=False, index=False, encoding="utf-8-sig")

def save_state(path, token, total):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "nextPageToken": token,
                "total_fetched": total
            },
            f,
            ensure_ascii=False,
            indent=2
        )

def load_state(path):
    if not Path(path).exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ================== YOUTUBE API ==================
def fetch_comment_threads(video_id, token=None):
    return fetch_json(
        "https://www.googleapis.com/youtube/v3/commentThreads",
        {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": MAX_RESULTS,
            "pageToken": token,
            "textFormat": "plainText"
        }
    )

def fetch_replies(parent_id, token=None):
    return fetch_json(
        "https://www.googleapis.com/youtube/v3/comments",
        {
            "part": "snippet",
            "parentId": parent_id,
            "maxResults": MAX_RESULTS,
            "pageToken": token,
            "textFormat": "plainText"
        }
    )

# ================== SADECE SON VIDEOYU ÇEK ==================
def collect_video_comments(video_id):
    csv_path = f"{video_id}_comments.csv"
    state_path = f"{video_id}_state.json"

    state = load_state(state_path)

    # Video daha önce tamamen bittiyse tekrar çekme
    if state and state.get("nextPageToken") is None and state.get("total_fetched", 0) > 0:
        print(f"⏭ {video_id} zaten tamamlanmış, atlanıyor")
        return

    next_token = state.get("nextPageToken") if state else None
    total = state.get("total_fetched", 0) if state else 0

    print(f"\n🎬 Yorum çekiliyor: {video_id}")

    while True:
        data = fetch_comment_threads(video_id, next_token)
        items = data.get("items", [])

        if not items:
            break

        rows = []

        for item in items:
            top = item["snippet"]["topLevelComment"]["snippet"]
            rows.append({
                "videoId": video_id,
                "author": top["authorDisplayName"],
                "text": top["textDisplay"],
                "publishedAt": top["publishedAt"]
            })
            total += 1

            parent_id = item["snippet"]["topLevelComment"]["id"]
            reply_token = None

            while True:
                replies = fetch_replies(parent_id, reply_token)
                for r in replies.get("items", []):
                    rs = r["snippet"]
                    rows.append({
                        "videoId": video_id,
                        "author": rs["authorDisplayName"],
                        "text": rs["textDisplay"],
                        "publishedAt": rs["publishedAt"]
                    })
                    total += 1

                reply_token = replies.get("nextPageToken")
                if not reply_token:
                    break

                time.sleep(SLEEP_TIME)

        append_to_csv(rows, csv_path)

        next_token = data.get("nextPageToken")
        save_state(state_path, next_token, total)

        print(f"✔ {len(rows)} yorum alındı | Toplam: {total}")

        if not next_token:
            break

        time.sleep(SLEEP_TIME)

    print(f"✅ {video_id} tamamlandı → {total} yorum")

# ================== TÜM CSV → EXCEL ==================
def merge_to_excel(output_file="all_comments.xlsx"):
    dfs = []

    for vid in SKIP_FETCH_VIDEOS + FETCH_VIDEOS:
        csv_path = Path(f"{vid}_comments.csv")
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            dfs.append(df)
        else:
            print(f"⚠ CSV bulunamadı: {csv_path}")

    if not dfs:
        print("❌ Birleştirilecek veri yok")
        return

    final_df = pd.concat(dfs, ignore_index=True)

    final_df.drop_duplicates(
        subset=["videoId", "author", "text", "publishedAt"],
        inplace=True
    )

    final_df.to_excel(output_file, index=False)
    print(f"\n📊 TÜM YORUMLAR EXCEL'E AKTARILDI → {output_file}")

# ================== ÇALIŞTIR ==================
if __name__ == "__main__":

    print("⏭ İlk iki video CSV'den aynen alınacak:")
    for v in SKIP_FETCH_VIDEOS:
        print(f"   - {v}")

    for vid in FETCH_VIDEOS:
        collect_video_comments(vid)

    merge_to_excel()

    print("\n🎉 TÜM İŞLEM TAMAMLANDI")
