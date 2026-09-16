from thespian.actors import *
import time

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

class NumberActor(Actor):
    def __init__(self):
        super().__init__()
        self.value = 0
 
    def receiveMessage(self, msg, sender):
        print(f'Актор числа с адресом {self.myAddress} получил {msg} от {sender}')
        # Ожидаем словарь со значением числа и адресом актора-калькулятора
        self.value = msg.get('init_value')
        calculator_address = msg.get('calculator_address')
        self.send(calculator_address, self.value)
 
class CalculatorActor(Actor):
    def __init__(self):
        super().__init__()
        self.values = []
 
    def receiveMessage(self, msg, sender):
        self.values.append(msg)
        total_sum = sum(self.values)
        print(f'Актор-калькулятор с адресом {self.myAddress} получил {msg} от {sender}, '
              f'итоговая сумма: {total_sum}')

class ExtendedCalculatorActor(Actor):
    def __init__(self):
        super().__init__()
        self.values = []
        self.operation = 'add'

    def compute(self):
        if self.operation == 'add':
            return sum(self.values)
        if self.operation == 'subtract':
            result = self.values[0]
            for v in self.values[1:]:
                result -= v
            return result
        if self.operation == 'multiply':
            result = 1
            for v in self.values:
                result *= v
            return result
        if self.operation == 'divide':
            result = self.values[0]
            for v in self.values[1:]:
                result /= v
            return result

    def receiveMessage(self, msg, sender):
        if isinstance(msg, dict) and 'operation' in msg:
            self.operation = msg['operation']
            print(f'Актор-калькулятор с адресом {self.myAddress} переключён на операцию "{self.operation}"')
            return
        self.values.append(msg)
        print(f'Актор-калькулятор с адресом {self.myAddress} получил {msg} от {sender}, '
              f'операция "{self.operation}", результат: {self.compute()}')
        
class TimerActor(Actor):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def receiveMessage(self, msg, sender):
        self.counter += 1
        print(f'Актор-таймер с адресом {self.myAddress} получил обращение №{self.counter}: {msg}')
        self.send(sender, self.counter)
        
class ChainLinkActor(Actor):
    def __init__(self):
        super().__init__()
        self.next_address = None
        self.origin_address = None

    def receiveMessage(self, msg, sender):
        if isinstance(msg, dict) and msg.get('type') == 'configure':
            self.next_address = msg.get('next_address')
            self.origin_address = msg.get('origin_address')
            return
        if isinstance(msg, dict) and msg.get('type') == 'chain_message':
            if self.next_address is not None:
                print(f'Актор цепочки {self.myAddress} пересылает сообщение актору {self.next_address}')
                self.send(self.next_address, msg)
            else:
                elapsed = time.time() - msg['start_time']
                print(f'Последний актор цепочки {self.myAddress} получил сообщение, 'f'время прохождения по цепочке: {elapsed} с')
                self.send(self.origin_address, {'type': 'chain_result', 'elapsed': elapsed})
            return
        if isinstance(msg, dict) and msg.get('type') == 'chain_result':
            print(f'Первый актор цепочки {self.myAddress} получил результат: 'f'время прохождения {msg["elapsed"]} с')
            
if __name__ == "__main__":
    # Создаем систему акторов, внутри которой они будут жить
    actorSystem = ActorSystem()
    # Создаем экземпляр созданного нами класса и сохраняем его адрес
    # actorAddress1 = actorSystem.createActor(SimplestActor)
    # actorSystem.tell(actorAddress1, 'CREATE_ACTOR')
    # actorSystem.tell(actorAddress1, 'RETRANSLATED MESSAGE')
    # # Отправляем по сохраненному адресу сообщение
    # actorSystem.tell(actorAddress1, "Первое сообщение")
    # actorSystem.tell(actorAddress1, 132)
    # actorSystem.tell(actorAddress1, [1, 3, 5])
    # actorSystem.tell(actorAddress1, {'key': 'value'})
    
    # calculator_address = actorSystem.createActor(CalculatorActor)
 
    # number_agent_1 = actorSystem.createActor(NumberActor)
    # init_message_1 = {'init_value': 1, 'calculator_address': calculator_address}
    # actorSystem.tell(number_agent_1, init_message_1)
 
    # number_agent_2 = actorSystem.createActor(NumberActor)
    # init_message_2 = {'init_value': 2, 'calculator_address': calculator_address}
    # actorSystem.tell(number_agent_2, init_message_2)
 
    # number_agent_3 = actorSystem.createActor(NumberActor)
    # init_message_3 = {'init_value': 3, 'calculator_address': calculator_address}
    # actorSystem.tell(number_agent_3, init_message_3)
    
    # #задание 1 
    # ext_calculator = actorSystem.createActor(ExtendedCalculatorActor)
    # actorSystem.tell(ext_calculator, {'operation': 'multiply'})
    # actorSystem.tell(ext_calculator, 2)
    # actorSystem.tell(ext_calculator, 3)
    # actorSystem.tell(ext_calculator, 4)
    # actorSystem.tell(ext_calculator, {'operation': 'subtract'})
    # actorSystem.tell(ext_calculator, 10)
    
    # #задание 2
    # timer_1 = actorSystem.createActor(TimerActor)
    # timer_2 = actorSystem.createActor(TimerActor)
    # print('Таймер 1:', actorSystem.ask(timer_1, 'ping', 2))
    # print('Таймер 1:', actorSystem.ask(timer_1, 'ping', 2))
    # print('Таймер 2:', actorSystem.ask(timer_2, 'ping', 2))

    #задание 3
    chain = [actorSystem.createActor(ChainLinkActor) for _ in range(5)]
    for i, address in enumerate(chain):
        next_address = chain[i + 1] if i + 1 < len(chain) else None
        actorSystem.tell(address, {'type': 'configure', 'next_address': next_address, 'origin_address': chain[0]})
    time.sleep(0.2)
    actorSystem.tell(chain[0], {'type': 'chain_message', 'start_time': time.time()})
    time.sleep(1)
