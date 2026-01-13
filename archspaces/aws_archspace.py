
import pandas as pd

from archspace import ArchSpace


class AWS_Microservices(ArchSpace):

    OUTPUTS = ['latency', 'availability']
    INPUT_PARAMETERS = []
    SEPARATOR = '#'

    AVAILABILITY_LABELS = ['low', 'average', 'high']

    ALL_LABELS = dict()
    ALL_LABELS['latency'] = ArchSpace.RESPONSE_TIME_LABELS
    ALL_LABELS['availability'] = AVAILABILITY_LABELS
        
    CONFIGURATION_PARAMETERS = {
        'temporal1': INPUT_PARAMETERS,
        'temporal2': INPUT_PARAMETERS,
        'low_traffic': INPUT_PARAMETERS,
        'high_traffic': INPUT_PARAMETERS
    }

    def __init__(self):
        # super().__init__()
        self.experiments_df_ = None
        self.outcomes_df_ = None    
        
    def load_results(self, path, target='PetSite'):

        df = pd.read_csv(path)
        print(df.shape) 

        qas = [o for o in self.OUTPUTS if (o+self.SEPARATOR+target) in df.columns]
        print("QAS:", qas)
        self.OUTPUTS = qas
        outputs = [o+self.SEPARATOR+target for o in qas]
        self.INPUT_PARAMETERS = [i for i in df.columns if (i not in outputs) and (i not in ['traffic', 'issue'])]

        self.experiments_df_ = df[self.INPUT_PARAMETERS + ['issue']].copy()
        self.experiments_df_.set_index('issue', inplace=True)
        self.experiments_df_.index.name = 'scenario' # TODO: Could scenario refer to the issue?
        self.experiments_df_.reset_index(inplace=True)
        self.experiments_df_['model'] = 'aws_microservices'
        self.experiments_df_['policy'] = df['traffic'].copy()
        self.experiments_df_['policy'] = self.experiments_df_['policy'].astype('category')

        self.outcomes_df_ = df[outputs].copy()
        self.outcomes_df_.columns = qas

        return self.experiments_df_, self.outcomes_df_
    
    def get_configurations(self):
        all_configs = set(self.experiments_df_['policy'])
        return list(all_configs) #[[x] for x in all_configs]