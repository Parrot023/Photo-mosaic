
from bing_image_downloader import downloader


downloader.download("Nature", limit=100, output_dir='images', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
