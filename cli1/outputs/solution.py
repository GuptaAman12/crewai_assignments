```
def calculate_factorial(n: int) -> int:
    """
    Calculate the factorial of a given non-negative integer.
    
    Args:
        n (int): A non-negative integer.
    
    Returns:
        int: The factorial of n.
    
    Raises:
        ValueError: If n is a negative integer.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    elif n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
```