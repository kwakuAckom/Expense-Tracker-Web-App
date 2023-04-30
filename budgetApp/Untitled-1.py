def bubble_sort(a):
    swap_again = False
    n = len(a)
    while n > 0 and swap_again == False:
        n-=1
        swap_again = True
        for i in range(n):
            if a[i] > a[i+1]:
                a[i], a[i+1] = a[i+1], a[i]
                swap_again == True
    return a

list_a = [2,1,3,6,4,3,5]
bubble_sort(list_a)