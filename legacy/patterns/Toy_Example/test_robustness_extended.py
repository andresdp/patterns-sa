from adept import PatternAnalysis
import pandas as pd

def test_robustness_extended():
    json_path = "patterns/Toy_Example/ArchExample_Discretization.json"
    session = PatternAnalysis(json_path)
    session.load(validate_integrity=False)
    session.define_tradeoffs(method='discretization', labels={qa.name: ['low', 'avg', 'high'] for qa in session.get_outcomes()})
    
    # 1. All policies (Global Report)
    print("\n--- Global Robustness Report (All Policies) ---")
    global_df = session.get_robustness_report(decision_key=None, metric='starr')
    print(global_df)

    # 2. Arbitrary set of policies
    target_policies = ["one_device_low", "balanced_low"]
    print(f"\n--- Targeted Robustness Report ({target_policies}) ---")
    targeted_df = session.get_robustness_report(policy_names=target_policies, metric='starr')
    print(targeted_df)

if __name__ == "__main__":
    test_robustness_extended()
