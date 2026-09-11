from thespian.actors import *


class SimplestActor(Actor):
    """Простой актор, который в будущем станет агентом"""

    def receiveMessage(self, msg, sender):
        print(f'Актор с адресом {self.myAddress} получил {msg} от {sender}')


if __name__ == "__main__":
    # Создаем систему акторов, внутри которой они будут жить
    actorSystem = ActorSystem()
    # Создаем экземпляр созданного нами класса и сохраняем его адрес
    actorAddress1 = actorSystem.createActor(SimplestActor)
    # Отправляем по сохраненному адресу сообщение
    actorSystem.tell(actorAddress1, "Первое сообщение")
