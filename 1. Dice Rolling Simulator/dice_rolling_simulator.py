import random

class Dice:
    def __init__(self, faces: list = [1,2,3,4,5,6]) -> None:
        self.faces = faces

    def roll(self) -> None:
        while True:
            print('Dice rolling...')
            result = random.randint(0, len(self.faces)-1)
            random_face = self.faces[result]
            print(f'Your roll is {random_face}!')
            reroll = self._reroll()
            if not reroll:
                print('Thanks for playing!')
                break
    
    def _reroll(self) -> bool:
        while True:
            confirm = ['yes', 'y']
            deny = ['no', 'n']
            user_input = input(f'Would you like to roll again ({confirm[0]}/{deny[0]})? ')
            decision = user_input.lower()
            if decision in confirm:
                return True
            if decision in deny:
                return False
            print(f'Please enter {confirm[0]}/{deny[0]}.')

if __name__ == '__main__':
    d6 = Dice()
    d6.roll()