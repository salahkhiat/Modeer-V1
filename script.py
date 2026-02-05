nums = [5, 5, 5, 5, 5]

def get_min_max(arr):
    maximum = arr[0]
    minimum = arr[0]
    
    for i in range(len(arr)-1):

        if arr[i + 1] > maximum:
            maximum = arr[i + 1]

        if arr[i + 1] < minimum:
            minimum = arr[i + 1]
    return (maximum, minimum)

def maxMinSum(arr):
    sums = []
    for outer_i in range(len(arr)):
        a_sum = 0 

        for inner_i in range(len(arr)):
            if inner_i != outer_i:
                a_sum += arr[inner_i]
        sums.append(a_sum) 
    
    maximum, minimum = get_min_max(sums)
    print(f"{minimum} {maximum}")

maxMinSum(nums)




"""

def miniMaxSum(arr):
    # Write your code here
    sums = []
    for outer in arr:
        a_sum = 0 

        for inner in arr:
            if inner != outer:
                a_sum += inner
        sums.append(a_sum) 
    
    maximum, minimum = get_min_max(sums)
    print(f"{minimum} {maximum}")

"""