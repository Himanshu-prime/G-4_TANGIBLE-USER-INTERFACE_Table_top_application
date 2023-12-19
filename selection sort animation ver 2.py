import pygame
import sys
from pythontuio import TuioListener, TuioClient
from threading import Thread
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BAR_COLOR = (102, 204, 255)
PURPLE=(255,51,255)
BAR_WIDTH = 40
BAR_GAP = 18
FONT_SIZE = 20
ORANGE = (255, 165, 0)
RED = (225, 0, 0)
GREEN = (255,165,0)
font = pygame.font.Font(None, FONT_SIZE)

HOME_PAGE_FONT_SIZE = 36
HOME_PAGE_TEXT_COLOR = (0, 0, 0)
HOME_PAGE_BG_COLOR = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Selection Sort Visualization')
arr = []

# Dictionary to map TUIO object IDs to bars
object_to_bar = set()
sorting = False
pseudo_code = [
    "for i from 0 to n-1:",
    "   min_idx = i",
    "   for j from i+1 to n:",
    "       if arr[j] < arr[min_idx]:",
    "           min_idx = j",
    "   swap(arr[i], arr[min_idx])"
]
current_step = 0
swap_i = 0
swap_j = 0
swap_progress = 0.0
a=0
b=0

# Function to display the home page
def display_home_page():
    screen.fill(HOME_PAGE_BG_COLOR)

    # Display a welcome message
    welcome_font = pygame.font.Font(None, HOME_PAGE_FONT_SIZE)
    welcome_text = welcome_font.render("Selection Sort Visualizer", True, HOME_PAGE_TEXT_COLOR)
    welcome_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(welcome_text, welcome_rect)

    # Display instructions
    instructions_font = pygame.font.Font(None, 24)
    instruction1 = instructions_font.render("Place the fiducial id you wish to insert in the array for visualization.", True, HOME_PAGE_TEXT_COLOR)
    instruction2 = instructions_font.render("Place fiducial id of 50 to begin the visualization.", True, HOME_PAGE_TEXT_COLOR)
    instruction1_rect = instruction1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    instruction2_rect = instruction2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(instruction1, instruction1_rect)
    screen.blit(instruction2, instruction2_rect)

    pygame.display.flip()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Selection Sort Visualization')

# Display the home page initially
display_home_page()

def selection_sort_step():
    global arr, swap_i, swap_j, swap_progress, current_step,g,h
    global a
    global b
    
    n = len(arr)
    for i in range(n):
        min_idx = i
        current_step = 1
        display_pseudo_code()
        pygame.display.flip()
        #time.sleep(2.5)
        
        time.sleep(2.5)
        for j in range(i + 1, n):
            g=min_idx
            h=j
            time.sleep(0.5)
            update_display2(i,j,min_idx)
            pygame.display.flip()
            current_step = 2
            display_pseudo_code()
            pygame.display.flip()
            time.sleep(2.5)
            current_step = 3
            display_pseudo_code()
            pygame.display.flip()
            time.sleep(2.5)
            
            if arr[j] < arr[min_idx]:
                min_idx = j
                current_step = 4
                display_pseudo_code()
                pygame.display.flip()
                update_min(i,j)
                time.sleep(2.5)
                
                
                
            

        swap_i = i
        swap_j = min_idx
        a=swap_i
        b=swap_j
        swap_progress = 0.0
        current_step = 5  # Highlight the step where a swap occurs
        display_pseudo_code()
        pygame.display.flip()
        if(swap_j!=swap_i):
            
            while a<swap_j and b>swap_i:
                block_swap_animation(swap_i, swap_j)  # Swap the two blocks with animation
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        #current_step = 2  # Highlight the step where a swap occurs


