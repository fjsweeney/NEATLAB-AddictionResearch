class Bag:
    def __init__(self, pid, start_time, end_time, instances, label,
                 feature_labels):
        super().__init__()
        self.feature_labels = feature_labels
        self.pid = pid
        self.start_time = start_time
        self.end_time = end_time
        self.instances = instances
        self.label = label