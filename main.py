from thespian.actors import *


class SimplestActor(Actor):

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

        for child in self.child_addresses:
            print(f'Ретранслируем сообщение дочернему актору с адресом {child}')
            self.send(child, msg)
        if msg == 'CREATE_ACTOR':
            child_actor_address = self.createActor(SimplestActor)
            print(f'Создали нового актора, его адрес - {child_actor_address}')
            self.child_addresses.append(child_actor_address)

if __name__ == "__main__":
    # Создаем систему акторов, внутри которой они будут жить
    actorSystem = ActorSystem()
    # Создаем экземпляр созданного нами класса и сохраняем его адрес
    actorAddress1 = actorSystem.createActor(SimplestActor)
    actorSystem.tell(actorAddress1, 'CREATE_ACTOR')
    actorSystem.tell(actorAddress1, 'RETRANSLATED MESSAGE')
    # Отправляем по сохраненному адресу сообщение
    # actorSystem.tell(actorAddress1, "Первое сообщение")
    # actorSystem.tell(actorAddress1, 132)
    # actorSystem.tell(actorAddress1, [1, 3, 5])
    # actorSystem.tell(actorAddress1, {'key': 'value'})
