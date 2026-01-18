from typing import Dict, Optional, Tuple, List, Any
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from ..core.models import QualityBin, DiscretizationScheme, QualityObjective


class DataProcessor:
    """Handles the definition of tradeoff regions in the outcome space.
    
    This component is responsible for segmenting continuous outcome data into 
    meaningful regions (tradeoffs) that can be analyzed. It supports multiple 
    paradigms including Discretization, Pareto-based analysis (Nadir, Epsilon, Knee), 
    and Static Thresholds.
    """

    @staticmethod
    def define_tradeoffs(df: pd.DataFrame, method: str = 'discretization', **kwargs) -> Tuple[pd.DataFrame, Any, Dict[str, np.ndarray], Optional[pd.DataFrame]]:
        """Defines tradeoff regions in the outcome space.
        
        Args:
            df: DataFrame containing continuous metrics.
            method: The method to use for definition ('discretization', 'pareto', 'threshold', 'pareto_knee', 'pareto_epsilon').
            **kwargs: Method-specific arguments.
            
        Returns:
            A tuple containing (labeled_df, schemes_metadata, tradeoff_indices, pareto_front_df).
            - labeled_df: DataFrame with categorical labels.
            - schemes_metadata: List of DiscretizationScheme objects.
            - tradeoff_indices: Dictionary mapping tradeoff labels (comma-separated) to numpy arrays of row indices.
            - pareto_front_df: DataFrame containing only the Pareto front (if applicable).
        """
        labeled_df = None
        schemes = []
        pareto_front = None

        if method == 'discretization':
            labeled_df, schemes = DataProcessor._discretize(df, **kwargs)
        elif method == 'clustering':
            labeled_df, schemes = DataProcessor._discretize_kmeans(df, **kwargs)
        elif method in ['pareto', 'pareto_nadir']:
            labels = kwargs.pop('labels', ["pareto-efficient", "sub-optimal"])
            labeled_df, schemes, pareto_front = DataProcessor._pareto_nadir(df, labels=labels,**kwargs)
        elif method == 'threshold':
            labels = kwargs.pop('labels', ["satisfactory", "unsatisfactory"])
            labeled_df, schemes = DataProcessor._static_threshold(df, labels=labels, **kwargs)
        elif method == 'pareto_knee':
            labeled_df, schemes, pareto_front = DataProcessor._pareto_knee(df, **kwargs)
        elif method == 'pareto_epsilon':
            labeled_df, schemes, pareto_front = DataProcessor._pareto_epsilon(df, **kwargs)
        else:
            raise NotImplementedError(f"Tradeoff definition method '{method}' not implemented.")

        # Precompute indices for all labels found in the space
        indices = DataProcessor.get_tradeoff_indices(labeled_df)
        
        return labeled_df, schemes, indices, pareto_front

    @staticmethod
    def get_tradeoff_indices(df: pd.DataFrame, separator: str = ',') -> Dict[str, np.ndarray]:
        """Returns a mapping of tradeoff labels to the row indices that produce them.
        
        Uses efficient pandas grouping to identify data points belonging to each 
        architectural region.
        """
        # observed=True ensures we don't create empty categories
        groups = df.groupby(list(df.columns), observed=True).indices
        
        # Convert tuple keys to comma-separated strings for framework consistency
        return {separator.join(map(str, k)): v for k, v in groups.items()}

    @staticmethod
    def get_tradeoffs(df: pd.DataFrame, separator: str = ',') -> Counter:
        """Counts unique combinations of categorical outcomes using optimized grouping."""
        indices = DataProcessor.get_tradeoff_indices(df, separator)
        return Counter({k: len(v) for k, v in indices.items()})

    @staticmethod
    def _static_threshold(df: pd.DataFrame, params: Dict[str, Any], objectives: List[QualityObjective], labels = ["satisfactory", "unsatisfactory"]) -> Tuple[pd.DataFrame, List[DiscretizationScheme]]:
        """Segments data based on static user-defined thresholds."""
        thresholds = params.get('thresholds', {})
        discrete_df = df.copy()
        schemes = []

        # Map directions (defaults if operator not provided)
        directions = {obj.name: ("max" if obj.maximize else "min") for obj in objectives if obj.name in df.columns}

        for col, thresh_val in thresholds.items():
            if col not in df.columns:
                continue
            
            # 1. Parse Threshold and Operator
            operator = None
            value = thresh_val
            
            if isinstance(thresh_val, (tuple, list)):
                value = thresh_val[0]
                if len(thresh_val) > 1:
                    operator = thresh_val[1]
            
            # 2. Determine Logic based on Operator (or default direction)
            # Default behavior if no operator:
            if operator is None:
                default_dir = directions.get(col, "min")
                if default_dir == "max":
                    operator = ">="
                else:
                    operator = "<="

            # 3. Configure pd.cut
            # Bins are always [-inf, value, inf]
            bins = [-float('inf'), value, float('inf')]
            
            if operator == "<=":
                # Sat: (-inf, val], Unsat: (val, inf]
                current_labels = labels
                right = True
            elif operator == "<":
                # Sat: [-inf, val), Unsat: [val, inf)
                current_labels = labels
                right = False
            elif operator == ">=":
                # Unsat: [-inf, val), Sat: [val, inf)
                current_labels = labels[::-1] # Reverse: [Unsat, Sat]
                right = False
            elif operator == ">":
                # Unsat: (-inf, val], Sat: (val, inf]
                current_labels = labels[::-1] # Reverse: [Unsat, Sat]
                right = True
            else:
                raise ValueError(f"Unknown threshold operator: {operator}")

            discrete_df[col] = pd.cut(discrete_df[col], bins=bins, labels=current_labels, right=right)

            q_bins = [
                QualityBin(label=current_labels[0], min_value=bins[0], max_value=bins[1]),
                QualityBin(label=current_labels[1], min_value=bins[1], max_value=bins[2])
            ]
            schemes.append(DiscretizationScheme(objective_name=col, bins=q_bins, method=f"static_threshold_{operator}"))

        return discrete_df, schemes

    @staticmethod
    def _pareto_epsilon(df: pd.DataFrame, objectives: List[QualityObjective], params: Dict[str, Any]) -> Tuple[pd.DataFrame, List[DiscretizationScheme], pd.DataFrame]:
        """Segments data based on epsilon-dominance distance from Pareto front."""
        try:
            import paretoset
        except ImportError:
            raise ImportError("paretoset library is required.")

        epsilon = params.get('epsilon', 0.0) 
        
        directions = {}
        for obj in objectives:
            if obj.name in df.columns:
                directions[obj.name] = "max" if obj.maximize else "min"
        
        if not directions:
            raise ValueError("No matching objectives found.")

        subset_cols = list(directions.keys())
        sense_list = [directions[col] for col in subset_cols]
        
        mask = paretoset.paretoset(df[subset_cols], sense=sense_list)
        pareto_df = df[mask][subset_cols].copy()
        
        # Normalize using MinMaxScaler
        scaler = MinMaxScaler()
        normalized_df_arr = scaler.fit_transform(df[subset_cols])
        normalized_df = pd.DataFrame(normalized_df_arr, index=df.index, columns=subset_cols)
        
        normalized_pareto_arr = scaler.transform(pareto_df)
        normalized_pareto = pd.DataFrame(normalized_pareto_arr, index=pareto_df.index, columns=subset_cols)

        nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(normalized_pareto)
        distances, indices = nbrs.kneighbors(normalized_df)
        
        is_epsilon_optimal = distances.flatten() <= epsilon
        compliant_df = df[is_epsilon_optimal]
        
        discrete_df = df.copy()
        schemes = []
        for col in subset_cols:
            if not compliant_df.empty:
                opt_min = float(compliant_df[col].min())
                opt_max = float(compliant_df[col].max())
                
                # Add tiny buffer to ensure points on the boundary fall inside
                buffer = 1e-9
                bins = [-float('inf'), opt_min - buffer, opt_max + buffer, float('inf')]
                labels = ["out_low", "epsilon-pareto-optimal", "out_high"]
                
                # Apply per-column discretization to discrete_df
                discrete_df[col] = pd.cut(df[col], bins=bins, labels=labels, include_lowest=True)
                
                q_bins = [
                    QualityBin(label="out_low", min_value=bins[0], max_value=bins[1]),
                    QualityBin(label="epsilon-pareto-optimal", min_value=bins[1], max_value=bins[2]),
                    QualityBin(label="out_high", min_value=bins[2], max_value=bins[3])
                ]
            else:
                q_bins = []

            schemes.append(DiscretizationScheme(
                objective_name=col, 
                bins=q_bins, 
                method="pareto_epsilon"
            ))

        return discrete_df, schemes, df[mask]

    @staticmethod
    def _pareto_knee(df: pd.DataFrame, objectives: List[QualityObjective], params: Dict[str, Any]) -> Tuple[pd.DataFrame, List[DiscretizationScheme], pd.DataFrame]:
        """Segments data to highlight the Knee region of the Pareto front."""
        try:
            import paretoset
        except ImportError:
            raise ImportError("paretoset library is required.")

        directions = {}
        for obj in objectives:
            if obj.name in df.columns:
                directions[obj.name] = "max" if obj.maximize else "min"
        
        subset_cols = list(directions.keys())
        sense_list = [directions[col] for col in subset_cols]
        mask = paretoset.paretoset(df[subset_cols], sense=sense_list)
        pareto_indices = df[mask].index
        pareto_df = df.loc[pareto_indices, subset_cols].copy()
        
        # Normalize using MinMaxScaler
        scaler = MinMaxScaler()
        normalized_pareto_arr = scaler.fit_transform(pareto_df)
        normalized_pareto = pd.DataFrame(normalized_pareto_arr, index=pareto_df.index, columns=subset_cols)
        
        utopia_point = []
        for col in subset_cols:
            target = 1.0 if directions[col] == "max" else 0.0
            utopia_point.append(target)
            
        dists = np.linalg.norm(normalized_pareto - np.array(utopia_point), axis=1)
        min_dist_idx = np.argmin(dists)
        knee_index = pareto_df.index[min_dist_idx]
        
        discrete_df = df.copy()
        labels_series = pd.Series(["off-knee"] * len(df), index=df.index)
        labels_series[knee_index] = "knee"
        
        knee_tolerance = params.get('tolerance', 0.1)
        if knee_tolerance > 0:
             normalized_df_arr = scaler.transform(df[subset_cols])
             normalized_df = pd.DataFrame(normalized_df_arr, index=df.index, columns=subset_cols)
             
             knee_norm = normalized_pareto.loc[knee_index]
             dists_to_knee = np.linalg.norm(normalized_df - knee_norm, axis=1)
             close_points = dists_to_knee <= knee_tolerance
             labels_series[close_points] = "knee"

        compliant_df = df[labels_series == "knee"]

        schemes = []
        for col in subset_cols:
            if not compliant_df.empty:
                k_min = float(compliant_df[col].min())
                k_max = float(compliant_df[col].max())
                
                bins = [-float('inf'), k_min, k_max, float('inf')]
                labels = ["off-knee-low", "knee", "off-knee-high"]
                
                discrete_df[col] = pd.cut(df[col], bins=bins, labels=labels, include_lowest=True)
                
                q_bins = [
                    QualityBin(label="off-knee-low", min_value=bins[0], max_value=bins[1]),
                    QualityBin(label="knee", min_value=bins[1], max_value=bins[2]),
                    QualityBin(label="off-knee-high", min_value=bins[2], max_value=bins[3])
                ]
            else:
                q_bins = []
                
            schemes.append(DiscretizationScheme(
                objective_name=col, 
                bins=q_bins, 
                method="pareto_knee"
            ))

        return discrete_df, schemes, df[mask]

    @staticmethod
    def _pareto_nadir(df: pd.DataFrame, objectives: List[QualityObjective], labels = ["pareto-efficient", "sub-optimal"]) -> Tuple[pd.DataFrame, List[DiscretizationScheme], pd.DataFrame]:
        """Segments data based on the Pareto Front Nadir point."""
        try:
            import paretoset
        except ImportError:
            raise ImportError("paretoset library is required for 'pareto' scheme.")

        directions = {}
        for obj in objectives:
            if obj.name in df.columns:
                directions[obj.name] = "max" if obj.maximize else "min"
        
        if not directions:
            raise ValueError("No matching objectives found in DataFrame for Pareto analysis.")

        subset_cols = list(directions.keys())
        sense_list = [directions[col] for col in subset_cols]
        mask = paretoset.paretoset(df[subset_cols], sense=sense_list)
        pareto_df = df[mask].copy()
        
        discrete_df = df.copy()
        schemes = []
        
        for col, direction in directions.items():
            if direction == "max":
                threshold = float(pareto_df[col].min())
                bins = [-float('inf'), threshold, float('inf')]
                labels1 = labels[::-1] # reverse labels
            else:
                threshold = float(pareto_df[col].max())
                bins = [-float('inf'), threshold, float('inf')]
                labels1 = labels
            
            # print(col,"threshold:", threshold)

            discrete_df[col] = pd.cut(discrete_df[col], bins=bins, labels=labels1)
            q_bins = [
                QualityBin(label=labels1[0], min_value=bins[0], max_value=bins[1]),
                QualityBin(label=labels1[1], min_value=bins[1], max_value=bins[2])
            ]
            schemes.append(DiscretizationScheme(
                objective_name=col,
                bins=q_bins,
                method="pareto_nadir"
            ))
            
        return discrete_df, schemes, pareto_df

    @staticmethod
    def _discretize_kmeans(df: pd.DataFrame, min_k: int = 2, max_k: int = 5, random_state: int = 42, **kwargs) -> Tuple[pd.DataFrame, List[DiscretizationScheme]]:
        """
        Discretizes data using K-Means clustering to find natural groupings.
        Auto-selects the number of bins (k) using Silhouette Score.
        """
        discrete_df = df.copy()
        schemes = []
        
        for col in df.columns:
            # Prepare data (drop NaNs for clustering)
            data = df[col].dropna()
            if len(data) == 0:
                continue

            X = data.values.reshape(-1, 1)
            
            best_score = -1.0
            best_k = min_k
            best_model = None
            
            # 1. Find optimal k
            # If min_k == max_k, skip search
            if min_k == max_k:
                best_k = min_k
                best_model = KMeans(n_clusters=best_k, random_state=random_state, n_init=10)
                best_model.fit(X)
            else:
                search_range = range(min_k, max_k + 1)
                # Can't have more clusters than data points
                search_range = [k for k in search_range if k < len(data)]
                
                if not search_range:
                    # Fallback if data is tiny
                    best_k = 1
                else:
                    for k in search_range:
                        km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
                        labels = km.fit_predict(X)
                        
                        if len(np.unique(labels)) < 2:
                            continue 
                            
                        score = silhouette_score(X, labels)
                        if score > best_score:
                            best_score = score
                            best_k = k
                            best_model = km
            
            if best_model is None and best_k > 1:
                # If loop didn't find valid k (e.g. all scores low or error), try forcing min_k
                try:
                    best_model = KMeans(n_clusters=min_k, random_state=random_state, n_init=10)
                    best_model.fit(X)
                    best_k = min_k
                except Exception:
                    best_k = 1

            if best_k == 1 or best_model is None:
                centroids = [data.mean()]
            else:
                centroids = sorted(best_model.cluster_centers_.flatten())
            
            # 2. Calculate Boundaries (Midpoints)
            # Bins: (-inf, mid1], (mid1, mid2], ..., (midN, inf)
            boundaries = [-float('inf')]
            if best_k > 1:
                for i in range(len(centroids) - 1):
                    mid = (centroids[i] + centroids[i+1]) / 2
                    boundaries.append(mid)
            boundaries.append(float('inf'))
            
            # 3. Create Labels
            # Use "L1", "L2"... or "C1", "C2"
            labels = [f"C{i+1}" for i in range(best_k)]
            
            # 4. Apply Cut
            discrete_df[col] = pd.cut(df[col], bins=boundaries, labels=labels)
            
            # 5. Create Scheme
            q_bins = []
            for i in range(best_k):
                min_v = boundaries[i]
                max_v = boundaries[i+1]
                
                # Display bounds logic
                display_min = min_v if np.isfinite(min_v) else df[col].min()
                display_max = max_v if np.isfinite(max_v) else df[col].max()
                
                q_bins.append(QualityBin(
                    label=labels[i],
                    min_value=float(display_min),
                    max_value=float(display_max)
                ))
                
            schemes.append(DiscretizationScheme(
                objective_name=col,
                bins=q_bins,
                method=f"kmeans_k{best_k}"
            ))
            
        return discrete_df, schemes

    @staticmethod
    def _discretize(df: pd.DataFrame, n_bins: int = 3, ranges: Optional[Dict[str, Tuple[float, float]]] = None, all_labels: Optional[Dict] = None) -> Tuple[pd.DataFrame, List[DiscretizationScheme]]:
        """Internal implementation of discretization logic."""
        discrete_df = df.copy()
        schemes = []
        all_labels = all_labels or {}
        ranges = ranges or {}
        
        for idx, c in enumerate(df.columns):
            qa = df[c]
            min_max = ranges.get(c, (None, None))
            
            qa_bins = DataProcessor.get_bins(qa, n_bins, min_max=min_max)
            
            if c in all_labels:
                labels = all_labels[c]
                if len(labels) != n_bins:
                    raise ValueError(f"Number of labels for '{c}' ({len(labels)}) must match n_bins ({n_bins}).")
            else:
                labels = [f"level_{i+1}" for i in range(n_bins)]
            
            qa_labels = pd.cut(qa, bins=qa_bins, labels=labels)
            discrete_df[c] = qa_labels
            
            bins = []
            for i in range(len(labels)):
                bins.append(QualityBin(
                    label=str(labels[i]),
                    min_value=float(qa_bins[i]),
                    max_value=float(qa_bins[i+1])
                ))
            
            schemes.append(DiscretizationScheme(
                objective_name=c,
                bins=bins
            ))

        return discrete_df, schemes

    @staticmethod
    def get_bins(col: pd.Series, n: int, min_max: Tuple[Optional[float], Optional[float]] = (None, None)) -> list:
        """Calculates bin boundaries for a given numeric column."""
        unique_values = sorted((set(col.values)))
        if min_max == (None, None):
            min_x = np.min(unique_values)
            max_x = np.max(unique_values)
        else:
            min_x = min_max[0]
            max_x = min_max[1]
        
        min_x = min_x - 0.1
        max_x = max_x + 0.1
        delta = (max_x - min_x) / n
        return ([min_x + i * delta for i in range(0, n)] + [max_x])