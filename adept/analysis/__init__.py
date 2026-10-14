from .discretization import DataProcessor
from .robustness import RobustnessAnalyzer
from .tradeoffs import TradeoffAnalyzer
from .discovery import ScenarioDiscoveryManager
from .explainer import ExplanationManager
from .box_quality import (
    BoxDuplicateMatch,
    BoxFitness,
    calculate_box_fitness,
    identify_duplicate_boxes,
    rank_box_results,
    rank_box_results_globally,
)

__all__ = [
    "DataProcessor",
    "RobustnessAnalyzer",
    "TradeoffAnalyzer",
    "ScenarioDiscoveryManager",
    "ExplanationManager",
    "BoxDuplicateMatch",
    "BoxFitness",
    "calculate_box_fitness",
    "identify_duplicate_boxes",
    "rank_box_results",
    "rank_box_results_globally",
]
