import random

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ship:
    def __init__(self, start_dot, length, orientation):
        self.start_dot = start_dot
        self.length = length
        self.orientation = orientation
        self.dots = []

        for i in range(length):
            if orientation == 'v':
                new_dot = Dot(start_dot.x, start_dot.y + i)
            else:
                new_dot = Dot(start_dot.x + i, start_dot.y)
            self.dots.append(new_dot)

class Board:
    def __init__(self, size=6):
        self.size = size
        self.board = [['O'] * size for _ in range(size)]
        self.ships = []

    def reset_board(self):
        self.board = [['O'] * self.size for _ in range(self.size)]
        self.ships = []

    def is_near_ship_or_contour(self, dot):
        for ship in self.ships:
            for ship_dot in ship.dots:
                if abs(ship_dot.x - dot.x) <= 1 and abs(ship_dot.y - dot.y) <= 1:
                    return True
                if (ship_dot.x == dot.x and abs(ship_dot.y - dot.y) <= 1) or (
                        ship_dot.y == dot.y and abs(ship_dot.x - dot.x) <= 1):
                    return True
        return False

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot):
                raise ValueError("Корабль выходит за пределы поля боя!")
            if self.is_near_ship_or_contour(dot):
                raise ValueError("Корабли не могут соприкасаться!")
            self.board[dot.y][dot.x] = '■'
        self.ships.append(ship)
        return True  # Возвращаем True, если корабль успешно размещен на доске

    def out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):
        if self.out(dot):
            raise ValueError("Координаты выстрела выходят за поле боя!")
        if self.board[dot.y][dot.x] == 'X' or self.board[dot.y][dot.x] == 'T':
            raise ValueError("В этот квадрат вы уже стреляли!")
        if self.board[dot.y][dot.x] == '■':
            self.board[dot.y][dot.x] = 'X'
            print("Попадание!")
        else:
            self.board[dot.y][dot.x] = 'T'
            print("Промах!")
        print(self.display_without_ships())  # Обновляем вывод поля
        return self.board[dot.y][dot.x] == 'X'

    def __str__(self):
        res = "   | 1 | 2 | 3 | 4 | 5 | 6 |\n"
        res += " \n"
        for i, row in enumerate(self.board):
            res += f"{i + 1:2} | {' | '.join(row)} |\n"
        res += " \n"
        return res

    def display_without_ships(self):
        res = "   | 1 | 2 | 3 | 4 | 5 | 6 |\n"
        res += " \n"
        for i, row in enumerate(self.board):
            res += f"{i + 1:2} | "
            for cell in row:
                if cell == 'X':
                    res += 'X | '
                elif cell == 'T':
                    res += 'T | '
                else:
                    res += 'O | '
            res += "\n"
        res += " \n"
        return res

def get_coordinates(length, ship_name):
    while True:
        try:
            x, y = map(int, input(f"Введите координаты {ship_name} (x y): ").split())
            return Dot(x - 1, y - 1)
        except ValueError:
            print("Некорректные координаты. Пожалуйста, введите два числа.")

def get_orientation(length):
    while True:
        orientation = input(f"Введите ориентацию корабля длиной {length} {'клетки' if length > 1 else 'клетку'} (h - горизонтально, v - вертикально): ").lower()
        if orientation == 'h' or orientation == 'v':
            return orientation
        else:
            print("Некорректная ориентация. Пожалуйста, введите 'h' или 'v'.")

def place_ships(board):
    ship_lengths = [3, 2, 2, 1, 1, 1, 1]
    ship_names = ["корабля на 3 клетки", "корабля на 2 клетки", "корабля на 2 клетки",
                  "корабля на 1 клетку", "корабля на 1 клетку", "корабля на 1 клетку", "корабля на 1 клетку"]
    for length, ship_name in zip(ship_lengths, ship_names):
        while True:
            try:
                start_dot = get_coordinates(length, ship_name)
                if length > 1:
                    orientation = get_orientation(length)
                else:
                    orientation = 'h'  # Присваиваем горизонтальную ориентацию для кораблей длиной 1 клетка
                if board.add_ship(Ship(start_dot, length, orientation)):
                    print("Ваше поле:")
                    print(board)
                    break
            except ValueError as e:
                print(e)