def block_swap_animation(i, j):
    global swap_progress
    global a
    global b
    while a<j and b>i:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)  # Clear the screen
        display_pseudo_code()
        total_width = len(arr) * (BAR_WIDTH + BAR_GAP)
        for idx, value in enumerate(arr):
            x = (WIDTH - total_width) // 2 + idx * (BAR_WIDTH + BAR_GAP)
            y = HEIGHT - value * 30
            if idx == i:
                block_x = x + ( 60*swap_progress)
                pygame.draw.rect(screen, RED, pygame.Rect(block_x, y, BAR_WIDTH, value * 30))
            elif idx == j:
                block_x = x - (60*swap_progress)
                pygame.draw.rect(screen, PURPLE, pygame.Rect(block_x, y, BAR_WIDTH, value * 30))
            else:
                block_x = x
                pygame.draw.rect(screen, BAR_COLOR, pygame.Rect(block_x, y, BAR_WIDTH, value * 30))

            # Render and display the number above the bar
            text_surface = font.render(str(value), True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = (block_x + BAR_WIDTH // 2, y - FONT_SIZE // 2)
            screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()

        # Slow down the animation
        pygame.time.delay(30)

        # Update the swap progress
        swap_progress += 0.1
        a+=0.1
        b-=0.1


class CustomTuioListener(TuioListener):
    def __init__(self):
        super().__init__()

    def update_tuio_object(self, obj):
        x, y = obj.position
        c = obj.class_id
        print(c)
        # Check if the object ID is not in the mapping
        if obj.class_id not in object_to_bar:
            if c > 50:
                #update_display(-1, -1, 100)
                selection_sort_step()
                
                current_step = -11  # Highlight the step where a swap occurs
                display_pseudo_code()
                pygame.display.flip()
                time.sleep(1.5)
                update_display2(-1,-1,-1)
                object_to_bar.add(obj.class_id)
            else:
                arr.append(obj.class_id)
                update_display(-1, -1, 100)
                object_to_bar.add(obj.class_id)

# Create an instance of your custom TUIO listener
listener = CustomTuioListener()

# Create a TUIO client and add the listener
client = TuioClient(("localhost", 3333))
client.add_listener(listener)

# Start the TUIO client in a separate thread
t = Thread(target=client.start)
t.start()
def update_display3(j, k):
    total_width = len(arr) * (BAR_WIDTH + BAR_GAP)
    screen.fill(WHITE)
    display_pseudo_code()
    for i, value in enumerate(arr):
        x = (WIDTH - total_width) // 2 + i * (BAR_WIDTH + BAR_GAP)
        y = HEIGHT - value * 30
        if i == j or i == k:
            pygame.draw.rect(screen, RED, pygame.Rect(x, y, BAR_WIDTH, value * 30))
        else:
            pygame.draw.rect(screen, BAR_COLOR, pygame.Rect(x, y, BAR_WIDTH, value * 30))

        # Render and display the number above the bar
        text_surface = font.render(str(value), True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x + BAR_WIDTH // 2, y - FONT_SIZE // 2)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
def update_min(k,j):
    total_width = len(arr) * (BAR_WIDTH + BAR_GAP)
    screen.fill(WHITE)
    display_pseudo_code()
    for i, value in enumerate(arr):
        x = (WIDTH - total_width) // 2 + i * (BAR_WIDTH + BAR_GAP)
        y = HEIGHT - value * 30
        if i == j:
            pygame.draw.rect(screen, PURPLE, pygame.Rect(x, y, BAR_WIDTH, value * 30))
        elif i==k:
            pygame.draw.rect(screen, RED, pygame.Rect(x, y, BAR_WIDTH, value * 30))
        else:
            pygame.draw.rect(screen, BAR_COLOR, pygame.Rect(x, y, BAR_WIDTH, value * 30))

        # Render and display the number above the bar
        text_surface = font.render(str(value), True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x + BAR_WIDTH // 2, y - FONT_SIZE // 2)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

def update_display2(j,k,l):
    total_width = len(arr) * (BAR_WIDTH + BAR_GAP)
    screen.fill(WHITE)
    display_pseudo_code()
    for i, value in enumerate(arr):
        x = (WIDTH - total_width) // 2 + i * (BAR_WIDTH + BAR_GAP)
        y = HEIGHT - value * 30
        if i == j:
            pygame.draw.rect(screen, RED, pygame.Rect(x, y, BAR_WIDTH, value * 30))
        elif i==l:
            pygame.draw.rect(screen, PURPLE, pygame.Rect(x, y, BAR_WIDTH, value * 30))
        else:
            pygame.draw.rect(screen, BAR_COLOR, pygame.Rect(x, y, BAR_WIDTH, value * 30))

        # Render and display the number above the bar
        text_surface = font.render(str(value), True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x + BAR_WIDTH // 2, y - FONT_SIZE // 2)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()


def update_display(j, k, limit):
    total_width = len(arr) * (BAR_WIDTH + BAR_GAP)
    screen.fill(WHITE)
    if sorting:
        display_pseudo_code()
    for i, value in enumerate(arr):
        if i <= limit:
            x = (WIDTH - total_width) // 2 + i * (BAR_WIDTH + BAR_GAP)
            y = HEIGHT - value * 30
            if i == j:
                pygame.draw.rect(screen, RED, pygame.Rect(x, y, BAR_WIDTH, value * 30))
            elif i == k:
                pygame.draw.rect(screen, RED, pygame.Rect(x, y, BAR_WIDTH, value * 30))
            else:
                pygame.draw.rect(screen, BAR_COLOR, pygame.Rect(x, y, BAR_WIDTH, value * 30))
        else:
            x = (WIDTH - total_width) // 2 + i * (BAR_WIDTH + BAR_GAP)
            y = HEIGHT - value * 30
            pygame.draw.rect(screen, GREEN, pygame.Rect(x, y, BAR_WIDTH, value * 30))
        # Render and display the number above the bar
        text_surface = font.render(str(value), True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x + BAR_WIDTH // 2, y - FONT_SIZE // 2)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()


def display_pseudo_code():
    x = WIDTH - 240  # Adjust the x-coordinate for the code block
    y = 60
    code_font = pygame.font.Font(None, 24)
    global g,h
    # Clear the area above the code block by filling it with the background color
    pygame.draw.rect(screen, WHITE, (x, y - 60, 250, 60))
    global current_step
    # Draw a border around the comment section
    pygame.draw.rect(screen, (0, 0, 0), (x - 40, y - 40, 250, 30), 2)

    # Add comments based on the current step
    
    comments = []
    if current_step == 0:
        comments.append("Increment i")
    if current_step == 1:
        comments.append("Initialize min")
    elif current_step == 2:
        comments.append("Increment J")
    elif current_step == 3:
        comments.append(f"comapring {arr[g]} with {arr[h]}")
    elif current_step == 4:
        comments.append(f"Found a smaller element")
    elif current_step == 5:
        comments.append(f"Bring {arr[swap_j]} at its correct place")
   
    else:
        comments.append(f"Finished iteration")  # Add comments for other steps

    # Add the comments above the code
    for i, comment in enumerate(comments):
        comment_surface = code_font.render(comment, True, (0, 0, 0))
        comment_rect = comment_surface.get_rect()
        comment_rect.topleft = (x, y - (i + 1) * 30)  # Position comments above the code
        screen.blit(comment_surface, comment_rect)

    # Draw a border around the pseudo code section
    code_section_height = len(pseudo_code) * 30
    pygame.draw.rect(screen, (0, 0, 0), (x - 40, y - 40, 250, code_section_height+45), 2)

    # Display the pseudo code
    for i, line in enumerate(pseudo_code):
        text_surface = code_font.render(line, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y + i * 30)

        if i == current_step:
            pygame.draw.rect(screen, ORANGE, (x - 4, y + i * 30, 200, 30))  # Highlight the current step
        else:
            pygame.draw.rect(screen, WHITE, (x - 4, y + i * 30, 200, 30))

        screen.blit(text_surface, text_rect)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Start the sorting visualization when 'Space' is pressed
            sorting = True
            display_pseudo_code()  # Display pseudo code
            pygame.display.flip()

    pygame.time.delay(10)

pygame.quit()
sys.exit()
