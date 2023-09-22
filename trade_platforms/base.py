from abc import ABC, abstractmethod


class TradePlatform(ABC):
    """
    Inherit other trade platforms from this class.
    New methods are welcome.
    """

    @abstractmethod
    def get_connection(self):
        """Create a connection."""
        pass

    @abstractmethod
    def ping(self):
        """Ping a connection."""
        pass
