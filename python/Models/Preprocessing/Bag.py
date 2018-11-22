class Bag:
    def __init__(self, pid, start_time, end_time, instances, label) -> None:
        super().__init__()
        self.pid = pid
        self.start_time = start_time
        self.end_time = end_time
        self.instances = instances
        self.label = label