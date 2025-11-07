"""
MSSQLTips.com General database connection configuration class
"""
import os
from attrs import define, field, validators
from sqlalchemy.engine import Engine, create_engine, URL
from dotenv import load_dotenv

load_dotenv()


@define
class RDSConfig:
    DB_SERVER: str = field(
        factory=lambda: os.getenv("DB_SERVER", ".\\MSSQLSERVER02"),
        validator=validators.instance_of(str)
    )
    DB_DATABASE: str = field(
        factory=lambda: os.getenv("DB_DATABASE", "MSSQLTips2025"),
        validator=validators.instance_of(str)
    )
    DB_USERNAME: str = field(
        factory=lambda: os.getenv("DB_USERNAME", ""),
        validator=validators.instance_of(str)
    )
    DB_PASSWORD: str = field(
        factory=lambda: os.getenv("DB_PASSWORD", ""),
        validator=validators.instance_of(str)
    )
    DB_PORT: int = field(
        factory=lambda: int(os.getenv("DB_PORT", 1433)),
        converter=int,
        validator=validators.instance_of(int)
    )
    DB_DRIVER: str = field(
        factory=lambda: os.getenv("DB_DRIVER", "mssql+pyodbc"),
        validator=validators.instance_of(str)
    )

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.DB_DRIVER,
            port=self.DB_PORT,
            host=self.DB_SERVER,
            database=self.DB_DATABASE,
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            query=dict(driver='ODBC Driver 18 for SQL Server',
                       # Trusted_Connection='True',
                       Encrypt='no',
                       TrustServerCertificate='yes')
        )

    def get_engine(self) -> Engine:
        return create_engine(self.url)


if __name__ == "__main__":
    db_cfg = RDSConfig()
    engine = db_cfg.get_engine()
    print(engine)
