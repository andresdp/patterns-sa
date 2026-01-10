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

from sklearn.tree._tree import TREE_LEAF, TREE_UNDEFINED
from sklearn.tree import _tree


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
        
        if method == 'rhodium':
            df = self._get_box_limits(box1)[['min', 'max']]
            return box1, df.to_dict(orient='index'), prim_alg
        else:
            df = box1.inspect(style='data')[0][1].to_dict(orient='index')
            clean_df = {}
            for key in df.keys():
                clean_df[key] = {k2:v for (k1,k2),v in df[key].items() if k2 in ['min', 'max']}
            return box1, clean_df, prim_alg

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
        
        return triple_rules, cart_boxes, cart_alg

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
        
        Special handling for 'Discretization' paradigm:
        If kwargs contains 'target_spec' with paradigm='discretization', 
        it creates the target mask 'y' based on 'target_bin'.
        
        Also supports passing a 'Tradeoff' object via 'tradeoff' kwarg.
        """
        tradeoff = kwargs.get('tradeoff')
        target_spec = kwargs.get('target_spec')
        
        # If a first-class Tradeoff object is provided, use its definition
        if tradeoff:
            from ..core.models import Tradeoff
            if not isinstance(tradeoff, Tradeoff):
                 # Handle cases where it might be a dict
                 tradeoff = Tradeoff.model_validate(tradeoff)
            
            supported_schemes = ['discretization', 'pareto', 'threshold', 'pareto_epsilon', 'pareto_knee']
            if tradeoff.scheme in supported_schemes:
                discrete_df = kwargs.get('discrete_outcomes_df')
                if discrete_df is None:
                    raise ValueError(f"discrete_outcomes_df is required for {tradeoff.scheme} tradeoff")
                
                # Create mask y based on all elements in the tradeoff
                y = pd.Series([True] * len(discrete_df), index=discrete_df.index)
                for obj_name, target_label in tradeoff.elements.items():
                    if obj_name in discrete_df.columns:
                        y = y & (discrete_df[obj_name] == target_label)
                
                if method == 'cart':
                    kwargs['discrete_outcomes'] = y
                else:
                    kwargs['y_mask'] = y

        elif target_spec and target_spec.get('paradigm') == 'discretization':
            target_bin = target_spec.get('target_bin')
            discrete_df = kwargs.get('discrete_outcomes_df')
            
            if discrete_df is None:
                raise ValueError("discrete_outcomes_df is required for discretization paradigm")
            
            # Create mask y based ONLY on the target outcome column
            if outcome in discrete_df.columns:
                y = (discrete_df[outcome] == target_bin)
            else:
                # If outcome name doesn't match directly, it might be a multi-dimensional tradeoff label
                # In that case, we fall back to the string representation of the whole row
                from .discretization import DataProcessor
                temp = discrete_df.to_string(header=False, index=False, index_names=False).split('\n')
                row_labels = [','.join(ele.split()) for ele in temp]
                y = pd.Series([label == target_bin for label in row_labels], index=discrete_df.index)
            
            if method == 'cart':
                kwargs['discrete_outcomes'] = y
            else:
                kwargs['y_mask'] = y

        strategy = self.get_strategy(method)
        return strategy.discover(experiments_df, outcomes_df, **kwargs)


__all__ = ["ScenarioDiscovery", "PRIMDiscovery", "CARTDiscovery", "ScenarioDiscoveryManager"]