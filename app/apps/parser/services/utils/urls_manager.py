class URLsManager:
    __REGIONS    = ["GL", "RU", "DE", "US", "FR", "CN", "PL", "KR", "JP", "EN"]
    __CATEGORIES = ["records", "ultralight", "telestick"]

    def records_urls(self, weekly: bool = False) -> dict:
        if weekly:
            return {
                rg: {
                    ct: f"https://rf4game.com/cn/{ct}/weekly/region/{rg}/"
                    for ct in self.__CATEGORIES
                }
                for rg in self.__REGIONS
            }

        return {
            rg: {
                ct: f"https://rf4game.com/cn/{ct}/region/{rg}/"
                for ct in self.__CATEGORIES
            }
            for rg in self.__REGIONS
        }

    def ratings_urls(self) -> dict:
        return {
            rg: f"https://rf4game.com/cn/ratings/region/{rg}/"
            for rg in self.__REGIONS
        }

    def winners_urls(self) -> dict:
        return {
            rg: {
                ct: f"https://rf4game.com/cn/{ct}/winners/region/{rg}/"
                for ct in self.__CATEGORIES
            }
            for rg in self.__REGIONS
        }

    @property
    def regions(self) -> list[str]:
        return self.__REGIONS

    @property
    def categories(self) -> list[str]:
        return self.__CATEGORIES
