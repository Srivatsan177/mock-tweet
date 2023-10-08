import sqlalchemy

from core.pg_models.base_class import Base


class KafkaOffset(Base):
    __tablename__ = "kafka_offset"
    id=sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    offset = sqlalchemy.Column(sqlalchemy.BIGINT)
