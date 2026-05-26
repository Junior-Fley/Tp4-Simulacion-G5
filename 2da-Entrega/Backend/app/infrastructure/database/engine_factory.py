from __future__ import annotations

from typing import Optional
import orjson
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def json_serializer(obj):
    return orjson.dumps(obj).decode("utf-8")


_DEFAULT_KWARGS = dict(
    echo=False,
    connect_args={
        "timeout": 30,
    },
    json_serializer=json_serializer,
)


def create_db_engine(db_url: Optional[str] = None, **overrides) -> Engine:
    """
    Crea y retorna un Engine de SQLAlchemy con la configuración estándar del proyecto.
    - db_url: si no se pasa, asume la estándar
    - overrides: permite ajustar parámetros.
    """
    db_url = "sqlite:///../database/bdd.db" if db_url is None else db_url

    kwargs = {**_DEFAULT_KWARGS, **overrides}
    return create_engine(db_url, **kwargs)