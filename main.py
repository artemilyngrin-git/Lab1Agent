from thespian.actors import *


class SimplestActor(Actor):
    """Простой актор, который в будущем станет агентом"""
    def __init__(self):
        super().__init__()
        print('Создан новый актор')
        self.messages = []
        self.child_addresses = []

    def receiveMessage(self, msg, sender):
        print(f'Актор с адресом {self.myAddress} получил {msg} от {sender}')
        self.messages.append(msg)
        for message in self.messages:
            print(f'Актор с адресом {self.myAddress} ранее получал сообщение {message}')


if __name__ == "__main__":
#     # Создаем систему акторов, внутри которой они будут жить
    actorSystem = ActorSystem()
    # Создаем экземпляр созданного нами класса и сохраняем его адрес
    actorAddress1 = actorSystem.createActor(SimplestActor)
    # Отправляем по сохраненному адресу сообщение
    actorSystem.tell(actorAddress1, "Первое сообщение")

    actorSystem.tell(actorAddress1, 132)
    actorSystem.tell(actorAddress1, [1, 3, 5])
    actorSystem.tell(actorAddress1, {'key': 'value'})



