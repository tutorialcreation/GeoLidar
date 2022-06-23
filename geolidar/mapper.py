from .constants import state_mapper
class Bunch(object):
    def __init__(self, adict):
        self.__dict__.update(adict)

state_mapper_variables = Bunch(state_mapper)