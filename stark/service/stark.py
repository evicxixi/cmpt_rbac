class StarkConfig(object):
    """docstring for StarkConfig"""

    def __init__(self, model_class):
        self.b = model_class


class AdminSite(object):
    """docstring for AdminSite"""

    def __init__(self, arg):
        self._registry = {}
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, stark_config=None):
        if not stark_config:
            stark_config = StarkConfig

        self._registry[model_class] = stark_config(model_class)


site = AdminSite()

# 最后生self._registry是:
