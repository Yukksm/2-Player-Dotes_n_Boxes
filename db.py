import pygame

SCREEN = WIDTH, HEIGHT = 300, 300
CELL = 20  # Cell size 20 px
PADDING = 20
ROWS = COLS = (WIDTH - 4 * PADDING) // CELL  # 11 rows and columns

# Initialize pygame window
pygame.init()
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption("Dots and Boxes")

# Define colors
WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLUE = (0, 255, 0)
GREEN = (0, 255, 0)
BLACK = (12, 12, 12)

font = pygame.font.SysFont('Cursive', 25)


class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.index = self.r * ROWS + self.c
        self.rect = pygame.Rect((c * CELL + 2 * PADDING, r * CELL + 3 * PADDING, CELL, CELL))

        # Store positions of the cell's edges
        self.left = self.rect.left
        self.top = self.rect.top
        self.right = self.rect.right
        self.bottom = self.rect.bottom

        # Edges and sides tracking
        self.edges = [
            [(self.left, self.top), (self.right, self.top)],
            [(self.right, self.top), (self.right, self.bottom)],
            [(self.right, self.bottom), (self.left, self.bottom)],
            [(self.left, self.bottom), (self.left, self.top)]
        ]
        self.sides = [False, False, False, False]
        self.winner = None
        self.color = None
        self.text = None

    def checkwin(self, winner):
        if not self.winner:
            if self.sides == [True] * 4:
                self.winner = winner
                self.color = GREEN if winner == 'X' else RED
                self.text = font.render(self.winner, True, WHITE)
                return 1
        return 0

    def update(self, win):
        if self.winner:
            pygame.draw.rect(win, self.color, self.rect)
            win.blit(self.text, (self.rect.centerx - 5, self.rect.centery - 7))
        for index, side in enumerate(self.sides):
            if side:
                pygame.draw.line(win, WHITE, self.edges[index][0], self.edges[index][1], 2)


def create_cells():
    cells = []
    for r in range(ROWS):
        for c in range(COLS):
            cell = Cell(r, c)
            cells.append(cell)
    return cells


def reset_game():
    return create_cells(), 0, 0, 0, ['X', 'O'], 'X', False, None


# Initial game setup
gameover = False
cells, fillcount, p1_score, p2_score, players, player, next_turn, ccell = reset_game()

# Main game loop
running = True
while running:
    win.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Select the cell under the mouse click
            position = event.pos
            for cell in cells:
                if cell.rect.collidepoint(position):
                    ccell = cell
                    break

        # Draw a line on a specific side based on the arrow keys
        if not gameover and ccell:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not ccell.sides[0]:  # Top
                    ccell.sides[0] = True
                    if ccell.index - ROWS >= 0:
                        cells[ccell.index - ROWS].sides[2] = True
                    next_turn = True

                elif event.key == pygame.K_RIGHT and not ccell.sides[1]:  # Right
                    ccell.sides[1] = True
                    if (ccell.index + 1) % COLS > 0:
                        cells[ccell.index + 1].sides[3] = True
                    next_turn = True

                elif event.key == pygame.K_DOWN and not ccell.sides[2]:  # Bottom
                    ccell.sides[2] = True
                    if ccell.index + ROWS < len(cells):
                        cells[ccell.index + ROWS].sides[0] = True
                    next_turn = True

                elif event.key == pygame.K_LEFT and not ccell.sides[3]:  # Left
                    ccell.sides[3] = True
                    if ccell.index % COLS > 0:
                        cells[ccell.index - 1].sides[1] = True
                    next_turn = True

            # Check if completing a box
            if ccell.checkwin(player):
                fillcount += 1
                if player == 'X':
                    p1_score += 1
                else:
                    p2_score += 1
                if fillcount == ROWS * COLS:
                    gameover = True  # End the game if the board is full

            # Switch turn if no box was completed
            if next_turn:
                players.reverse()
                player = players[0]
                next_turn = False
                ccell = None  # Reset selected cell for the next player

    # Draw grid and score
    for r in range(ROWS + 1):
        for c in range(COLS):
            pygame.draw.circle(win, WHITE, (c * CELL + 2 * PADDING, r * CELL + 3 * PADDING), 2)

    for cell in cells:
        cell.update(win)

    p1img = font.render(f'Player 1  : {p1_score}', True, BLUE)
    p1rect = p1img.get_rect()
    p1rect.x, p1rect.y = 2 * PADDING, 15
    p2img = font.render(f'Player 2 : {p2_score}', True, BLUE)
    p2rect = p2img.get_rect()
    p2rect.right, p2rect.y = WIDTH - 2 * PADDING, 15

    win.blit(p1img, p1rect)
    win.blit(p2img, p2rect)

    if player == 'X':
        pygame.draw.line(win, BLUE, (p1rect.x, p1rect.bottom + 2), (p1rect.right, p1rect.bottom + 2), 1)
    else:
        pygame.draw.line(win, BLUE, (p2rect.x, p2rect.bottom + 2), (p2rect.right, p2rect.bottom + 2), 1)

    # Game Over Screen
    if gameover:
        rect = pygame.Rect((50, 100, WIDTH - 100, HEIGHT - 200))
        pygame.draw.rect(win, BLACK, rect)
        pygame.draw.rect(win, RED, rect, 2)

        over = font.render('GAME OVER', True, WHITE)
        win.blit(over, (rect.centerx - over.get_width() // 2, rect.y + 10))

        winner = '1' if p1_score > p2_score else '2'
        winner_img = font.render(f'Player {winner} Won', True, GREEN)
        win.blit(winner_img, (rect.centerx - winner_img.get_width() // 2, rect.centery - 10))

        msg = "Press R to Restart, Q to Quit"
        msgimg = font.render(msg, True, RED)
        win.blit(msgimg, (rect.centerx - msgimg.get_width() // 2, rect.centery + 20))

    pygame.display.update()

pygame.quit()
