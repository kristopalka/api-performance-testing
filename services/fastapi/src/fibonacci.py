def generate_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1 or n == 2:
        return 1

    a, b = 1, 1
    for _ in range(2, n):
        c = a + b
        a = b
        b = c
    return b
