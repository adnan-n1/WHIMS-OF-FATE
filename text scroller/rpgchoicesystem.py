import random
import time


def choices(title, choice, outcome):

    while True:
        print(str(title))
        count = 0
        for i in choice:
            print(str(count+1) + ". " + i)
            count += 1
        decision = input("\n >")
        try:
            decision = int(decision)
            if decision > 0 and decision <= len(choice):
                decision = outcome[decision-1]
                print(decision)
                break
        except Exception as e:
            print("Invalid Input: " + str(e))
        print("\n" * 30)

    return decision
        



print("sans undertale go into my eyes")
time.sleep(1)
print("\n")

event = choices("WOH- HWA WHATHOEAHA", ["Scream calmly", "Leave"], ["Eggman respected your decision and pat you on the head.", "Leave"])
if event == "You missed and got hit!":
    print("Defeat!")
elif event == "Ran away successfully":
    print("Victory!")

print("End")


















































