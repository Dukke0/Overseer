from typing import Union
from Model.Attacks.AbstractAttack import AbstractAttack
from Model.Target import Target

class AttackPlan():

    def __init__(self, target=None, attack_list=list()):
        self.__target = target
        self.__attack_list = attack_list

    @property
    def attack_list(self) -> list:
        return self.__attack_list
    
    @attack_list.setter
    def attack_list(self, values: Union[AbstractAttack, list]) -> None:
        self.__attack_list = [values]

    @property
    def target(self) -> Target:
        return self.__target

    @target.setter
    def target(self, target: Target) -> None:
        self.__target = Target
    
    def execute_plan(self) -> list():
        generators_list = list()
        for attack in self.__attack_list:
            generators_list.append(attack.execute_attack())
        print(generators_list)
        return generators_list

 
