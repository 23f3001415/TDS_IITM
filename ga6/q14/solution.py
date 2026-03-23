import math


def main() -> None:
    p = 0.9400
    n_test = 2000
    rounds = 50

    sigma = math.sqrt(p * (1 - p) / n_test)
    inflation_pp = sigma * math.sqrt(2 * math.log(rounds)) * 100
    adjusted_accuracy = p * 100 - inflation_pp

    print(f"{sigma:.6f},{inflation_pp:.3f},{adjusted_accuracy:.3f}")


if __name__ == "__main__":
    main()
