from abc import abstractmethod
from botish.finance.models.open_interest import OpenInterest


class IAdapter:
    @abstractmethod
    async def get_all_symbols(self) -> list[str]: ...

    @abstractmethod
    async def get_open_interests(self) -> list[OpenInterest]: ...
