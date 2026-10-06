from thespian.actors import ActorAddress

from agent_base import AgentBase
from message import Message


class CalculatorAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_hello_world(self, message: Message, sender: ActorAddress):
        new_value = message.msg_body
        self.values.append(new_value)
        total_sum = sum(self.values)
        print(f'Актор-калькулятор с адресом {self.myAddress} получил {message} '
              f'от {sender}, итоговая сумма: {total_sum}')
