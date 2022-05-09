from typing import Union
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.Target import Target

class AttackPlan():

    def __init__(self, target=None, attack_list=list()):
        self.__target = target
        self.__attack_list = attack_list

    @property
    def attack_list(self) -> list:
        return self.__attack_list()
    
    @attack_list.setter
    def attack_list(self, values: Union[AbstractAttack, list]) -> None:

        if type(values) == list:
            for val in range(len(values)):
                self.__attack_list.append(val)
        elif type(values) == AbstractAttack:
            self.__attack_list.append(val)
        else:
            raise TypeError('Value is not an AbstractAttack class or a list') # TODO enforcing types in python!? is it justified?

    @property
    def target(self) -> Target:
        return self.__target

    @target.setter
    def target(self, target: Target) -> None:
        self.__target = Target
    
    def execute_plan(self):
        for attack in self.__attack_list:
            attack.execute_attack()
 
