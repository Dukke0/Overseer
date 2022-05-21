from Model.Attacks.AbstractAttack import AbstractAttack
import subprocess as sb

class WPSBruteForce(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'WPS Brute Force'

    @classmethod
    def execute_attack(cls):
        pass

class Pixie_Dust(AbstractAttack):

    @classmethod
    def attack_name(cls) -> str:
        return 'Pixie Dust'

    @classmethod
    def execute_attack(cls):
        pass