def place_remaining_ships(board):
    ship_lengths = [3] + [2] * 2 + [1] * 4
    for length in ship_lengths:
        while True:
            try:
                start_dot = get_coordinates(length, f"корабля на {length} клетки")
                orientation = get_orientation(length)
                if board.add_ship(Ship(start_dot, length, orientation)):
                    print("Ваше поле:")
                    print(board)
                    break
            except ValueError as e:
                print(e)

class User:
    def __init__(self, board, opponent_board):  # Добавляем параметр opponent_board
        self.board = board
        self.opponent_board = opponent_board  # Сохраняем поле противника

    def move(self):
        while True:
            try:
                x, y = map(int, input("Введите координаты выстрела (x y): ").split())
                target_dot = Dot(x - 1, y - 1)
                if self.opponent_board.shot(target_dot):  # Выстрел на поле противника
                    print("Вы попали! Сделайте еще один выстрел.")
                    if not self.check_game_over(self.opponent_board):  # Проверяем поле противника на окончание игры
                        continue  # Продолжаем цикл, чтобы игрок мог сделать второй выстрел
                    else:
                        print("Победа! Вы уничтожили все корабли противника.")
                        return True
                else:
                    print("Вы промахнулись.")
                    return False  # Возвращаем False, если игрок промахнулся
            except ValueError:
                print("Некорректные координаты. Пожалуйста, введите два числа.")
            except Exception as e:
                print(e)

    def check_game_over(self, board):
        for ship in board.ships:
            for dot in ship.dots:
                if board.board[dot.y][dot.x] == '■':
                    return False
        return True

class AI:
    def __init__(self, board, opponent_board):
        self.board = board
        self.opponent_board = opponent_board
        self.place_ships()  # Размещаем корабли компьютера при создании объекта AI

    def place_ships(self):
        ship_lengths = [3, 2, 2, 1, 1, 1, 1]
        for length in ship_lengths:
            while True:
                try:
                    start_dot = self.get_random_coordinates(length)
                    orientation = random.choice(['h', 'v'])
                    if self.board.add_ship(Ship(start_dot, length, orientation)):
                        break
                except ValueError:
                    continue

    def get_random_coordinates(self, length):
        x = random.randint(0, self.board.size - 1)
        y = random.randint(0, self.board.size - 1)
        return Dot(x, y)

    def move(self):
        while True:
            x, y = random.randint(0, self.board.size - 1), random.randint(0, self.board.size - 1)
            target_dot = Dot(x, y)
            try:
                if self.opponent_board.shot(target_dot):
                    print("ИИ попал!")
                    if not self.check_game_over(self.opponent_board):
                        continue
                    else:
                        print("Победил ИИ! Он уничтожил все ваши корабли.")
                        return True
                else:
                    print("ИИ промахнулся.")
                    return False
            except ValueError:
                continue

    def check_game_over(self, board):
        for ship in board.ships:
            for dot in ship.dots:
                if board.board[dot.y][dot.x] == '■':
                    return False
        return True


class Game:
    def __init__(self, size=6):
        self.size = size
        self.playing = True
        self.player_board = Board(size)
        self.computer_board = Board(size)
        self.player = User(self.player_board, self.computer_board)
        self.ai = AI(self.computer_board, self.player_board)

    def greet(self):
        print("Добро пожаловать в игру Морской бой!")
        print("Ваше поле:")
        print(self.player_board)

    def start(self):
        self.greet()
        place_ships(self.player_board)
        print("Начало игры.")
        print("Поле боя:")
        print(self.computer_board.display_without_ships())  # Выводим поле противника перед первым выстрелом игрока
        while self.playing:
            if self.player.move():
                self.playing = not self.check_game_over(self.computer_board)
                if not self.playing:
                    print("Победа!")
                    break
                continue  # Продолжаем цикл, чтобы игрок мог сделать второй выстрел
            if self.ai.move():
                self.playing = not self.check_game_over(self.player_board)
                if not self.playing:
                    print("Поражение!")
                    break
                continue  # Продолжаем цикл, чтобы ИИ мог сделать второй выстрел

    def check_game_over(self, board):
        for ship in board.ships:
            for dot in ship.dots:
                if board.board[dot.y][dot.x] == '■':
                    return False
        return True

if __name__ == "__main__":
    game = Game()
    game.start()