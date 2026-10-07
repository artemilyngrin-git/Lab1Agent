from unittest import result

from thespian.actors import ActorAddress

from agent_base import AgentBase
from message import MessageType, Message


class CalculatorAgent(AgentBase):
    MAX_MESSAGES = 10

    # def handle_hello_world(self, message: Message, sender: ActorAddress):
    #     new_value = message.msg_body.get('init_value')
    #     self.values.new_value
    #     total_sum = sum(self.values)
    #     print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
    #           f'от {sender}, итоговая сумма: {total_sum}')

    def __init__(self):
        super().__init__()
        self.subscribe(MessageType.SET_OPERATION, self.handle_set_operation)
        self.values = None
        self.operation = ''
        self.count = 0

    def handle_set_operation(self, message: Message, sender: ActorAddress):
        self.count += 1
        if self.count >= self.MAX_MESSAGES:
            self.unsubscribe(MessageType.SET_OPERATION)
            self.subscribe(MessageType.SET_OPERATION, self.handle_refusal)
            print(f'Калькулятор принял {self.MAX_MESSAGES} сообщений и больше не принимает числа')

        new_value = message.msg_body.get('init_value')
        new_operation = message.msg_body.get('operation')

        self.operation = new_operation

        if self.values is None:
            self.values = new_value
            print(f'Актор-калькулятор {self.myAddress}: Стартовое число: {self.values}')
            return

        if self.operation == '+':
            self.values += new_value
            print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
                  f'от {sender}, итоговая сумма: {self.values}')
        elif self.operation == '-':
            self.values -= new_value
            print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
                  f'от {sender}, итоговая разница: {self.values}')
        elif self.operation == '*':
            self.values *= new_value
            print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
                  f'от {sender}, итог умножения : {self.values}')
        elif self.operation == '/':
            if new_value != 0:
                self.values /= new_value
                print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
                      f'от {sender}, итог деления: {self.values}')
            else:
                print(f'Актор-калькулятор с адресом {self.myAddress} получил 0, деление на 0 запрещено')

    def handle_refusal(self, message: Message, sender: ActorAddress):
        reason = f'лимит в {self.MAX_MESSAGES} сообщений исчерпан'
        self.send(sender, Message(MessageType.REJECTED, reason))