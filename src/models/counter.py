class ScrapeCounter:
    count = 0

    @classmethod
    def increment(cls, amount: int = 1):
        cls.count += amount

    @classmethod
    def reset(cls):
        cls.count = 0

    @classmethod
    def get_count(cls) -> int:
        return cls.count