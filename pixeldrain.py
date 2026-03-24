import os, time, requests
from dotenv import load_dotenv
from tqdm import tqdm
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from discord_webhook import DiscordWebhook
from crc_config import OUTPUT_DIR

load_dotenv()
API_KEY = os.getenv('PIXELDRAIN_API_KEY')
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
BASE_URL = os.getenv('PIXELDRAIN_URL', 'https://pixeldrain.com/').rstrip('/') + '/'

def upload_to_pixeldrain(file_path):
    file_name = os.path.basename(file_path)
    url = f"{BASE_URL}api/file"
    auth = ("", API_KEY) if API_KEY else None

    encoder = MultipartEncoder(
        fields={'file': (file_name, open(file_path, 'rb'))}
    )

    pbar = tqdm(
        total=encoder.len,
        unit='B',
        unit_scale=True,
        desc=file_name[:100]
    )

    def callback(monitor):
        pbar.update(monitor.bytes_read - pbar.n)

    monitor = MultipartEncoderMonitor(encoder, callback)

    try:
        response = requests.post(
            url,
            data=monitor,
            headers={'Content-Type': monitor.content_type},
            auth=auth
        )
        pbar.close()

        if response.status_code == 201:
            file_id = response.json()["id"]
            return f"{BASE_URL}u/{file_id}"
        else:
            print(f"\nGagal upload {file_name}. Status: {response.status_code}")
            return None
    except Exception as e:
        if 'pbar' in locals(): pbar.close()
        print(f"\nError pada file {file_name}: {e}")
        return None

def send_to_discord(file_name, link):
    if not link:
        return

    content = f"File Berhasil Diupload\nNama: `{file_name}`\nLink: {link}"
    webhook = DiscordWebhook(url=WEBHOOK_URL, content=content)
    webhook.execute()

def main():
    if not os.path.exists(OUTPUT_DIR):
        print(f"Folder {OUTPUT_DIR} tidak ditemukan")
        return

    files = [f for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f))]

    if not files:
        print("Tidak ada file untuk diupload")
        return

    print(f"Ditemukan {len(files)} file di folder {OUTPUT_DIR}")
    print("-" * 30)

    for file_name in files:
        full_path = os.path.join(OUTPUT_DIR, file_name)
        link = upload_to_pixeldrain(full_path)

        if link:
            print(f"Link: {link}")
            send_to_discord(file_name, link)
            print("Notifikasi dikirim ke Discord")
            time.sleep(1) # Jeda untuk menghindari rate limit

        print("-" * 30)

    print("Proses selesai")

if __name__ == "__main__":
    main()