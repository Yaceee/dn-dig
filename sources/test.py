# Python program to demonstrate
# passing dictionary as kwargs


def display(**name):

    print (name["fname"]+" "+name["mname"]+" "+name["lname"])

def main():

    # passing dictionary key-value
    # pair as arguments
    display(fname ="John",
            mname ="F.",
            lname ="Kennedy")
# Driver's code
main()
