import os
import logging
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


class FishImageCache:
    """Download and cache fish images locally, deduplicated by filename.

    Usage:
        url = FishImageCache.get("https://rf4game.com/res/48x48/alb_barbel.png")
        # Returns "/media/fish/alb_barbel.png"
    """

    _subdir = "fish"  # subdirectory under MEDIA_ROOT

    @classmethod
    def _cache_dir(cls) -> str:
        return os.path.join(settings.MEDIA_ROOT, cls._subdir)

    @classmethod
    def get(cls, remote_url: str) -> str:
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

        # Download
        try:
            urllib.request.urlretrieve(remote_url, local_path)
            logger.info("Cached fish image: %s -> %s", filename, media_url)
        except Exception as exc:
            logger.warning("Failed to download fish image %s: %s", remote_url, exc)
            return ""

        return media_url
