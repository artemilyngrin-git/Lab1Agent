from collections import Counter


class MessageStats:
    counter = Counter()

    @classmethod
    def register(cls, message):
        cls.counter[message.msg_type.name] += 1

    @classmethod
    def reset(cls):
        cls.counter = Counter()

    @classmethod
    def total(cls):
        return sum(cls.counter.values())
