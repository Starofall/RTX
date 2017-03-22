# Interface for a change provider
#
# A change provider is able to change the system at runtime


class ChangeProvider:
    def __init__(self, wf):
        pass

    def applyChange(self, message):
        """ message gets send to the system to be applied """
        pass
