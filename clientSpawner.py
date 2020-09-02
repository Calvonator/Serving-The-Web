import os


def welcome():
    print("\nSpawning clients...\n\n")

    for x in range(2):
        x += 1
        os.system('python3 clientLogin.py ' + str(x))




if __name__ == "__main__":
    welcome()

