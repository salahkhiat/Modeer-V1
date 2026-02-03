def staircase(n):
    j = n 
    for _ in range(n): 
        spaces = ' ' * (j - 1)
        j -= 1 
        hashes = '#' * (n - j)
        print(spaces + hashes)

staircase(10)
