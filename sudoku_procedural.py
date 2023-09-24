import pygame
import sys
import time

pygame.init()

# Constants
reset_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 6, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solved_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 6, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

sudoku_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 6, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

GRID_WIDTH, GRID_HEIGHT = 600, 600
GRID_SIZE = 9
CELL_SIZE = (GRID_WIDTH // GRID_SIZE)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CIAN = (39, 162, 219)
GREEN = (127, 255, 212)
start_time = time.time()
IMG = pygame.image.load('retry-icon-14.jpg')

timer_running = True

# Set up the display
screen = pygame.display.set_mode((596.6, 750))
pygame.display.set_caption("Sudoku")


def get_cell_position(mouse_x, mouse_y):
    """Convert mouse coordinates to grid cell indices."""
    row = mouse_y // CELL_SIZE
    col = mouse_x // CELL_SIZE + 1
    return row, col


def out_of_grid_check(cell):
    """Check if a cell is out of bounds."""
    if cell[0] > 9 or cell[0] < 1:
        return True
    return False


def draw_grid():
    """Draw the Sudoku grid on the screen."""
    for i in range(GRID_SIZE + 1):
        line_thickness = 2 if i % 3 == 0 else 1  # Thick lines for box boundaries

        pygame.draw.line(screen, (255, 255, 255), (i * CELL_SIZE, CELL_SIZE), (i * CELL_SIZE, GRID_HEIGHT + 61),
                         line_thickness)  # vertical
        pygame.draw.line(screen, (255, 255, 255), (0, i * CELL_SIZE + CELL_SIZE),
                         (GRID_WIDTH, i * CELL_SIZE + CELL_SIZE),
                         line_thickness)  # horizontal


def draw_static_numbers_on_the_grid(grid):
    """Draw the static numbers on the Sudoku grid."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            number = grid[row][col]
            if number != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(number), True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2 + CELL_SIZE))
                screen.blit(text, text_rect)


def calculate_time():
    """Calculate and format the elapsed time."""
    elapsed_time = time.time() - start_time
    elapsed_time_seconds = int(elapsed_time)
    elapsed_time_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed_time_seconds))

    return elapsed_time_formatted


def draw_time(elapsed_time_formatted):
    """Calculate and format the elapsed time."""
    font = pygame.font.Font(None, 30)
    text = font.render(f"{elapsed_time_formatted}", True, (255, 255, 255))
    screen.blit(text, (500, CELL_SIZE / 2))


def highlight_border_on_click(cell):
    """Highlight the selected cell's border."""
    if cell:
        if out_of_grid_check(cell):
            pass
        else:
            cell_x = (cell[1] - 1) * CELL_SIZE
            cell_y = (cell[0] - 1) * CELL_SIZE
            pygame.draw.rect(screen, CIAN, (cell_x, cell_y + CELL_SIZE, CELL_SIZE + 2.2, CELL_SIZE),
                             2)  # Highlight the selected cell


def insert_new_value_in_the_matrix(value, coords):
    """Insert a new value into the Sudoku grid."""
    row, col = coords
    if sudoku_grid[row][col] == 0:
        sudoku_grid[row][col] = value


def draw_number(number, coords, color):
    """Draw a number on the screen with a specified color."""
    row, col = coords

    font = pygame.font.Font(None, 36)
    text = font.render(str(number), True, color)
    text_rect = text.get_rect(
        center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2 + CELL_SIZE))
    screen.blit(text, text_rect)


def draw_mistakes(made_mistakes, allowed):
    """Draw the number of mistakes on the screen."""
    font = pygame.font.Font(None, 30)
    text = font.render(f"{made_mistakes}/{allowed}", True, (255, 255, 255))
    screen.blit(text, (285, 695))


def draw_game_over(x, y):
    """Display the 'GAME OVER' message on the screen."""

    # Define button properties
    button_width, button_height = 150, 40
    button_color = RED
    border_radius = 30
    text_color = (0, 0, 0)  # Black
    text_font = pygame.font.Font(None, 30)
    button_text = "YOU LOST"

    # Create the button rectangle with rounded corners at the specified coordinates (x, y)
    button_rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=border_radius)

    # Create the button text
    text_surface = text_font.render(button_text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)

    # Draw the button text on the screen
    screen.blit(text_surface, text_rect)


def draw_you_won(x, y):
    """Display the 'YOU WON' message on the screen."""
    # Define button properties
    button_width, button_height = 150, 40
    button_color = CIAN  # Green
    border_radius = 30
    text_color = (0, 0, 0)  # Black
    text_font = pygame.font.Font(None, 30)
    button_text = "YOU WON"

    # Create the button rectangle with rounded corners at the specified coordinates (x, y)
    won_button_rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(screen, button_color, won_button_rect, border_radius=border_radius)

    # Create the button text
    text_surface = text_font.render(button_text, True, text_color)
    text_rect = text_surface.get_rect(center=won_button_rect.center)

    # Draw the button text on the screen
    screen.blit(text_surface, text_rect)

    return won_button_rect


