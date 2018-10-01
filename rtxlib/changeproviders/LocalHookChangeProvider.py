from rtxlib.changeproviders.ChangeProvider import ChangeProvider


class LocalHookChangeProvider(ChangeProvider):

    def __init__(self, wf, cp):
        self.setParameterHook = cp["setParameterHook"]

    def applyChange(self, message):
        self.setParameterHook(message)
