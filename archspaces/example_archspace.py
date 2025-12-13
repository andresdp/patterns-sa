import pandas as pd
from ema_workbench import load_results

from collections import Counter
from natsort import natsorted
import itertools

from archspace import ArchSpace


class ToyExample(ArchSpace):

    OUTPUTS = ['cost', 'executionTime', 'probSuccessfulExecution']
    INPUT_PARAMETERS = []

    COST_LABELS = ['cheap', 'average', 'expensive'] #['very-cheap', 'cheap', 'average', 'expensive', 'very-expensive']
    PERFORMANCE_LABELS = ['fast', 'average', 'slow'] #['very-fast', 'fast', 'average', 'low', 'very-low'] #['fast', 'average', 'low']
    RELIABILITY_LABELS = ['highly-reliable', 'average', 'unreliable'] #['unreliable', 'often-unreliable', 'average', 'reliable', 'highly-reliable']

    ALL_TRADEOFF_LABELS = natsorted([','.join(t) for t in itertools.product(*[COST_LABELS, PERFORMANCE_LABELS, RELIABILITY_LABELS])])

    ALL_LABELS = dict()
    ALL_LABELS['executionTime'] = PERFORMANCE_LABELS
    ALL_LABELS['probSuccessfulExecution'] = RELIABILITY_LABELS
    ALL_LABELS['cost'] = COST_LABELS

    def __init__(self):
        # super().__init__()
        self.experiments_df_ = None
        self.outcomes_df_ = None

    def load_results(self, path):
        results = load_results(path)
        self.experiments_df_, outcomes = results
        self.outcomes_df_ = pd.DataFrame(outcomes)

        # Drop void architecture
        config_0_0_0_to_remove = self.experiments_df_[(self.experiments_df_.d1Services==0)&(self.experiments_df_.d2Services==0)&(self.experiments_df_.d3Services==0)].index
        if len(config_0_0_0_to_remove) > 0:
            print("Removing void architecture!", self.experiments_df_.shape, len(self.get_configurations()))
            self.experiments_df_.drop(self.experiments_df_.index[config_0_0_0_to_remove], inplace=True)
            self.experiments_df_.reset_index(drop=True, inplace=True)
            self.outcomes_df_.drop(self.outcomes_df_.index[config_0_0_0_to_remove], inplace=True)
            self.outcomes_df_.reset_index(drop=True, inplace=True)

        return self.experiments_df_, self.outcomes_df_
    
    def get_configurations(self):
        all_configs = set(self.experiments_df_['policy'])
        return list(all_configs)