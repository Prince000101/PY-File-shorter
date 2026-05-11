async def fetch_middleware(session: ClientSession, url: str) -> dict:
    async with semaphore:
        for attempt in range(MAX_RETRIES):
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    logger.warning(f'Got {resp.status}, retry {attempt+1}')
            except aiohttp.ClientError as e:
                logger.error(f'Request failed: {e}')
                if attempt == MAX_RETRIES - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
