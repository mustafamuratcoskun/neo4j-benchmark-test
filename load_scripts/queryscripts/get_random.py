import random

def getRandomIds(number):
    random_ids = list()
    for i in range(1,number):
        random_ids.append(random.randint(1,1630000))
    return random_ids