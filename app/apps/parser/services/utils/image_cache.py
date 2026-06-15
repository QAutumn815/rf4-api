import os
import re
import base64
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class FishImageCache:
    """Download and cache fish images locally, deduplicated by filename.

    Uses Selenium CDP when a WebDriver is available (bypasses hotlink protection
    that blocks plain HTTP requests).
    """

    _subdir = "fish"

    @classmethod
    def _cache_dir(cls) -> str:
        return os.path.join(settings.MEDIA_ROOT, cls._subdir)

    @classmethod
    def get(cls, remote_url: str, driver=None) -> str:
        """Download (if not cached) and return the local media URL path."""
        if not remote_url:
            return ""

        filename = os.path.basename(remote_url.rstrip("/"))
        if not filename:
            return ""

        cache_dir = cls._cache_dir()
        local_path = os.path.join(cache_dir, filename)
        media_url = f"{settings.MEDIA_URL}{cls._subdir}/{filename}"

        # Already cached
        if os.path.exists(local_path):
            return media_url

        # Ensure cache directory exists
        os.makedirs(cache_dir, exist_ok=True)

        # Download via Selenium CDP (handles advanced hotlink protection)
        if driver is not None:
            success = cls._download_via_selenium(driver, remote_url, local_path)
        else:
            success = cls._download_via_urllib(remote_url, local_path)

        if not success:
            return ""

        # Validate downloaded file is a real PNG
        try:
            with open(local_path, "rb") as f:
                header = f.read(8)
            if header == b"\x89PNG\r\n\x1a\n":
                logger.info("Cached fish image: %s -> %s", filename, media_url)
                return media_url
            else:
                logger.warning("Downloaded %s is not a valid PNG, removing", filename)
                os.remove(local_path)
                return ""
        except Exception as exc:
            logger.warning("Failed to validate %s: %s", filename, exc)
            return ""

    @classmethod
    def _download_via_urllib(cls, url: str, local_path: str) -> bool:
        import urllib.request
        try:
            urllib.request.urlretrieve(url, local_path)
            return True
        except Exception as exc:
            logger.warning("urllib download failed for %s: %s", url, exc)
            return False

    @classmethod
    def _download_via_selenium(cls, driver, url: str, local_path: str) -> bool:
        """Download image using Selenium's CDP (bypasses hotlink protection)."""
        try:
            # Navigate to the image URL directly
            driver.get(url)

            # Fetch the binary data via same-origin JS
            result = driver.execute_async_script("""
                const url = arguments[0];
                const done = arguments[1];
                fetch(url)
                    .then(r => r.arrayBuffer())
                    .then(buf => {
                        const bytes = new Uint8Array(buf);
                        let binary = '';
                        for (let i = 0; i < bytes.length; i++) {
                            binary += String.fromCharCode(bytes[i]);
                        }
                        done(btoa(binary));
                    })
                    .catch(err => done('SEL_ERR:' + err.toString()));
            """, url)

            if not result or result.startswith("SEL_ERR"):
                logger.warning("Selenium CDP fetch failed for %s: %s", url,
                               (result or "no result")[:80])
                return False

            img_data = base64.b64decode(result)
            with open(local_path, "wb") as f:
                f.write(img_data)
            return True

        except Exception as exc:
            logger.warning("Selenium CDP download error for %s: %s", url, exc)
            return False
