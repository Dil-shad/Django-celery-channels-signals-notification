

# Create your tests here.
def test_functions(**kwargs):
   #
    # for i in range(int(args[0])):
    #     print(i)
    print(kwargs)
    return "DONE"


l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
n={'a':'apple'}

test_functions(**n)

