import re

print("Magical Calculater")
print("Type 'quit' for Exit\n")

previous = 0
run = True


def performMath():
    global run
    global previous
    equation = ""

    # make the calculation to be continuous
    if previous == 0:
        equation = input("Enter Equation: ")
    else:
        equation = input(str(previous))

    # Exit Option
    if equation == 'quit':
        print("Goodbye! :)")
        run = False

    # To solve the problem with Eval function
    else:
        equation = re.sub('[a-zA-Z,.:()" "]', '', equation)
        if previous == 0:
            previous = eval(equation)
        else:
            previous = eval(str(previous) + equation)


while run:
    performMath()
