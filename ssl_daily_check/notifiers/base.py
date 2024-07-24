from abc import ABC, abstractmethod

class BaseNotifier(ABC):
    @abstractmethod
    def send_notification(self, expired_domains):
        pass
