import pygame
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe Arcade (X-O)")
clock = pygame.time.Clock()

# Couleurs (Thème Néon & Sombre)
DARK_BG = (20, 24, 33)
GRID_COLOR = (45, 55, 75)
X_COLOR = (0, 255, 157)      # Vert néon pour les X
O_COLOR = (255, 75, 75)      # Rouge pour les O
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Polices
font_large = pygame.font.SysFont("Arial", 42, bold=True)
font_medium = pygame.font.SysFont("Arial", 26, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

BOARD_SIZE = 3
CELL_SIZE = 130
GRID_OFFSET_X = (WIDTH - (BOARD_SIZE * CELL_SIZE)) // 2
GRID_OFFSET_Y = 120

def reset_game():
    return {
        "board": [["" for _ in range(3)] for _ in range(3)],
        "turn": "X",  # Le joueur X commence
        "winner": None,
        "game_over": False
    }

game = reset_game()

def check_winner(board):
    # Vérification des lignes
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] != "":
            return board[r][0]
    # Vérification des colonnes
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] != "":
            return board[0][c]
    # Vérification des diagonales
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    
    # Vérification du match nul
    if all(board[r][c] != "" for r in range(3) for c in range(3)):
        return "Tie"
        
    return None

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game["game_over"]:
                game = reset_game()
            else:
                # Vérifier si le clic est dans la grille
                x, y = mouse_pos
                if GRID_OFFSET_X <= x <= GRID_OFFSET_X + 3 * CELL_SIZE and \
                   GRID_OFFSET_Y <= y <= GRID_OFFSET_Y + 3 * CELL_SIZE:
                    c = (x - GRID_OFFSET_X) // CELL_SIZE
                    r = (y - GRID_OFFSET_Y) // CELL_SIZE
                    
                    if game["board"][r][c] == "" and not game["winner"]:
                        game["board"][r][c] = game["turn"]
                        winner = check_winner(game["board"])
                        if winner:
                            game["winner"] = winner
                            game["game_over"] = True
                        else:
                            game["turn"] = "O" if game["turn"] == "X" else "X"
                            
        elif event.type == pygame.KEYDOWN:
            if game["game_over"] and event.key == pygame.K_SPACE:
                game = reset_game()

    screen.fill(DARK_BG)

    # 1. Affichage du HUD / Tour en cours
    if not game["game_over"]:
        turn_txt = font_medium.render(f"Tour du joueur : {game['turn']}", True, X_COLOR if game["turn"] == "X" else O_COLOR)
        screen.blit(turn_txt, (WIDTH // 2 - turn_txt.get_width() // 2, 40))
    else:
        if game["winner"] == "Tie":
            end_txt = font_medium.render("Match Nul !", True, WHITE)
        else:
            end_txt = font_medium.render(f"Joueur {game['winner']} Gagne !", True, X_COLOR if game["winner"] == "X" else O_COLOR)
        screen.blit(end_txt, (WIDTH // 2 - end_txt.get_width() // 2, 40))

    # 2. Dessin de la grille du morpion
    for r in range(3):
        for c in range(3):
            rect = pygame.Rect(GRID_OFFSET_X + c * CELL_SIZE, GRID_OFFSET_Y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (28, 34, 46), rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 2)

            # Dessiner X ou O selon l'état de la case
            val = game["board"][r][c]
            if val == "X":
                pad = 30
                pygame.draw.line(screen, X_COLOR, (rect.left + pad, rect.top + pad), (rect.right - pad, rect.bottom - pad), 6)
                pygame.draw.line(screen, X_COLOR, (rect.right - pad, rect.top + pad), (rect.left + pad, rect.bottom - pad), 6)
            elif val == "O":
                pygame.draw.circle(screen, O_COLOR, rect.center, CELL_SIZE // 2 - 25, 6)

    # 3. Indication de redémarrage en bas
    if game["game_over"]:
        restart_txt = font_small.render("Appuie sur ESPACE ou clique pour rejouer", True, GRAY)
        screen.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, HEIGHT - 55))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()