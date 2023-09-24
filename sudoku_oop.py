import pygame
import sys
import time


class SudokuGame:
    def __init__(self):
        pygame.init()
        self.GRID_WIDTH, self.GRID_HEIGHT = 600, 600
        self.GRID_SIZE = 9
        self.CELL_SIZE = (self.GRID_WIDTH // self.GRID_SIZE)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.CYAN = (39, 162, 219)
        self.GREEN = (127, 255, 212)
        self.current_time = time.time()
        self.sci = []

        self.initial_grid = [
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

        self.sudoku_grid = [
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

        self.solution_grid = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]

        self.allowed_mistakes = 3
        self.mistakes = 0
        self.start_time = time.time()
        self.timer_running = True
        self.selected_cell = None
        self.button_pressed = False
        self.number_color = ""
        self.key = None
        self.game_over_flag = False

        self.screen = pygame.display.set_mode((596.6, 750))
        pygame.display.set_caption("Sudoku")

    def get_cell_position(self, mouse_x, mouse_y):
        """Convert mouse coordinates to grid cell indices."""
        row = mouse_y // self.CELL_SIZE
        col = mouse_x // self.CELL_SIZE + 1
        return row, col

    def is_out_of_grid(self, cell):
        """Check if a cell is out of bounds."""
        if cell[0] > 9 or cell[0] < 1:
            return True
        return False

    def draw_grid(self):
        """Draw the Sudoku grid on the screen."""
        for i in range(self.GRID_SIZE + 1):
            line_thickness = 2 if i % 3 == 0 else 1  # Thick lines for box boundaries

            pygame.draw.line(self.screen, self.WHITE, (i * self.CELL_SIZE, self.CELL_SIZE),
                             (i * self.CELL_SIZE, self.GRID_HEIGHT + 61), line_thickness)  # vertical
            pygame.draw.line(self.screen, self.WHITE, (0, i * self.CELL_SIZE + self.CELL_SIZE),
                             (self.GRID_WIDTH, i * self.CELL_SIZE + self.CELL_SIZE),
                             line_thickness)  # horizontal

    def draw_static_numbers(self, grid):
        """Draw the static numbers on the Sudoku grid."""
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                number = grid[row][col]
                if number != 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(number), True, self.WHITE)
                    text_rect = text.get_rect(
                        center=(col * self.CELL_SIZE + self.CELL_SIZE // 2,
                                row * self.CELL_SIZE + self.CELL_SIZE // 2 + self.CELL_SIZE))
                    self.screen.blit(text, text_rect)

    def format_elapsed_time(self):
        """Calculate and format the elapsed time."""
        elapsed_time = time.time() - self.start_time
        elapsed_time_seconds = int(elapsed_time)
        elapsed_time_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed_time_seconds))
        return elapsed_time_formatted

    def draw_elapsed_time(self, elapsed_time_formatted):
        """Draw the elapsed time on the screen."""
        font = pygame.font.Font(None, 30)
        text = font.render(elapsed_time_formatted, True, self.WHITE)
        self.screen.blit(text, (500, self.CELL_SIZE / 2))

    def highlight_selected_cell(self):
        """Highlight the selected cell's border."""
        if self.selected_cell and not self.is_out_of_grid(self.selected_cell):
            cell_x = (self.selected_cell[1] - 1) * self.CELL_SIZE
            cell_y = (self.selected_cell[0] - 1) * self.CELL_SIZE
            pygame.draw.rect(self.screen, self.CYAN,
                             (cell_x, cell_y + self.CELL_SIZE, self.CELL_SIZE + 2, self.CELL_SIZE), 2)

    def insert_value(self, value, coords):
        """Insert a new value into the Sudoku grid."""
        row, col = coords
        if self.sudoku_grid[row][col] == 0:
            self.sudoku_grid[row][col] = value

    def draw_number(self, number, coords, color):
        """Draw a number on the screen with a specified color."""
        row, col = coords
        font = pygame.font.Font(None, 36)
        text = font.render(str(number), True, color)
        text_rect = text.get_rect(
            center=(
            col * self.CELL_SIZE + self.CELL_SIZE // 2, row * self.CELL_SIZE + self.CELL_SIZE // 2 + self.CELL_SIZE))
        self.screen.blit(text, text_rect)

    def draw_mistakes(self):
        """Draw the number of mistakes on the screen."""
        font = pygame.font.Font(None, 30)
        text = font.render(f"{self.mistakes}/{self.allowed_mistakes}", True, self.WHITE)
        self.screen.blit(text, (285, 695))

    def draw_game_over(self, x, y):
        """Display the 'GAME OVER' message on the screen."""
        button_width, button_height = 150, 40
        button_color = self.RED
        border_radius = 30
        text_color = (0, 0, 0)
        text_font = pygame.font.Font(None, 30)
        button_text = "YOU LOST"
        button_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=border_radius)
        text_surface = text_font.render(button_text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_you_won(self, x, y):
        """Display the 'YOU WON' message on the screen."""
        button_width, button_height = 150, 40
        button_color = self.CYAN
        border_radius = 30
        text_color = (0, 0, 0)
        text_font = pygame.font.Font(None, 30)
        button_text = "YOU WON"
        won_button_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(self.screen, button_color, won_button_rect, border_radius=border_radius)
        text_surface = text_font.render(button_text, True, text_color)
        text_rect = text_surface.get_rect(center=won_button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_solve_button(self, x, y):
        """Draw the SOLVE button on the screen."""
        button_width, button_height = 150, 40
        button_color = self.GREEN
        border_radius = 30
        text_color = (0, 0, 0)
        text_font = pygame.font.Font(None, 30)
        button_text = "SOLVE"
        solve_button_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(self.screen, button_color, solve_button_rect, border_radius=border_radius)
        text_surface = text_font.render(button_text, True, text_color)
        text_rect = text_surface.get_rect(center=solve_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        return solve_button_rect

    def draw_reset_button(self, x, y):
        """Draw the RESET button on the screen."""
        button_width, button_height = 150, 40
        button_color = self.GREEN
        border_radius = 30
        text_color = (0, 0, 0)
        text_font = pygame.font.Font(None, 30)
        button_text = "RESET"
        reset_button_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(self.screen, button_color, reset_button_rect, border_radius=border_radius)
        text_surface = text_font.render(button_text, True, text_color)
        text_rect = text_surface.get_rect(center=reset_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        return reset_button_rect

    def solve_sudoku(self, board):
        def find_empty_location(bo):
            for r in range(len(bo)):
                for c in range(len(bo[r])):
                    if bo[r][c] == 0:
                        return r, c

        def is_valid(bo, num, pos):
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
                    if bo[x][y] == num and (x, y) != pos:
                        return False
            return True

        def solve(bo):
            find = find_empty_location(bo)
            if not find:
                return True
            else:
                row, col = find

            for i in range(1, 10):
                if is_valid(bo, i, (row, col)):
                    bo[row][col] = i

                    if solve(bo):
                        return True

                    bo[row][col] = 0

            return False

        solve(board)
        return board

    def main(self):
        self.solve_sudoku(self.solution_grid)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.selected_cell = self.get_cell_position(mouse_x, mouse_y)
                    if self.button_pressed:
                        self.key = ""

                    solve_button_rect = self.draw_solve_button(420, 685)
                    reset_button_rect = self.draw_reset_button(25, 685)

                    if solve_button_rect.collidepoint(mouse_x, mouse_y):
                        self.sudoku_grid = self.solve_sudoku(self.solution_grid)
                        self.game_over_flag = True

                    elif reset_button_rect.collidepoint(mouse_x, mouse_y):
                        self.sudoku_grid = self.initial_grid
                        self.start_time = time.time()
                        self.mistakes = 0
                        self.game_over_flag = False

                if not self.game_over_flag:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                            self.key = 1
                        elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                            self.key = 2
                        elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                            self.key = 3
                        elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                            self.key = 4
                        elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                            self.key = 5
                        elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                            self.key = 6
                        elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                            self.key = 7
                        elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                            self.key = 8
                        elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                            self.key = 9

                        self.sci = [x - 1 for x in self.selected_cell]

                        if self.key is not None and self.selected_cell and self.sudoku_grid[self.selected_cell[0] - 1][
                            self.selected_cell[1] - 1] == 0:
                            self.button_pressed = True

                            if self.key == self.solution_grid[self.sci[0]][self.sci[1]]:
                                self.number_color = self.WHITE
                                self.insert_value(self.key, self.sci)
                            else:
                                self.mistakes += 1
                                self.number_color = self.RED

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_solve_button(420, 685)
            self.draw_reset_button(25, 685)
            self.draw_static_numbers(self.sudoku_grid)
            self.highlight_selected_cell()

            if not self.game_over_flag:
                self.current_time = self.format_elapsed_time()

            self.draw_elapsed_time(self.current_time)

            if self.mistakes == self.allowed_mistakes:
                self.draw_mistakes()
                self.game_over_flag = True
                self.draw_game_over(225, 685)
            else:
                self.draw_mistakes()

            if self.key is not None and self.number_color != "" and self.sudoku_grid[self.sci[0]][self.sci[1]] == 0:
                self.draw_number(self.key, self.sci, self.number_color)

            if sum(1 for row in self.sudoku_grid for val in row if val != 0) == 81:
                if self.game_over_flag:
                    pass
                else:
                    self.game_over_flag = True
                    self.draw_you_won(225, 685)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SudokuGame()
    game.main()
