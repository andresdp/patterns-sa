from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from collections import Counter
from operator import itemgetter

# EMA Workbench and Sklearn imports
try:
    from ema_workbench.analysis import prim
    from ema_workbench.analysis import cart
    from ema_workbench.analysis.scenario_discovery_util import RuleInductionType
    import prim as rhodium_prim
except ImportError:
    # Allow running without these if strictly testing structure
    pass

from pydantic import BaseModel, Field
from sklearn.tree._tree import TREE_LEAF, TREE_UNDEFINED
from sklearn.tree import _tree

from .robustness import RobustnessAnalyzer
from ..core.models import Box

# Import custom exceptions
try:
    from ..utils.exceptions import DiscoveryError, TradeoffDefinitionError
except ImportError:
    # Fallback for backward compatibility
    class DiscoveryError(Exception):
        pass
    class TradeoffDefinitionError(Exception):
        pass


class BoxEvaluator:
    """Computes performance metrics for discovered boxes on independent datasets."""
    
    @staticmethod
    def evaluate(box_limits: Dict[str, Dict[str, float]], X: pd.DataFrame, y: pd.Series, population_prevalence: float = 0.0) -> Dict[str, float]:
        """
        Evaluates a box against a target mask y.
        
        Args:
            box_limits: Dict of {param: {'min': float, 'max': float}}
            X: Feature matrix
            y: Binary target mask
            population_prevalence: The baseline % of target in the original space (e.g. Train set).
        """
        if X.empty or y.empty:
            return {'density': 0.0, 'coverage': 0.0, 'population_prevalence': population_prevalence}
            
        # 1. Identify rows in X that satisfy all box_limits
        mask = pd.Series(True, index=X.index)
        for param, limits in box_limits.items():
            if param in X.columns:
                mask &= (X[param] >= limits['min']) & (X[param] <= limits['max'])
        
        # 2. Compute metrics
        points_in_box = mask.sum()
        targets_in_box = (mask & y).sum()
        total_targets = y.sum()
        
        density = targets_in_box / points_in_box if points_in_box > 0 else 0.0
        coverage = targets_in_box / total_targets if total_targets > 0 else 0.0
        
        # Lift is how much better we are than the baseline
        # lift = (density / population_prevalence) if population_prevalence > 0 else 0.0
        lift = density - population_prevalence # This can be a positive or negative improvement
        
        return {
            'density': float(density),
            'coverage': float(coverage),
            'population_prevalence': float(population_prevalence),
            'lift': float(lift),
            'samples_in_box': int(points_in_box),
            'targets_in_box': int(targets_in_box)
        }

    @staticmethod
    def compute_policy_robustness_matrix(
        experiments_df: pd.DataFrame,
        outcomes_df: pd.DataFrame,
        discrete_df: pd.DataFrame,
        policy_series: pd.Series,
        tradeoffs: List[Any],
        boxes: List[Optional[Box]],
        schemes: List[Any],
        metric: str = 'starr',
        stats: Optional[Dict[str, Any]] = None,
        min_samples: int = 1
    ) -> pd.DataFrame:
        """
        Computes a matrix of Policy vs. Tradeoff robustness under box constraints.
        
        Args:
            experiments_df: Parameter DataFrame.
            outcomes_df: Continuous outcomes DataFrame.
            discrete_df: Discretized outcomes DataFrame.
            policy_series: Series mapping row indices to policy names.
            tradeoffs: List of Tradeoff objects.
            boxes: List of Box objects (one per tradeoff, or None).
            schemes: List of DiscretizationScheme objects.
            metric: 'starr' or 'regret'.
            stats: Optional scaler info for REGRET calculation.
            min_samples: Minimum points required to calculate the metric.
            
        Returns:
            pd.DataFrame: Rows=Policies, Cols=Tradeoffs, Values=Metric.
        """
        policies = sorted(policy_series.dropna().unique())
        results = {t.name: [] for t in tradeoffs}
        
        metric = metric.lower()
        
        for i, tradeoff in enumerate(tradeoffs):
            box = boxes[i]
            
            # If no box for this tradeoff, mark entire column as None
            if box is None:
                for _ in policies:
                    results[tradeoff.name].append(None)
                continue
                
            # Pre-calculate boundaries for REGRET if needed
            boundaries = {}
            if metric == 'regret':
                for obj_name, target_label in tradeoff.elements.items():
                    scheme = next((s for s in schemes if s.objective_name == obj_name), None)
                    if scheme:
                        bin_obj = next((b for b in scheme.bins if b.label == target_label), None)
                        if bin_obj:
                            boundaries[obj_name] = {'min': bin_obj.min_value, 'max': bin_obj.max_value}

            # Pre-calculate overall success mask for this tradeoff
            is_success_overall = pd.Series(True, index=discrete_df.index)
            for obj_name, target_label in tradeoff.elements.items():
                if obj_name in discrete_df.columns:
                    is_success_overall &= (discrete_df[obj_name] == target_label)

            for policy in policies:
                # 1. Filter data for this policy
                policy_mask = (policy_series == policy)
                exp_pol = experiments_df[policy_mask]
                out_pol = outcomes_df[policy_mask]
                succ_pol = is_success_overall[policy_mask]
                
                # 2. Apply Box Constraints
                box_mask = pd.Series(True, index=exp_pol.index)
                for param, limits in box.limits.items():
                    if param in exp_pol.columns:
                        box_mask &= (exp_pol[param] >= limits['min']) & (exp_pol[param] <= limits['max'])
                
                n_samples = box_mask.sum()
                
                # 3. Calculate Metric
                if n_samples < min_samples:
                    val = 0.0 if (metric == 'starr' or metric == 'density') else 10.0
                else:
                    if metric == 'starr' or metric == 'density':
                        val = RobustnessAnalyzer.compute_starr(succ_pol[box_mask])['value']
                    elif metric == 'regret':
                        val = RobustnessAnalyzer.compute_regret(
                            out_pol[box_mask], succ_pol[box_mask], boundaries, stats
                        )['value']
                    else:
                        val = None
                
                results[tradeoff.name].append(val)
                
        return pd.DataFrame(results, index=policies)


