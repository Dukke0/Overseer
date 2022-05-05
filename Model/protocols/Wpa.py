from Model.protocols.Protocol import AbstractProtocol
from Model.DeauthAttack import DeauthAttack

class WpaProtocol(AbstractProtocol):

    attacks = []

    def __init__(self):
        super().__init__()
