from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __table_name__ automatically
    @declared_attr
    def __table_name__(self) -> str:
        return self.__name__.lower()
