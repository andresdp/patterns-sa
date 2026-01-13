"""Small mock-data generator for tests and CI.

This generator produces a compact Toy CSV suitable for unit tests and smoke
runs of the example analysis.
"""
import random
import pandas as pd


def generate_toy_csv(path: str, n: int = 100) -> str:
    df = pd.DataFrame({
        "param1": [random.choice([1, 2, 3]) for _ in range(n)],
        "param2": [random.random() for _ in range(n)],
        "latency": [max(0.0, random.gauss(100, 20)) for _ in range(n)],
        "availability": [random.choice([0, 1]) for _ in range(n)],
    })
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="patterns/Toy_Example/sample.csv")
    parser.add_argument("--n", type=int, default=100)
    args = parser.parse_args()
    generate_toy_csv(args.out, args.n)
