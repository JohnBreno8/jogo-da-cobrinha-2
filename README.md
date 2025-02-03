# jogo-da-cobrinha-2
---

1. Configuração dos Modos de Jogo:

GAME_MODES = {
    "🎮 Clássico": "classic",
    
    "🤖 Modo IA": "ai"
    
    "🌀 Modo Portal": "portal"
    
    "🚧 Modo Obstáculos": "obstacles"
}

Esse dicionário GAME_MODES define os diferentes modos de jogo. Quando o jogador inicia o jogo, ele escolhe um modo e a mecânica do jogo muda. O modo "IA" faz a cobrinha jogar contra uma inteligência artificial que tenta buscar a comida. Já o "Modo Portal" permite que a cobrinha atravesse as bordas da tela, enquanto no "Modo Obstáculos", você tem obstáculos pelo caminho, tornando o jogo mais desafiador. Esse tipo de configuração é bacana porque dá ao jogo uma boa variabilidade!


---

2. A Função draw_menu():

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

Esse código exibe o menu do jogo de forma animada. Uma curiosidade é o uso da função stdscr.addstr() para desenhar texto no terminal. A animação acontece quando o jogador navega pelas opções usando as teclas de seta ou 'w' e 's'. Quando a opção está selecionada, ela muda de cor e aparece com um símbolo "▶" antes do texto, tornando a navegação visualmente interessante. Isso cria uma experiência de menu bem interativa, mesmo sendo simples no terminal.


---

3. Lógica da IA (Inteligência Artificial):

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

Aqui temos a lógica da IA que controla a cobra no modo "IA". Ela tenta sempre se mover na direção da comida, evitando colisões com o corpo da cobra e obstáculos. Esse trecho é um exemplo básico de IA, onde a cobrinha toma decisões simples com base na posição da comida. A escolha da direção é feita aleatoriamente entre as opções viáveis, o que deixa a IA bem simples, mas funcional.


---

4. A Função Principal main() e o Controle do Jogo:

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    mode = GAME_MODES[draw_menu(stdscr, "🐍 JOGO DA COBRINHA 🐍", list(GAME_MODES.keys()))]
    difficulty = draw_menu(stdscr, "🎮 Escolha a Dificuldade:", list(DIFFICULTY_LEVELS.keys()))
    speed, score_multiplier = DIFFICULTY_LEVELS[difficulty]

Nessa parte, o jogo começa de verdade. Aqui, o código configura a aparência do terminal, inicializa as cores e chama o menu para o jogador escolher o modo e a dificuldade. O uso de curses.start_color() e curses.init_pair() permite que o jogo tenha cores diferentes para os elementos, o que ajuda a dar uma sensação de vivacidade ao jogo no terminal.


---

5. Movimento da Cobra e Detecção de Colisões:

new_head = [snake[0][0] + (direction == "DOWN") - (direction == "UP"),
            snake[0][1] + (direction == "RIGHT") - (direction == "LEFT")]

if new_head in snake or new_head in obstacles:
    break

Aqui, a lógica do movimento da cobra é processada. A posição da cabeça da cobra é atualizada dependendo da direção escolhida. Se a cabeça colidir com o corpo da cobra ou com obstáculos (no caso do modo "obstacles"), o jogo termina. Essa parte é a essência do jogo: a cobra cresce e você tem que evitar bater em si mesma ou nos obstáculos.


---

6. Movimentação usando Teclas A, W, D e S:

O jogo permite que você movimente a cobra usando as teclas direcionais do teclado, como as setas, mas também é possível utilizar as teclas 'A', 'W', 'S' e 'D' para se mover. Aqui está como as teclas estão configuradas para controlar a direção da cobra:

'W': Move a cobra para cima (equivalente à seta para cima).

'S': Move a cobra para baixo (equivalente à seta para baixo).

'A': Move a cobra para a esquerda (equivalente à seta para a esquerda).

'D': Move a cobra para a direita (equivalente à seta para a direita).


O código para essa movimentação é processado dentro da função main().


---

Como Rodar o Jogo no Termux ou Outro Terminal Linux:

1. Instale o Python no Termux (se ainda não estiver instalado):

pkg install python


2. Instale o módulo curses: O módulo curses já vem com a instalação do Python no Termux, mas se precisar instalá-lo em outra plataforma, use:

pip install windows-curses  # Para sistemas Windows


3. Baixe ou Crie o Arquivo do Jogo: Crie um arquivo com o nome jogo-da-cobrinha2.py e copie o código do jogo para esse arquivo.


4. Execute o Jogo: Navegue até o diretório onde o arquivo está salvo e execute o jogo com o comando:

python jogo-da-cobrinha2.py



Após executar esse comando, o jogo será iniciado no terminal e você poderá jogar diretamente ali, utilizando as teclas para controlar a cobrinha ou se você estiver em um dispositivo móvel vc pode usar as setas também .

 
