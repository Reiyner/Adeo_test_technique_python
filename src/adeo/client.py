import httpx

class Client:
    def __init__(self, max_retries=2 ):
        self.client = httpx.AsyncClient()
        self.max_retries = max_retries
        pass

    async def get(self,url: str):

        for attempt in range(self.max_retries):
            try:
                response = await self.client.get(url=url)
                return response
            except Exception as e:
                if attempt <= self.max_retries:
                    continue
                raise e

    async def close(self):
        await self.client.aclose()