class ScenarioDiscovery(ABC):
    """Abstract base class for scenario discovery algorithms.
    
    Scenario discovery aims to identify 'boxes' or 'rules' in the parameter space 
    that reliably lead to specific outcomes (e.g., finding the range of 
    server counts that guarantee fast response time).
    """
    @abstractmethod
    def discover(self, experiments_df: pd.DataFrame, outcomes_df: pd.DataFrame, **kwargs) -> Any:
        """Run scenario discovery algorithm."""


class PRIMDiscovery(ScenarioDiscovery):
    """Implementation of the Patient Rule Induction Method (PRIM).
    
    PRIM iteratively 'peels' the parameter space to find a high-density region 
    (box) that satisfies a target outcome condition.
    """
    def discover(self, experiments_df: pd.DataFrame, outcomes_df: pd.DataFrame, **kwargs) -> Any:
        """
        Runs PRIM analysis.
        
        Args:
            experiments_df: DataFrame of input parameters (Levers/Uncertainties).
            outcomes_df: DataFrame of performance metrics.
            **kwargs:
                property: Dict mapping outcome name to (min, max) ROI.
                threshold: Minimum density/coverage threshold.
                method: 'rhodium' or 'ema' backend.
        """
        property = kwargs.get('property')
        threshold = kwargs.get('threshold', 0.8)
        method = kwargs.get('method', 'rhodium')
        key_parameters = kwargs.get('key_parameters')
        n_boxes = kwargs.get('n_boxes', False)
        verbose = kwargs.get('verbose', True)
        
        y = kwargs.get('y_mask')
        
        if y is None:
            if property is None:
                 raise ValueError("Either 'property' or 'y_mask' must be defined for PRIM")

            # Construct ROI mask
            y = pd.Series([True] * len(outcomes_df), index=outcomes_df.index)
            for outcome, (min_val, max_val) in property.items():
                if outcome in outcomes_df.columns:
                    y = y & (outcomes_df[outcome] >= min_val) & (outcomes_df[outcome] <= max_val)
        
        x = experiments_df.copy()
        to_drop = ['policy', 'model', 'scenario']
        x = x.drop(columns=[c for c in to_drop if c in x.columns])
        
        if key_parameters is not None:
             x = x[key_parameters]

        if verbose:
            print('Instances satisfying property:', y.value_counts())
            print("Total instances:", x.shape)
            print("Running PRIM ...", method)

        if not y.any():
            if verbose:
                print("No instances satisfy the target property. Skipping PRIM.")
            if n_boxes:
                return []
            return None

        if method == 'rhodium':
            prim_alg = rhodium_prim.Prim(x, y, threshold=threshold)
            all_boxes = prim_alg.find_all()
        else:
            prim_alg = prim.Prim(x, y, threshold=threshold)
            box = prim_alg.find_box()
            all_boxes = [box]

        if verbose:
            print(len(all_boxes), 'possible boxes')
            
        if n_boxes:
            return all_boxes
        
        if not all_boxes:
            return None

        box1 = all_boxes[0]
        
        # Populate target_tradeoff if available
        target_name = None
        if 'tradeoff' in kwargs:
            target_name = kwargs['tradeoff'].name
        elif 'target_spec' in kwargs:
            target_name = kwargs['target_spec'].get('target_bin')

        if method == 'rhodium':
            df = self._get_box_limits(box1)[['min', 'max']]
            box_obj = Box(limits=df.to_dict(orient='index'), method="prim", target_tradeoff=target_name)
            # Rhodium boxes don't have built-in metrics dict in the same way, we might need to compute them or extract them
            # For now, we return the Box object which wraps the limits. 
            # Ideally we should populate metrics using BoxEvaluator or extract from box1 stats.
            # The current implementation returns (box1, df, prim_alg) tuple in original code.
            # To be backward compatible but return Box objects, we might need to wrap it.
            # But the user asked to "return the Box objects".
            # The original code returned: return box1, df.to_dict(orient='index'), prim_alg
            # I will modify it to return a list of Box objects or a single Box object?
            # The interface says "Any".
            # Let's keep the return signature but ensure the Box object is created if we were returning objects.
            # Wait, the previous code returned TUPLES. 
            # "When returning results ... I'd like to return the Box objects"
            # I should change the return type to List[Box].
            
            metrics = {
                "density": box1.peeling_trajectory.iloc[box1._cur_box]['density'],
                "coverage": box1.peeling_trajectory.iloc[box1._cur_box]['coverage'],
                "mean": box1.peeling_trajectory.iloc[box1._cur_box]['mean'],
                "mass": box1.peeling_trajectory.iloc[box1._cur_box]['mass']
            }
            box_obj.metrics = metrics
            return [box_obj] # Return list of Box objects
            
        else:
            # EMA Workbench Box
            df = box1.inspect(style='data')[0][1].to_dict(orient='index')
            clean_df = {}
            for key in df.keys():
                clean_df[key] = {k2:v for (k1,k2),v in df[key].items() if k2 in ['min', 'max']}
            
            box_obj = Box(limits=clean_df, method="prim", target_tradeoff=target_name)
            # EMA box metrics extraction might be different
            # For now, returning Box object
            return [box_obj]

    @staticmethod
    def _get_box_limits(box):
        """Extracts numeric bounds from a Rhodium/PRIM box object."""
        stats = box.peeling_trajectory.iloc[box._cur_box].to_dict()
        stats['restricted_dim'] = stats['res dim']

        qp_values = box._calculate_quasi_p(box._cur_box)
        
        uncs = [(key, value) for key, value in qp_values.items()]
        uncs.sort(key=itemgetter(1))
        uncs = [uncs[0] for uncs in uncs]
        
        box_lim = pd.DataFrame(np.zeros((len(uncs), 3)), 
                               index=uncs, 
                               columns=['min', 'max', 'qp values'])
        
        for unc in uncs:
            values = box._box_lims[box._cur_box][unc][:]
            box_lim.loc[unc] = [values[0], values[1], qp_values[unc]]
             
        return box_lim


