import httpx
import os


class GIFApiException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GIF:
    def __init__(self, *args, **kwargs):
        self.type = kwargs.get("type", "gif")
        self.id = kwargs.get("id")
        self.slug = kwargs.get("slug")
        self.url = kwargs.get("url")
        self.title = kwargs.get("title")

    def __repr__(self) -> str:
        return f"GIF(title: {self.title}, type: {self.type}, id: {self.id}, slug: {self.slug}, url: {self.url})"


class GiphyApi:
    def __init__(self):
        self.api_key = os.getenv("giphy_api_key") or ""
        self.base_url = "https://api.giphy.com/v1"

    def _get(
        self, endpoint: str, params: dict[str, str] | None = None
    ) -> httpx.Response:
        params = params or {}
        res = httpx.get(
            self.base_url + endpoint, params={"api_key": self.api_key} | params
        )
        if not res.is_success:
            raise GIFApiException(res.json())
        return res

    def get_trending(self, **kwargs) -> list[GIF]:
        return [
            GIF(**i)
            for i in self._get("/gifs/trending", params=kwargs).json().get("data")
        ]

    def search(self, q: str, **kwargs) -> list[GIF]:
        return [
            GIF(**i)
            for i in self._get("/gifs/search", params={"q": q} | kwargs)
            .json()
            .get("data")
        ]


giphy_api_instance = GiphyApi()
