def bs (s,n):
    left = 0
    right= len(s) - 1

    while left <= right:
        mid = (left+right)//2

        if s[mid] == n:
            return print(mid)
        elif s[mid] < n:
            left = mid + 1

        else:
            right = mid -1
    return -1

s =[1,2,3,4,5]
n=7

bs(s,n)

