arr = [-4, 3, -9, 0, 4, 1]

def plus_minus(arr):
    number_of_elements = len(arr)
    positives = 0 
    negatives = 0 
    zeros = 0 
    for n in arr:
        if n > 0:
            positives += 1
        elif n < 0:
            negatives += 1
        else:
            zeros += 1 

    print(f"{positives/number_of_elements:.6f}")
    print(f"{negatives/number_of_elements:.6f}")
    print(f"{zeros/number_of_elements:.6f}")


