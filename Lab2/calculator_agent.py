from unittest import result

from thespian.actors import ActorAddress

from agent_base import AgentBase
from message import MessageType, Message


class CalculatorAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.subscribe(MessageType.SET_OPERATION, self.handle_set_operation)
        self.values = []
        self.operation = ''


    def handle_hello_world(self, message: Message, sender: ActorAddress):
        new_value = message.msg_body
        self.values.append(new_value)
        total_sum = sum(self.values)
        print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
              f'от {sender}, итоговая сумма: {total_sum}')

    def handle_set_operation(self, message: Message, sender: ActorAddress):
        new_value = message.msg_body
        self.operation = new_value
        if self.operation == '+':
            total_sum = sum(self.values)
            print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
                  f'от {sender}, итоговая сумма: {total_sum}')
        elif self.operation == '-':
            subtract_result = self.values[0]
            for v in self.values[1:]:
                subtract_result -= v
            print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
                  f'от {sender}, итоговая разница: {subtract_result}')
        elif self.operation == '*':
            multiply_result = 1
            for v in self.values:
                multiply_result *= v
            print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
                  f'от {sender}, итог умножения : {multiply_result}')
        else:
            divide_result = self.values[0]
            for v in self.values[1:]:
                divide_result/=v
            print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
                  f'от {sender}, итог деления: {divide_result}')