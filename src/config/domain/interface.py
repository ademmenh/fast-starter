from abc import ABC, abstractmethod


class IConfig(ABC):
    @property
    @abstractmethod
    def env(self) -> str:
        pass

    @property
    @abstractmethod
    def app_name(self) -> str:
        pass

    @property
    @abstractmethod
    def api_version(self) -> str:
        pass

    @property
    @abstractmethod
    def port(self) -> int:
        pass

    @property
    @abstractmethod
    def nginx_port(self) -> int:
        pass

    @property
    @abstractmethod
    def db_host(self) -> str:
        pass

    @property
    @abstractmethod
    def db_port(self) -> int:
        pass

    @property
    @abstractmethod
    def db_user(self) -> str:
        pass

    @property
    @abstractmethod
    def db_password(self) -> str:
        pass

    @property
    @abstractmethod
    def db_name(self) -> str:
        pass

    @property
    @abstractmethod
    def logs_dirname(self) -> str:
        pass

    @property
    @abstractmethod
    def retention_days(self) -> int:
        pass

    @property
    @abstractmethod
    def jwt_access_token_secret(self) -> str:
        pass

    @property
    @abstractmethod
    def jwt_refresh_token_secret(self) -> str:
        pass

    @property
    @abstractmethod
    def jwt_access_token_expiry(self) -> int:
        pass

    @property
    @abstractmethod
    def jwt_refresh_token_expiry(self) -> int:
        pass

    @property
    @abstractmethod
    def jwt_algo(self) -> str:
        pass

    @property
    @abstractmethod
    def cookies_secure(self) -> bool:
        pass

    @property
    @abstractmethod
    def cookies_same_site(self) -> str:
        pass

    @property
    @abstractmethod
    def cors_origins(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def cors_credentials(self) -> bool:
        pass

    @property
    @abstractmethod
    def database_url(self) -> str:
        pass

    @property
    @abstractmethod
    def async_database_url(self) -> str:
        pass

    @property
    @abstractmethod
    def jwt_secret(self) -> str:
        pass

    @property
    @abstractmethod
    def debug(self) -> bool:
        pass
