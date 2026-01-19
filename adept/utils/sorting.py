from typing import List, Dict, Optional, Any

def get_tradeoff_sort_key(label: Any, custom_priorities: Optional[Dict[str, int]] = None):
    """
    Computes a sortable tuple for a single tradeoff label.
    Suitable for use with pandas.Series.map().
    """
    priorities = {
        'fast': 0, 'average': 1, 'slow': 2,
        'high': 0, 'medium': 1, 'low': 2,
        'low_cost': 0, 'high_cost': 1,
        'success': 0, 'failure': 1,
        'optimized': 0, 'baseline': 1
    }
    
    if custom_priorities:
        priorities.update(custom_priorities)

    if not label or not isinstance(label, str):
        return (999, str(label))
        
    parts = label.split('-')
    p1 = parts[0].lower()
    p2 = parts[1].lower() if len(parts) > 1 else ""
    
    return (
        priorities.get(p1, 99), p1, 
        priorities.get(p2, 99), p2
    )

def sort_tradeoff_labels(labels: List[str], custom_priorities: Optional[Dict[str, int]] = None) -> List[str]:
    """Sorts a list of unique labels (e.g., for reindexing a matrix)."""
    return sorted(list(set(labels)), key=lambda l: get_tradeoff_sort_key(l, custom_priorities))