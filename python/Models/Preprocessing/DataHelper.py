import os
import numpy as np


def load_participant_data(base_dir):
    # Get each participant directory
    participants = [filename for filename in os.listdir('./') if
                    filename.startswith('participant')]

    participant_data = {}
    for participant in participants:
        bags = np.load('%s/bags.npy' % participant)
        labels = np.load('%s/labels.npy' % participant)

        pid = participant.split("_")[1]
        participant_data[pid] = (bags, labels)

    return participant_data
