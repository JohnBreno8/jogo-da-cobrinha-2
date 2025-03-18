import curses
import random
import time
import os
from plyer import notification
import logging

# Configura logging para debug
logging.basicConfig(level=logging.DEBUG)

# Configuração dos modos de jogo
GAME_MODES = {
    "🎮 Clássico": "classic",
    "🤖 Modo IA": "ai",
    "🌀 Modo Portal": "portal",
    "🚧 Modo Obstáculos": "obstacles"
}

# Configuração das dificuldades
DIFFICULTY_LEVELS = {
    "🐢 Fácil": (150, 1),
    "🐍 Médio": (100, 2),
    "🔥 Difícil": (70, 3),
    "💀 Insano": (50, 5)
}

# Função para carregar e salvar recordes
def load_record():
    return int(open("record.txt").read()) if os.path.exists("record.txt") else 0

def save_record(score):
    with open("record.txt", "w") as file:
        file.write(str(score))

# Função para enviar notificação no desktop
def send_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Jogo da Cobrinha",
            timeout=5
        )
        logging.debug(f"Notificação enviada: {title} - {message}")
    except Exception as e:
        logging.error(f"Erro ao enviar notificação: {e}")

# Exibição de um menu animado
def draw_menu(stdscr, title, options):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    selected = 0

    while True:
        stdscr.clear()
        stdscr.border(0)
        stdscr.addstr(h//6, w//2 - len(title)//2, title, curses.A_BOLD | curses.A_BLINK)

        for i, option in enumerate(options):
            x = w//2 - len(option) // 2
            y = h//3 + i
            if i == selected:
                stdscr.addstr(y, x - 2, "▶ ", curses.A_BOLD)
                stdscr.addstr(y, x, option, curses.A_REVERSE | curses.A_BOLD)
            else:
                stdscr.addstr(y, x, option)

        stdscr.refresh()
        key = stdscr.getch()
        if key in [curses.KEY_UP, ord('w')]:
            selected = max(0, selected - 1)
        elif key in [curses.KEY_DOWN, ord('s')]:
            selected = min(len(options) - 1, selected + 1)
        elif key in [10, 13]:  # Enter
            return options[selected]

# Função para definir o movimento da IA
def get_next_move(snake, food, obstacles, h, w, mode):
    hx, hy = snake[0]
    fx, fy = food

    possible_moves = []
    if hx > fx and [hx - 1, hy] not in snake + obstacles:
        possible_moves.append("UP")
    if hx < fx and [hx + 1, hy] not in snake + obstacles:
        possible_moves.append("DOWN")
    if hy > fy and [hx, hy - 1] not in snake + obstacles:
        possible_moves.append("LEFT")
    if hy < fy and [hx, hy + 1] not in snake + obstacles:
        possible_moves.append("RIGHT")

    return random.choice(possible_moves) if possible_moves else "RIGHT"

# Função principal
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    mode = GAME_MODES[draw_menu(stdscr, "🐍 JOGO DA COBRINHA 🐍", list(GAME_MODES.keys()))]
    difficulty = draw_menu(stdscr, "🎮 Escolha a Dificuldade:", list(DIFFICULTY_LEVELS.keys()))
    speed, score_multiplier = DIFFICULTY_LEVELS[difficulty]

    h, w = stdscr.getmaxyx()
    snake = [[h//2, w//2]]
    direction = "RIGHT"
    score = 0
    last_notified_score = 0
    obstacles = [[random.randint(5, h-5), random.randint(5, w-5)] for _ in range(10)] if mode == "obstacles" else []

    food = [random.randint(1, h-2), random.randint(1, w-2)]
    powerups = []
    start_time = time.time()
    is_paused = False

    while True:
        stdscr.clear()
        stdscr.border(0)

        for obs in obstacles:
            stdscr.addch(obs[0], obs[1], "█", curses.color_pair(4))

        for pu in powerups:
            stdscr.addch(pu[0], pu[1], "⭐", curses.color_pair(3))

        stdscr.addch(food[0], food[1], "🍎", curses.color_pair(2))
        for i, part in enumerate(snake):
            stdscr.addch(part[0], part[1], "█" if i == 0 else "■", curses.color_pair(1))

        stdscr.addstr(0, 2, f"🏆 Score: {score} | 🚀 Tempo: {int(time.time() - start_time)}s", curses.color_pair(3))

        key = stdscr.getch()
        if key == ord('p'):
            is_paused = not is_paused
        if is_paused:
            stdscr.addstr(h//2, w//2 - 5, "⏸️ PAUSADO", curses.color_pair(4) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.5)
            continue

        if mode == "ai":
            direction = get_next_move(snake, food, obstacles, h, w, mode)
        elif key in [curses.KEY_UP, ord('w')] and direction != "DOWN":
            direction = "UP"
        elif key in [curses.KEY_DOWN, ord('s')] and direction != "UP":
            direction = "DOWN"
        elif key in [curses.KEY_LEFT, ord('a')] and direction != "RIGHT":
            direction = "LEFT"
        elif key in [curses.KEY_RIGHT, ord('d')] and direction != "LEFT":
            direction = "RIGHT"

        new_head = [snake[0][0] + (direction == "DOWN") - (direction == "UP"),
                    snake[0][1] + (direction == "RIGHT") - (direction == "LEFT")]

        if mode == "portal":
            new_head[0] %= h
            new_head[1] %= w

        if new_head in snake or new_head in obstacles:
            send_notification("Game Over!", f"Você perdeu! Pontuação final: {score}")
            break

        snake.insert(0, new_head)
        if new_head == food:
            score += score_multiplier
            food = [random.randint(1, h-2), random.randint(1, w-2)]
            if score // 100 > last_notified_score // 100:
                send_notification("Parabéns!", f"Você alcançou {score} pontos!")
                last_notified_score = score
        else:
            snake.pop()

        stdscr.refresh()
        time.sleep(speed / 1000)

curses.wrapper(main) 
