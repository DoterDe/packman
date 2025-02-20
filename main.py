import numpy as np
import random
import time

# Параметры обучения
alpha = 0.5  # Скорость обучения
gamma = 0.9 # Дисконтирование будущей награды
epsilon = 0.7  # Вероятность случайного выбора
# Поле 5x5
grid_size = 5
goal = (random.randint(0, 4), random.randint(0, 4))
tabletca = (random.randint(0, 4), random.randint(0, 4))
ghosts = [(1, 1), (3, 3)] 

while tabletca == goal:
    tabletca = (random.randint(0, 4), random.randint(0, 4))
    

def create_q_table():
    return {(x, y): {a: 0 for a in ['UP', 'DOWN', 'LEFT', 'RIGHT']}
            for x in range(grid_size) for y in range(grid_size)}

q_table = create_q_table()

def print_grid(state):
    for y in range(grid_size):
        row = ''
        for x in range(grid_size):
            if (x, y) == state:
                row += 'P '
            elif (x, y) == goal:
                row += 'G '
            elif (x, y) == tabletca:
                row += 'T '
            elif (x, y) in ghosts:
                row += 'B '  
            else:
                row += '- '
        print(row)
    print()

def get_next_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    return max(q_table[state], key=q_table[state].get)

def get_next_state(state, action):
    x, y = state
    if action == 'UP' and y > 0:
        y -= 1
    elif action == 'DOWN' and y < grid_size - 1:
        y += 1
    elif action == 'LEFT' and x > 0:
        x -= 1
    elif action == 'RIGHT' and x < grid_size - 1:
        x += 1
    return (x, y)

def get_reward(state):
    if state == tabletca:
        return -1
    if state == goal:
        return 10
    elif state in ghosts:
        return -100 
    return -5

def move_ghosts():
    
    global ghosts 
    new_ghosts = []
    for ghost in ghosts:
        action = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        new_ghost = get_next_state(ghost, action)
        if new_ghost not in ghosts and new_ghost != goal:
            new_ghosts.append(new_ghost)
        else:
            new_ghosts.append(ghost)
    ghosts = new_ghosts

def train(iterations=1000):
    for _ in range(iterations):
        state = (0, 0)
        while state != goal:
            action = get_next_action(state)
            next_state = get_next_state(state, action)
            reward = get_reward(next_state)
            max_future_q = max(q_table[next_state].values())
            q_table[state][action] += alpha * (reward + gamma * max_future_q - q_table[state][action])
            state = next_state
            move_ghosts() 

def test():
    state = (0, 0)
    path = [state]
    while state != goal:
        action = get_next_action(state)
        state = get_next_state(state, action)
        path.append(state)
        move_ghosts()
    print("Оптимальный путь:", path)

def play():
    state = (0, 0)
    invincibility_counter = 0
    print("Вы управляете персонажем! Введите UP, DOWN, LEFT, RIGHT для движения.")
    while state != goal:
        print_grid(state)
        action = input("Введите направление: ").strip().upper()
        if action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            state = get_next_state(state, action)
        else:
            print("Некорректный ввод. Попробуйте снова.")
        move_ghosts()  
        if invincibility_counter == 0 and state in ghosts:
            print("Вы попали в призрака! Игра закончена.")
            break
        if state == tabletca:
            invincibility_counter = 5  
            print("Вы съели таблетку и стали неуязвимы на 5 ходов!")
        if invincibility_counter > 0:
            invincibility_counter -= 1
    else:
        print_grid(state)
        print("Поздравляем! Вы достигли цели!")

def auto_play():
    state = (0, 0)
    invincibility_counter = 0 
    print("ИИ обучается и играет сам...")
    while state != goal:
        print_grid(state)
        time.sleep(0.5)
        action = get_next_action(state)
        state = get_next_state(state, action)
        move_ghosts() 

        if state == tabletca:
            invincibility_counter = 5 
            print("ИИ съел таблетку и стал неуязвим на 5 ходов!")

        if invincibility_counter == 0 and state in ghosts:
            print("ИИ попал в призрака! Игра закончена.")
            break
        if invincibility_counter > 0:
            invincibility_counter -= 1

    else:
        print_grid(state)
        print("ИИ дошел до цели!")

mode = input("Выберите режим: 1 - Игрок, 2 - ИИ: ").strip()
train()
if mode == "1":
    play()
elif mode == "2":
    auto_play()
else:
    print("Некорректный режим.")
