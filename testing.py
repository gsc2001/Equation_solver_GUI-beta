from solver import get_solution
def get_solve():
    global solution
    try:
        solution = get_solution()
    except:
        print('Error while solving')


    if solution[0] == ('*',0.0):
        print('Error')
    else:
        print("Solution:")
        for var, sol in solution:
            print("{} = {}".format(var, sol))
