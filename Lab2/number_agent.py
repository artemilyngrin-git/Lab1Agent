from thespian.actors import ActorAddress

from agent_base import AgentBase
from message import Message, MessageType


class NumberAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.operation = ''
        self.subscribe(MessageType.INITIALIZATION, self.handle_initialization)
        self.subscribe(MessageType.SET_OPERATION, self.handle_set_operation)

    def handle_initialization(self, message: Message, sender: ActorAddress):
        print(f'Актор числа с адресом {self.myAddress} получил {message} от {sender}')
        self.value = message.msg_body.get('init_value')
        calculator_address = message.msg_body.get('calculator_address')
        new_message = Message(MessageType.HELLO_WORLD, self.value)
        self.send(calculator_address, new_message)


    def handle_set_operation(self, message: Message, sender: ActorAddress):
        print(f'Актор числа с адресом {self.myAddress} получил {message} от {sender}')
        self.value = message.msg_body.get('init_value')
        self.operation = message.msg_body.get('operation')
        calculator_address = message.msg_body.get('calculator_address')

        # формируем сообщение
        payload = {'init_value': self.value, 'operation': self.operation}
        new_message = Message(MessageType.SET_OPERATION, payload)

        self.send(calculator_address, new_message)
        
    def handle_rejected(self, message: Message, sender: ActorAddress):
        print(f'Агент числа {self.myAddress}: значение {self.value} отклонено, причина: {message.msg_body}')