class CARTDiscovery(ScenarioDiscovery):
    """Implementation of Classification And Regression Trees (CART) for scenario discovery.
    
    CART partitions the parameter space into hyper-rectangles by recursively 
    splitting on parameters that best separate different outcome classes.
    """
    def discover(self, experiments_df: pd.DataFrame, outcomes_df: pd.DataFrame, **kwargs) -> Any:
        """
        Runs CART analysis.
        
        Args:
            experiments_df: DataFrame of input parameters.
            outcomes_df: DataFrame of outcomes.
            **kwargs:
                discrete_outcomes: Series of categorical labels (Required).
                prune_tree: Whether to simplify the resulting tree.
        """
        key_parameters = kwargs.get('key_parameters')
        prune_tree = kwargs.get('prune_tree', False)
        mass_min = kwargs.get('mass_min')
        y = kwargs.get('discrete_outcomes')
        
        if y is None:
             raise ValueError("discrete_outcomes (y) is required for CART")

        x = experiments_df.copy()
        to_drop = ['policy', 'model', 'scenario']
        x = x.drop(columns=[c for c in to_drop if c in x.columns])
        
        if key_parameters is not None:
            x = x[key_parameters]
            
        if mass_min is None:
            mass_min =  2.0 / x.shape[0]
            
        cart_alg = cart.CART(x, y, mass_min, mode=RuleInductionType.CLASSIFICATION)
        cart_alg.build_tree(random_state=42)

        if prune_tree:
            cart_alg.clf = self._prune_duplicate_leaves(cart_alg.clf)

        class_names = kwargs.get('class_names') 
        if class_names is None:
             class_names = [str(i) for i in sorted(pd.unique(y))]

        string_rules, triple_rules = self._get_rules(cart_alg.clf, feature_names=x.columns, class_names=class_names)
        
        cart_boxes = self._extract_boxes(triple_rules)
        
        # Convert to Box objects
        box_objects = []
        for label, limits in cart_boxes.items():
             # Extract metrics from rules if possible, but CART metrics are usually class probabilities
             # For now, just limits. Evaluation happens downstream.
             box = Box(limits=limits, target_tradeoff=str(label), method='cart')
             box_objects.append(box)
             
        return box_objects

    def _extract_boxes(self, triple_rules):
        """Converts tree rules into parameter bound 'boxes'."""
        cart_boxes = dict()
        for t in triple_rules:
            qa_label = t[-1][1]
            if qa_label not in cart_boxes.keys():
                cart_boxes[qa_label] = []
            vars_ = set([x[1] for x in t[0:-1]])
            vars_ranges = dict()
            for v in vars_:
                vrange = self._intersect_intervals_from_paths([t[0:-1]], v, min_bound=0, max_bound=None)
                if vrange is not None:
                    vars_ranges[v] = {'min': vrange[0], 'max': vrange[1]}
            if len(vars_ranges.keys()) > 0:
                cart_boxes[qa_label].append(vars_ranges)
        
        final_boxes = {}
        for qa_label, boxes in cart_boxes.items():
            if boxes:
                final_boxes[qa_label] = boxes[0]
        return final_boxes

    @staticmethod
    def _is_leaf(inner_tree, index):
        return (inner_tree.children_left[index] == TREE_LEAF and 
            inner_tree.children_right[index] == TREE_LEAF)

    @staticmethod
    def _prune_index(inner_tree, decisions, index=0):
        if not CARTDiscovery._is_leaf(inner_tree, inner_tree.children_left[index]):
            CARTDiscovery._prune_index(inner_tree, decisions, inner_tree.children_left[index])
        if not CARTDiscovery._is_leaf(inner_tree, inner_tree.children_right[index]):
            CARTDiscovery._prune_index(inner_tree, decisions, inner_tree.children_right[index])

        if (CARTDiscovery._is_leaf(inner_tree, inner_tree.children_left[index]) and
            CARTDiscovery._is_leaf(inner_tree, inner_tree.children_right[index]) and
            (decisions[index] == decisions[inner_tree.children_left[index]]) and 
            (decisions[index] == decisions[inner_tree.children_right[index]])):
            inner_tree.children_left[index] = TREE_LEAF
            inner_tree.children_right[index] = TREE_LEAF
            inner_tree.feature[index] = TREE_UNDEFINED

    @staticmethod
    def _prune_duplicate_leaves(mdl):
        """Simplifies the tree by merging leaves that make the same classification."""
        decisions = mdl.tree_.value.argmax(axis=2).flatten().tolist()
        CARTDiscovery._prune_index(mdl.tree_, decisions)
        return mdl

    @staticmethod
    def _get_rules(tree, feature_names, class_names):
        """Extracts human-readable rules from a trained scikit-learn tree."""
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        paths = []
        path = []
        
        def recurse(node, path, paths):
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                p1, p2 = list(path), list(path)
                p1 += [('<=', name, np.round(threshold, 3))]
                recurse(tree_.children_left[node], p1, paths)
                p2 += [('>', name, np.round(threshold, 3))]
                recurse(tree_.children_right[node], p2, paths)
            else:
                path += [(tree_.value[node], tree_.n_node_samples[node])]
                paths += [path]
                
        recurse(0, path, paths)

        samples_count = [p[-1][1] for p in paths]
        ii = list(np.argsort(samples_count))
        paths = [paths[i] for i in reversed(ii)]
        
        rules = []
        triples = []
        for path in paths:
            rule = "if "
            tuple_rule = []
            for p in path[:-1]:
                tuple_rule.append(p)
                if rule != "if ":
                    rule += " and "
                rule += p[1] + " " + p[0] + " " + str(p[2])
            rule += " then "
            
            classes = path[-1][0][0]
            l = np.argmax(classes)
            if class_names is not None and l < len(class_names):
                prob_class = np.round(classes[l]/np.sum(classes),2)
                rule += f"class: {class_names[l]} (proba: {100.0*prob_class}%)"
                tuple_rule.append(('class', class_names[l], prob_class))
            else:
                rule += f"class index: {l}"
                tuple_rule.append(('class', l, 1.0))
                
            rule += f" | based on {path[-1][1]:,} samples"
            rules += [rule]
            triples.append(tuple_rule)
            
        return rules, triples

    @staticmethod 
    def _intersect_intervals_from_paths(paths, variable_name, min_bound=None, max_bound=None):
        """Calculates the intersection of multiple constraints on a single parameter."""
        if min_bound is None:
            min_bound = float('-inf')
        if max_bound is None:
            max_bound = float('inf')

        for path in paths:
            for (operator, var_name, value) in path:
                if var_name == variable_name:
                    if operator == '<=':
                        max_bound = min(max_bound, value)
                    elif operator == '<':
                        max_bound = min(max_bound, value - 1e-9)
                    elif operator == '>=':
                        min_bound = max(min_bound, value)
                    elif operator == '>':
                        min_bound = max(min_bound, value + 1e-9)

        if min_bound > max_bound:
            return None

        return (min_bound, max_bound)


