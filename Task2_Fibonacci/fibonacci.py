# Fibonacci Generator Module
# Returns the first n Fibonacci numbers as a list, with input checks and timing.
import timeit


def fibonacci(n):
    """Return a list with the first n Fibonacci numbers."""
    # Input sanitization: n must be a non negative integer
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a whole number, 0 or greater")

    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result


# ------- Test the function --------
tests = [10, 0, -5, "abc"]

for value in tests:
    try:
        print(f"fibonacci({value!r}) =", fibonacci(value))
    except ValueError as e:
        print(f"fibonacci({value!r}) -> Error:", e)

# ------ Runtime benchmark with timeit ------
print("\nBenchmark (1000 runs each):")
sizes = [10, 100, 1000]
for size in sizes:
    t = timeit.timeit(lambda: fibonacci(size), number=1000)
    print(f"n={size}: total {t:.6f}s , average {t / 1000:.8f}s")