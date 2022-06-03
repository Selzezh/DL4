from random import random

# Игровое поле
arr = [[2, -3], [-1, 2]]
games = 100


# датчик случайных чисел
def sensor(prob):
    r = random()
    if r <= prob:
        res = 0
    else:
        res = 1
    return res


# Вывод данных
def conc(res, probA, probB, rms, avg):
    global games
    print('Вероятность выбора игроком A красной строки:', probA)
    print('Вероятность выбора игроком B красного столбца:', probB)
    print('Счёт игрока A:', res[0])
    print('Счёт игрока B:', res[1])
    print('Средний выигрыш игрока A за одну игру:', avg)
    waiting = 8 * probA * probB - 5 * probA - 3 * probB + 2
    print('Математическое ожидание:', waiting)
    print('СКО:', rms)
    disp = (-2 * probA * probB - 3 * probB + 5 * probA + 4) - waiting ** 2
    print('Дисперсия:', disp)
    print('Теоретическое СКО:', disp ** 0.5)


# симуляция игр, когда вероятности игроков известны
def prob(probA, probB):
    global games
    res = [0, 0]
    math_res = []
    for i in range(games):
        n = arr[sensor(probA)][sensor(probB)]
        math_res.append(n)
        res = [res[0] + n, res[1] - n]
    avg = res[0] / games
    rms = 0
    for i in math_res:
        rms += (i - avg) ** 2
    rms = (rms / (games - 1)) ** 0.5
    conc(res, probA, probB, rms, avg)


# игра с подкреплением игрока A
def refresh(probB):
    global games
    res = [0, 0]
    math_res = []
    case = [10, 10]
    probA = case[0] / (case[0] + case[1])
    for i in range(games):
        rand = sensor(probA)
        n = arr[rand][sensor(probB)]
        if n > 0:
            case[rand] += 2
        probA = case[0] / (case[0] + case[1])
        math_res.append(n)
        res = [res[0] + n, res[1] - n]
    avg = res[0] / games
    rms = 0
    for i in math_res:
        rms += (i - avg) ** 2
    rms = (rms / (games - 1)) ** 0.5
    conc(res, probA, probB, rms, avg)


# игра с наказанием игрока A
def punish(probB):
    global games
    res = [0, 0]
    math_res = []
    case = [100, 100]
    probA = case[0] / (case[0] + case[1])
    for i in range(games):
        rand = sensor(probA)
        n = arr[rand][sensor(probB)]
        if n < 0:
            case[rand] += n
        probA = case[0] / (case[0] + case[1])
        math_res.append(n)
        res = [res[0] + n, res[1] - n]
    avg = res[0] / games
    rms = 0
    for i in math_res:
        rms += (i - avg) ** 2
    rms = (rms / (games - 1)) ** 0.5
    conc(res, probA, probB, rms, avg)


# игра с подкреплением обоих игроков
def refresh_4_2():
    global games
    res = [0, 0]
    math_res = []
    caseA = [10, 10]
    caseB = [10, 10]
    probA = caseA[0] / (caseA[0] + caseA[1])
    probB = caseB[0] / (caseB[0] + caseB[1])
    for i in range(games):
        randA = sensor(probA)
        randB = sensor(probB)
        n = arr[randA][randB]
        if n < 0:
            caseB[randB] -= n
        else:
            caseA[randA] += n
        probA = caseA[0] / (caseA[0] + caseA[1])
        probB = caseB[0] / (caseB[0] + caseB[1])
        math_res.append(n)
        res = [res[0] + n, res[1] - n]
    avg = res[0] / games
    rms = 0
    for i in math_res:
        rms += (i - avg) ** 2
    rms = (rms / (games - 1)) ** 0.5
    conc(res, probA, probB, rms, avg)


print('\nИгра с равными вероятностями выбора столбца/строки\n')
prob(0.5, 0.5)
print('\nИгра, при которой игрок A равновероятно выбирает строку, а игрок B выбирает красный столбец втрое реже, '
      'чем синий.\n')
prob(0.5, 0.25)
print('\nОбучение игрока A с помощью подкрепления\n')
refresh(0.25)
print('\nОбучение игрока A с помощью наказания\n')
punish(0.25)
print('\nОбучение обоих игроков с помощью подкрепления\n')
refresh_4_2()






