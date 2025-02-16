# TGStickerDownloader

TGStickerDownloader is a Python script that allows you to download all stickers from a Telegram sticker pack using the Telethon library.

## Prerequisites

Before using this script, ensure you have the following:
- Python installed on your system
- Telethon library installed
- A Telegram API ID and API Hash (You can obtain these from [my.telegram.org](https://my.telegram.org))

## Installation

To install the required dependencies, run:

```sh
pip install telethon
```

## Configuration

You need to input your credentials inside the `settings.ini` file in the root directory as follows:

```ini
[telegram]
api_id = 123456  # Replace with your API ID
api_hash = your_api_hash  # Replace with your API Hash
phone = +911234567890  # Replace with your phone number linked to Telegram

[settings]
max_threads = 10  # Number of threads for downloading
wait_time = 0.5  # Delay between requests (in seconds)
```

## Usage

1. Ensure your `settings.ini` file is properly configured.
2. Run the script using:

```sh
python tg_sticker_downloader.py
```
3. Follow the prompts to authenticate with Telegram if required.
4. Enter the sticker pack link or name when prompted.
5. The stickers will be downloaded to a designated folder.

## Troubleshooting

- **Login Issues**: Ensure you have entered the correct phone number and API credentials.
- **Too Many Requests Error**: Increase `wait_time` in `settings.ini`.
- **Stickers Not Downloading**: Verify the sticker pack name/link and check your internet connection.

## Contribution

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Added a new feature"`
4. Push to the branch: `git push origin feature-name`
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

