from enum import Enum
class State(Enum):
    WAITING = 0
    RUNNING = 1
    DONE = 2

class KafkaBrokers(Enum):
    MAIN = "127.0.0.1:9092"

class KafkaTopics(Enum):
    CRAWLER_DOWNLOAD = "CRAWLER_DOWNLOAD"