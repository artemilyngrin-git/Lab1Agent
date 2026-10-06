from thespian.actors import *

from calculator_agent import CalculatorAgent
from number_agent import NumberAgent
from message import Message, MessageType

if __name__ == '__main__':
    actorSystem = ActorSystem()
    calculator_address = actorSystem.createActor(CalculatorAgent)

    number_agent_1 = actorSystem.createActor(NumberAgent)
    init_message_1_data = {'init_value': 1, 'calculator_address': calculator_address}
    init_message_1 = Message(MessageType.INITIALIZATION, init_message_1_data)
    actorSystem.tell(number_agent_1, init_message_1)

    number_agent_2 = actorSystem.createActor(NumberAgent)
    init_message_2_data = {'init_value': 3, 'calculator_address': calculator_address}
    init_message_2 = Message(MessageType.INITIALIZATION, init_message_2_data)
    actorSystem.tell(number_agent_2, init_message_2)
