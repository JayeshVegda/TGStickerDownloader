import os
import re
import asyncio
import configparser
from telethon import TelegramClient
from telethon.errors import RPCError, FileMigrateError
from telethon.tl.functions.messages import GetAllStickersRequest, GetStickerSetRequest
from telethon.tl.types import InputStickerSetID

# Load settings from ini file
config = configparser.ConfigParser()
config.read("settings.ini")

if "telegram" not in config or "settings" not in config:
    raise KeyError("Missing [telegram] or [settings] section in settings.ini!")

api_id = int(config["telegram"]["api_id"])
api_hash = config["telegram"]["api_hash"]
phone = config["telegram"]["phone"]
MAX_CONCURRENT_DOWNLOADS = int(config["settings"]["max_threads"])
WAIT_TIME = float(config["settings"].get("wait_time", 0.5))  # Default to 0.5 sec if not set

client = TelegramClient("sticker_downloader", api_id, api_hash)

def sanitize_filename(name):
    """Removes invalid characters from folder names."""
    return re.sub(r'[<>:"/\\|?*]', "", name)  # Remove special characters

async def download_sticker(sticker, folder, index):
    """Download a single sticker."""
    try:
        await asyncio.sleep(WAIT_TIME)  # Avoid rate limit
        await client.download_media(sticker, file=os.path.join(folder, f"{index}.webp"))
    except RPCError as e:
        print(f"❌ Failed to download sticker {index}: {e}")

async def download_sticker_pack(pack):
    """Download all stickers from a given pack."""
    pack_name = sanitize_filename(pack.title.replace(" ", "_"))
    folder = f"stickers/{pack_name}"
    os.makedirs(folder, exist_ok=True)

    print(f"📥 Downloading: {pack.title}...")

    try:
        sticker_set = await client(GetStickerSetRequest(InputStickerSetID(pack.id, pack.access_hash), hash=0))

        tasks = [download_sticker(sticker, folder, i) for i, sticker in enumerate(sticker_set.documents)]
        await asyncio.gather(*tasks)

        print(f"✔ {pack.title} downloaded successfully.")
    except FileMigrateError as e:
        print(f"⚠️ File stored in different DC, reconnecting... ({e})")
        new_dc = e.new_dc
        await client.disconnect()
        client.session.set_dc(new_dc)
        await client.connect()
        await download_sticker_pack(pack)  # Retry after reconnecting
    except Exception as e:
        print(f"❌ Skipping {pack.title} due to error: {e}")

async def download_all_stickers():
    """Fetch all sticker packs and download them asynchronously."""
    await client.start(phone)
    sticker_sets = await client(GetAllStickersRequest(0))

    for pack in sticker_sets.sets:
        await download_sticker_pack(pack)

    await client.disconnect()
    print("✅ All stickers downloaded!")

# Run everything inside the same event loop
asyncio.run(download_all_stickers())
