def game_sum_8():
    name = input("Hi, what's your name?\n>> ")
    print('Hi ' + name + "\n")

    print("Whats 5 + 3 \n")
    answer = int(input("type your answer\n>> "))
    if answer == 8:
        print("that is correct, good job!\n")
    else:
        print("incorrect, try again.\n")


def guess_the_number():
    from random import randint

    # name = input("Hi, what's your name?\n>> ")
    # print('Hi ' + name + "\n")

    print("Guess a number from 1 to 10, you have 5 tries:")
    secret_number = randint(1, 10)

    tries = 5
    win = False
    while tries > 0:
        answer = int(input("type your guess: "))

        if answer == secret_number:
            win = True
            print("You guessed the number! Great job!\n")
            break
        else:
            print("incorrect, try again.\n")
            tries -= 1

        if abs(secret_number - answer) < 3:
            if win:
                break
            else:
                print("you are close!")


    if tries == 0 or win:
        print("the secrect number was " + str(secret_number))












game_sum_8()
guess_the_number()
