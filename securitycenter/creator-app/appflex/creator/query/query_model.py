class Threshold():
    def __init__(self):
        self.operator = "ge"
        self.value = 0


class Join():
    def __init__(self):
        self.order = 1
        self.kind = ''
        self.field = ''
        self.field_type = ''


class ReferenceTime():
    def __init__(self):
        self.reference_type = ''
        self.value = ''


class Step():
    def __init__(self):
        self.order = 1
        self.kind = ''
        self.reference_time = None
        self.duration = ''
        self.where = ''


class Query():
    def __init__(self):
        self.name = ''
        self.threshold = None
        self.joins = []
        self.steps = []
