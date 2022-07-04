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
        self.__threads_running = list()
        self.controller = controller

    @property
    def attack_list(self) -> list:
        return self.__attack_list
    
    @attack_list.setter
    def attack_list(self, values: Union[AbstractAttack, list]) -> None:
        self.__attack_list = [values]

    def add_attack(self, attack: AbstractAttack) -> None:
        '''
        Adds an attack to the list
        '''
        if attack not in self.__attack_list:
            self.__attack_list.append(attack)
    
    def remove_attack(self, attack: AbstractAttack) -> None:
        '''
        Removes an attack form the list
        '''
        if attack in self.__attack_list:
            self.__attack_list.remove(attack)

    @property
    def target(self) -> Target:
        return self.__target

    @target.setter
    def target(self, target: Target) -> None:
        self.__target = Target
    
    def execute_plan(self, q, kwargs) -> list():
        '''
        Creates one thread for every attack, starts it and every 2 seconds notifies the controller to check
        the queue
        '''
        self.__threads_running = list()
        for attack in self.__attack_list:
            q.put('Attempting attack: ' + attack.attack_name())
            t = threading.Thread(target=attack.execute_attack, args=(q, kwargs), daemon=True)
            self.__threads_running.append(t)
            t.start()
            self.update(q, threads=self.__threads_running)
        q.put(self.END_MESSAGE)
        self.controller.attack_notification(q=q)

    def update(self, q, threads):
        '''
        Notify the controller to check the queue
        '''
        while True:

            if not threads:
                break 

            threads = [t for t in threads if t.is_alive()]
            time.sleep(2)
            self.controller.attack_notification(q=q)


    