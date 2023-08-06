import dataclasses as dc
import typing as t
import httpx
from ssl import SSLContext
from types import TracebackType

from geopy.adapters import BaseAsyncAdapter, _normalize_proxies
from geopy.geocoders import Nominatim

# from brew_scout import MODULE_NAME, VERSION
P = t.ParamSpec("P")


class HttpxAsyncAdapter(BaseAsyncAdapter):
    def __init__(self, *, proxies: dict[t.Hashable, t.Any], ssl_context: SSLContext):
        proxies = _normalize_proxies(proxies)
        super().__init__(proxies=proxies, ssl_context=ssl_context)

        self.proxies = proxies
        self.ssl_context = ssl_context
    
    async def __aenter__(self) -> t.Self:
        return self
    
    async def __aexit__(self, exc_type: t.Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None:
        await self.client.aclose()
    
    @property
    def client(self) -> httpx.AsyncClient:
        if not (client := self.__dict__.get("client")):
            client = httpx.AsyncClient(trust_env=False)
            self.__dict__["client"] = client

        return client
    
    async def get_text(self, url,  *, timeout, headers) -> str:
        response = await self._request(url=url, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        return response.text
    
    async def get_json(self, url, *, timeout, headers) -> t.Mapping[t.Hashable, t.Any]:
        response = await self._request(url=url, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def _request(self, *, url, timeout, headers) -> httpx.Response:
        return await self.client.get(url=url, timeout=timeout, headers=headers)



@dc.dataclass(frozen=True, slots=True)
class GeoClient:
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Nominatim:
        return Nominatim(
            user_agent=self._get_user_agent(),
            adapter_factory=HttpxAsyncAdapter
        )

    def _get_user_agent(self) -> str:
        # return f"{MODULE_NAME}/{VERSION}"
        return f"MODULE_NAME/VERSION-1"


async def main() -> None:
    gc = GeoClient()
    
    async with gc() as geolocator:
        location = await geolocator.reverse((35.14536898418535, 33.40408254113125), language="en")
    print(location.raw)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
