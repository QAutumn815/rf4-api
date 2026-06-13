import logging

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service  import Service
from selenium.webdriver.common.by      import By
from selenium.webdriver.support.ui     import WebDriverWait
from selenium.webdriver.support        import expected_conditions as EC
from selenium.common.exceptions        import TimeoutException, WebDriverException
from selenium                          import webdriver
from webdriver_manager.chrome          import ChromeDriverManager

logger = logging.getLogger(__name__)


class WebDriver:
    def __init__(self) -> None:
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.0 Safari/537.36"
        )
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-images")
        options.add_argument("--disable-css")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--user-agent={user_agent}")

        service = Service(ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=service, options=options)
        self._driver.implicitly_wait(5)

    def fetch_raw_html(self, url: str, class_name: str) -> str:
        """Fetch raw HTML from a URL by waiting for an element with the given class name.

        Returns the outerHTML of the first matching element.
        Raises TimeoutException if the element is not found within 10 seconds.
        """
        try:
            self._driver.get(url)
            element = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            return element.get_attribute("outerHTML")
        except TimeoutException:
            logger.error(
                "Timeout waiting for element '%s' at %s", class_name, url
            )
            raise
        except WebDriverException as e:
            logger.error("WebDriver error fetching %s: %s", url, e)
            raise

    @property
    def driver(self) -> webdriver:
        return self._driver

    def quit(self) -> None:
        """Clean up the WebDriver resources."""
        try:
            self._driver.quit()
        except Exception:
            pass
