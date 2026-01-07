from typing import Dict, List
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors


class TradeoffAnalyzer:
    """Explores the solution space by finding similar tradeoffs.
    
    This component uses distance-based metrics (e.g., Euclidean distance between 
    ordinal-encoded category labels) to identify architectural configurations 
    or tradeoff regions that are 'near' a target or reference point.
    """

    def get_nearest_tradeoffs(self, qa_tradeoff: str, available_tradeoffs: List[str], all_labels: Dict[str, List[str]], outputs: List[str], k: int = 5, metric: str = 'euclidean', separator: str = ',') -> List[str]:
        """
        Finds the nearest available tradeoffs to a given reference tradeoff.
        
        Args:
            qa_tradeoff: The target tradeoff string (e.g., 'fast,high').
            available_tradeoffs: List of unique tradeoff strings present in the dataset.
            all_labels: Metadata defining the ordering of labels for each metric.
            outputs: List of output metric names.
            k: Number of neighbors to return.
            
        Returns:
            A list of similar tradeoff strings.
        """
        reference_tradeoff = qa_tradeoff.split(separator)
        tradeoff_list = [qat.split(separator) for qat in available_tradeoffs]
        df = pd.DataFrame(tradeoff_list, columns=outputs) 
        
        # Create ordinal mapper to transform text labels to numeric coordinates
        mapper = dict()
        for c in all_labels.keys():
            mapper[c] = dict()
            value = -1
            for label in all_labels[c]:
                mapper[c][label] = value
                value = value + 1

        for c in df.columns:
            if c in mapper:
                df[c] = df[c].replace(mapper[c]) 
        
        # Initialize KNN engine
        nbrs = NearestNeighbors(n_neighbors=k, metric=metric)
        nbrs.fit(df.values)
        
        # Encode the reference point
        ref_df = pd.DataFrame(np.array(reference_tradeoff).reshape(1, len(outputs)), columns=outputs) 
        for c in ref_df.columns:
            if c in mapper:
                ref_df[c] = ref_df[c].replace(mapper[c])
        
        y = ref_df.loc[0, :].values.tolist()
        distances, indices = nbrs.kneighbors([y])
        
        return [available_tradeoffs[i] for i in indices[0]]