class ScenarioDiscoveryManager:
    """Registry and factory for scenario discovery strategies.
    
    Allows the framework to switch between different discovery backends 
    (e.g., PRIM, CART) through a unified interface.
    """
    
    def __init__(self):
        self._strategies = {
            'prim': PRIMDiscovery,
            'cart': CARTDiscovery
        }

    def get_strategy(self, method: Optional[str]) -> ScenarioDiscovery:
        """Retrieves a discovery strategy by name."""
        if method is None:
            method = 'prim'
        
        strategy_class = self._strategies.get(method.lower())
        if strategy_class:
            return strategy_class()
        
        return PRIMDiscovery()

    def discover(self, experiments_df: pd.DataFrame, outcomes_df: pd.DataFrame, outcome: str, method: Optional[str] = None, **kwargs) -> Any:
        """Delegates discovery to the selected strategy.
        
        Handles different tradeoff paradigms and prepares the target mask 'y'
        for scenario discovery algorithms.
        
        Args:
            experiments_df: DataFrame of input parameters
            outcomes_df: DataFrame of outcomes
            outcome: Name of the target outcome
            method: Discovery method ('prim' or 'cart')
            **kwargs: Additional parameters including:
                - tradeoff: Tradeoff object for complex tradeoff definitions
                - target_spec: Specification for target-based discovery
                - discrete_outcomes_df: DataFrame with discretized outcomes
                
        Returns:
            Result from the selected discovery strategy
            
        Raises:
            DiscoveryError: If discovery setup fails
            TradeoffDefinitionError: If tradeoff configuration is invalid
        """
        self._validate_inputs(experiments_df, outcomes_df, outcome)
        
        # Handle tradeoff-based discovery
        if 'tradeoff' in kwargs:
            self._handle_tradeoff_based_discovery(kwargs, method)
        
        # Handle target specification-based discovery
        elif 'target_spec' in kwargs:
            self._handle_target_spec_discovery(kwargs, outcome, method)
        
        # Validate that required parameters are set
        self._validate_discovery_parameters(kwargs, method)
        
        strategy = self.get_strategy(method)
        return strategy.discover(experiments_df, outcomes_df, **kwargs)
    
    def _validate_inputs(self, experiments_df: pd.DataFrame, outcomes_df: pd.DataFrame, outcome: str) -> None:
        """Validates input DataFrames and parameters."""
        if experiments_df is None or outcomes_df is None:
            raise DiscoveryError("Input DataFrames cannot be None")
        
        if not isinstance(experiments_df, pd.DataFrame) or not isinstance(outcomes_df, pd.DataFrame):
            raise DiscoveryError("Inputs must be pandas DataFrames")
        
        if experiments_df.empty or outcomes_df.empty:
            raise DiscoveryError("Input DataFrames cannot be empty")
        
        if not outcome or not isinstance(outcome, str):
            raise DiscoveryError("Outcome must be a non-empty string")
    
    def _handle_tradeoff_based_discovery(self, kwargs: Dict[str, Any], method: Optional[str]) -> None:
        """Handles discovery based on Tradeoff objects."""
        tradeoff = kwargs.get('tradeoff')
        
        try:
            from ..core.models import Tradeoff
            if not isinstance(tradeoff, Tradeoff):
                tradeoff = Tradeoff.model_validate(tradeoff)
            kwargs['tradeoff'] = tradeoff
        except Exception as e:
            raise TradeoffDefinitionError(f"Invalid tradeoff definition: {str(e)}")
        
        supported_schemes = ['discretization', 'pareto', 'threshold', 'pareto_epsilon', 'pareto_knee']
        if tradeoff.scheme not in supported_schemes:
            raise TradeoffDefinitionError(f"Unsupported tradeoff scheme: {tradeoff.scheme}")
        
        discrete_df = kwargs.get('discrete_outcomes_df')
        if discrete_df is None:
            raise DiscoveryError(f"discrete_outcomes_df is required for {tradeoff.scheme} tradeoff")
        
        # Create mask y based on all elements in the tradeoff
        y = pd.Series([True] * len(discrete_df), index=discrete_df.index)
        for obj_name, target_label in tradeoff.elements.items():
            if obj_name in discrete_df.columns:
                y = y & (discrete_df[obj_name] == target_label)
        
        if method == 'cart':
            kwargs['discrete_outcomes'] = y
        else:
            kwargs['y_mask'] = y
    
    def _handle_target_spec_discovery(self, kwargs: Dict[str, Any], outcome: str, method: Optional[str]) -> None:
        """Handles discovery based on target specifications."""
        target_spec = kwargs.get('target_spec')
        
        if target_spec.get('paradigm') != 'discretization':
            raise DiscoveryError(f"Unsupported target specification paradigm: {target_spec.get('paradigm')}")
        
        target_bin = target_spec.get('target_bin')
        if not target_bin:
            raise DiscoveryError("target_bin is required for discretization paradigm")
        
        discrete_df = kwargs.get('discrete_outcomes_df')
        if discrete_df is None:
            raise DiscoveryError("discrete_outcomes_df is required for discretization paradigm")
        
        # Create mask y based on the target outcome column
        if outcome in discrete_df.columns:
            y = (discrete_df[outcome] == target_bin)
        else:
            # Fallback for multi-dimensional tradeoff labels
            from .discretization import DataProcessor
            temp = discrete_df.to_string(header=False, index=False, index_names=False).split('\n')
            row_labels = [','.join(ele.split()) for ele in temp]
            y = pd.Series([label == target_bin for label in row_labels], index=discrete_df.index)
        
        if method == 'cart':
            kwargs['discrete_outcomes'] = y
        else:
            kwargs['y_mask'] = y
    
    def _validate_discovery_parameters(self, kwargs: Dict[str, Any], method: Optional[str]) -> None:
        """Validates that required parameters are set for the chosen method."""
        if method == 'cart':
            if 'discrete_outcomes' not in kwargs:
                raise DiscoveryError("discrete_outcomes is required for CART method")
        else:  # PRIM or other methods
            if 'y_mask' not in kwargs:
                raise DiscoveryError("y_mask is required for PRIM method")


__all__ = ["ScenarioDiscovery", "PRIMDiscovery", "CARTDiscovery", "ScenarioDiscoveryManager", "Box", "BoxEvaluator"]