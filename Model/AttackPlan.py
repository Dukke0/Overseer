import queue
import threading
import time
from typing import Union
from Model.Attacks.AbstractAttack import AbstractAttack, AttackResultInfo
from Model.Attacks.EvilTwin import EvilTwin
from Model.Target import Target

class AttackPlan():

    END_MESSAGE = 'Attack plan has finished!'

    def __init__(self, target=None, attack_list=list(), controller=None):
        self.__target = target
        self.__attack_list = attack_list
        self.controller = controller

    @property
    def attack_list(self) -> list:
        return self.__attack_list
    
    @attack_list.setter
    def attack_list(self, values: Union[AbstractAttack, list]) -> None:
        self.__attack_list = [values]

    def add_attack(self, attack: AbstractAttack) -> None:
        if attack not in self.__attack_list:
            self.__attack_list.append(attack)
    
    def remove_attack(self, attack: AbstractAttack) -> None:
        if attack in self.__attack_list:
            self.__attack_list.remove(attack)

    @property
    def target(self) -> Target:
        return self.__target

    @target.setter
    def target(self, target: Target) -> None:
        self.__target = Target
    
    def execute_plan(self, q, kwargs) -> list():
        current_threads = list()
        for attack in self.__attack_list:
            #q.put('Attempting attack: ' + attack.attack_name())
            t = threading.Thread(target=attack.execute_attack, args=(q, kwargs), daemon=True)
            current_threads.append(t)
            t.start()
            self.update(q, threads=current_threads)

    def update(self, q, threads):
        print('Im ', threading.get_ident())
        while True:

            if not threads:
                q.put(self.END_MESSAGE)
                print('its over')
                break 
            print(threads)
            threads = [t for t in threads if t.is_alive()]
            time.sleep(2)
            self.controller.attack_notification(q=q)

"""
    def execute_plan(self, **kwargs) -> list():
        q = queue.Queue()
        for attack in self.__attack_list:
            q.put('Attempting attack: ' + attack.attack_name())
            threading.Thread(target=attack.execute_attack, args=(q, kwargs), daemon=True).start()
            #self.controller.app.after(3000, self.update())
            while True:
                try:
                    l = q.get(True, timeout=attack.TIMEOUT)
                    yield l
                    if type(l) == AttackResultInfo:
                        yield "Attack done, getting results..."
                        break
                except queue.Empty:
                    break
        yield "Attack plan has finished!"
"""
    

