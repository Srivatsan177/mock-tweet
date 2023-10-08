from kafka import KafkaConsumer, TopicPartition
from core.utils.constants import KAFKA_USER_LIKE_TOPIC, KAFKA_HOST
import json
from core.dataclass_containers.tweets import TweetLike as TweetLikeContainer
from core.pg_models.tweets import TweetLike
from core.utils.db_util import DbHelper
import sqlalchemy
from core.pg_models.kafka_offset import KafkaOffset

BATCH_SIZE = 10000


class TweetLikeConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(bootstrap_servers=[KAFKA_HOST], consumer_timeout_ms=5000)
        self.partition = TopicPartition(KAFKA_USER_LIKE_TOPIC, partition=0)
        self.consumer.assign([self.partition])
        self.session = DbHelper().get_connection()
        with self.session.begin() as connection:
            kafka_offset = connection.execute(sqlalchemy.select(KafkaOffset).where(KafkaOffset.id == 0)).first()[0]
            self.consumer.seek(self.partition, kafka_offset.offset + 1)

    def _push_to_postgres(self):
        tweet_like_containers = []
        print(self.consumer.position(self.partition))
        last_offset = -1
        for message in self.consumer:
            json_str = message.value.decode("utf-8")
            json_obj = json.loads(json_str)
            tweet_like_containers.append(TweetLikeContainer(id=json_obj["id"], value=json_obj["value"]))
            last_offset = message.offset
            if len(tweet_like_containers) >= BATCH_SIZE:
                break
        if last_offset >= 0:
            with self.session.begin() as connection:
                kafka_offset = connection.execute(sqlalchemy.select(KafkaOffset).where(KafkaOffset.id == 0)).first()[0]
                kafka_offset.offset = last_offset
        print(tweet_like_containers)
        if len(tweet_like_containers) > 0:
            print("updating values")
            results = self._reduce(tweet_like_containers)
            with self.session.begin() as connection:
                for tweet_id, count in results.items():
                    query = sqlalchemy.select(TweetLike).where(TweetLike.tweet_id == tweet_id)
                    tweet_like = connection.execute(query).first()[0]
                    tweet_like.like_count += count
    def _reduce(self, containers):
        results = {}
        for container in containers:
            results[container.id] = results.get(container.id, 0) + container.value
        return results

    def run(self):
        self._push_to_postgres()
