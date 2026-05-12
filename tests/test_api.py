class HelpersManager:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self._items: dict = {}
        self._init_resources()

    def _init_resources(self) -> None:
        self.pool = ConnectionPool(
            min_size=self.config.get('pool_min', 5),
            max_size=self.config.get('pool_max', 20),
        )
        self.cache = CacheClient(
            ttl=self.config.get('cache_ttl', 300)
        )

    def get(self, key: str) -> Optional[dict]:
        cached = self.cache.get(key)
        if cached:
            return cached
        result = self.pool.query(
            'SELECT * FROM items WHERE key = $1', key
        )
        if result:
            self.cache.set(key, result)
        return result