def draw_solve_button(x, y):
    # Define button properties
    button_width, button_height = 150, 40
    button_color = (0, 255, 0)  # Green
    border_radius = 30
    text_color = (0, 0, 0)  # Black
    text_font = pygame.font.Font(None, 30)
    button_text = "SOLVE"

    # Create the button rectangle with rounded corners at the specified coordinates (x, y)
    solve_button_rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(screen, button_color, solve_button_rect, border_radius=border_radius)

    # Create the button text
    text_surface = text_font.render(button_text, True, text_color)
    text_rect = text_surface.get_rect(center=solve_button_rect.center)

    # Draw the button text on the screen
    screen.blit(text_surface, text_rect)
    return solve_button_rect


def draw_continue_button(x, y):
    # Define button properties
    button_width, button_height = 150, 40
    button_color = (0, 255, 0)  # Green
    border_radius = 30
    text_color = (0, 0, 0)  # Black
    text_font = pygame.font.Font(None, 30)
    button_text = "RESET"

    # Create the button rectangle with rounded corners at the specified coordinates (x, y)
    try_again_button_rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(screen, button_color, try_again_button_rect, border_radius=border_radius)

    # Create the button text
    text_surface = text_font.render(button_text, True, text_color)
    text_rect = text_surface.get_rect(center=try_again_button_rect.center)

    # Draw the button text on the screen
    screen.blit(text_surface, text_rect)
    return try_again_button_rect

def solve_sudoku(board):
    def find_empty_location(bo):
        for r in range(len(bo)):
            for c in range(len(bo[r])):
                if bo[r][c] == 0:
                    return r, c

    def valid(bo, num, pos):
        for i in range(len(bo)):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False

        for j in range(len(bo)):
            if bo[j][pos[1]] == num and pos[0] != j:
                return False

        box_x = pos[0] // 3
        box_y = pos[1] // 3

        for x in range(box_x * 3, box_x * 3 + 3):
            for y in range(box_y * 3, box_y * 3 + 3):
                if bo[x][y] == num and (x, y) != [pos]:
                    return False
        return True

    def solve(bo):
        find = find_empty_location(bo)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(bo, i, (row, col)):
                bo[row][col] = i

                if solve(bo):
                    return True

                bo[row][col] = 0

        return False

    solve(board)
    return board


def main():
    """Display the 'YOU WON' message on the screen."""

    global solve_rect
    global try_again_rect
    solve_sudoku(solved_grid)  # Change with the main board to see how a WIN scenario looks like

    # Game state variables
    running = True
    game_over_flag = False

    # Input and UI-related variables
    selected_cell = None
    button_pressed = False
    number_color = ""
    key = None

    # Mistake tracking
    allowed_mistakes = 3
    mistakes = 0

    # Timer-related variables
    current_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_cell = get_cell_position(mouse_x, mouse_y)
                if button_pressed:
                    key = ""

                if solve_rect.collidepoint(mouse_x, mouse_y):
                    global sudoku_grid
                    sudoku_grid = solved_grid
                    game_over_flag = True

                elif try_again_rect.collidepoint(mouse_x, mouse_y):
                    global reset_grid
                    global start_time
                    sudoku_grid = reset_grid
                    start_time = time.time()
                    mistakes = 0
                    game_over_flag = False

            if not game_over_flag:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        key = 1
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        key = 2
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        key = 3
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        key = 4
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        key = 5
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        key = 6
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        key = 7
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        key = 8
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        key = 9

                    # if there is selected cell, and clicked button, check if the number can be placed there
                    sci = [x - 1 for x in selected_cell]
                    if key is not None and selected_cell and sudoku_grid[sci[0]][sci[1]] == 0:
                        button_pressed = True
                        # Get the index values of the selected cell

                        # Validate
                        if key == solved_grid[sci[0]][sci[1]]:
                            # The position on which the selected number is placed is correct
                            number_color = WHITE
                            # Change the value in the matrix with the number inputted
                            insert_new_value_in_the_matrix(key, sci)
                        else:
                            mistakes += 1
                            number_color = RED  # Fixed: Set number_color to RED for an invalid number

                        # Draw the number with the determined color

        screen.fill((0, 0, 0))
        draw_grid()
        draw_static_numbers_on_the_grid(sudoku_grid)
        solve_rect = draw_solve_button(420, 685)
        try_again_rect = draw_continue_button(25, 685)
        highlight_border_on_click(selected_cell)

        if not game_over_flag:
            current_time = calculate_time()

        draw_time(current_time)

        if mistakes == allowed_mistakes:
            draw_mistakes(mistakes, allowed_mistakes)
            game_over_flag = True
            draw_game_over(225, 685)
        else:
            draw_mistakes(mistakes, allowed_mistakes)

        if key is not None and number_color != "" and sudoku_grid[sci[0]][sci[1]] == 0:
            draw_number(key, sci, number_color)

        if sum(1 for row in sudoku_grid for val in row if val != 0) == 81:
            if game_over_flag:
                pass
            else:
                game_over_flag = True
                draw_you_won(225, 685)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
