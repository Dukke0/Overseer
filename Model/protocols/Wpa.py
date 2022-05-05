from Model.protocols.Protocol import AbstractProtocol
from Model.Attacks.DeauthAttack import DeauthAttack

class WpaProtocol(AbstractProtocol):
    #class attribute
    __protocol_attacks = (DeauthAttack)

    def __init__(self):
        super().__init__()
    
