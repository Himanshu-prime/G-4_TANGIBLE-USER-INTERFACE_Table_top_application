import pygame
import sys
from pythontuio import TuioListener, TuioClient
from threading import Thread
import time
import random
import copy

def generate_sorted_random_list(n):
    random_list = [random.randint(1, 15) for _ in range(n)]  # Generating a list of n random numbers
    #random_list.sort()  # Sorting the list in ascending order
    return random_list
# Initialize Pygame
pygame.init()
current_i = 0
current_j = 0
# Constants
WIDTH, HEIGHT = 800, 600
WHITE =(253, 219, 202)
BAR_COLOR = (102,204,255)
PURPLE=(255,51,255)
BAR_WIDTH = 40
BAR_GAP = 18
FONT_SIZE = 40
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED=(225,0,0)
BLACK=(0,0,0)
font = pygame.font.Font(None, FONT_SIZE)
screen_info = pygame.display.Info()  # Get display information
WIDTH = screen_info.current_w  # Screen width
HEIGHT = screen_info.current_h  # Screen height
h=0
g=0
# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dynamic Bars')
screen.fill(WHITE)
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
swap_k=0
swap_progress = 0.0
a=0
b=0

def selection_sort_step():
    global arr, swap_i, swap_j, swap_progress, current_step,g,h,swap_i,swap_j,swap_k
    global a
    global b
    
    n = len(arr)
    for i in range(n):
        min_idx = i
        current_step = 1
        display_pseudo_code()
        pygame.display.flip()
        #time.sleep(2.5)
        swap_i=i
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


array_check=0
history=[]
class CustomTuioListener(TuioListener):
    def __init__(self):
        super().__init__()
        self.trigg=set()

    def update_tuio_object(self, obj):
        x, y = obj.position
        global array_check
        global arr
        global running
        global history
        c = obj.class_id
        # Check if the object ID is not in the mapping
        if obj.class_id not in self.trigg:
            if c ==136:
                selection_sort_step()
                current_step=6
                update_display3()
                object_to_bar.add(obj.class_id)
            elif c==135:
                array_check=0
                arr=generate_sorted_random_list(0)
                
                update_display(-1, -1, 100)
                object_to_bar.add(obj.class_id)
                pygame.display.flip()
            elif c==134:
                arr=history
                print(arr)
                update_display(-1, -1, 100)
                object_to_bar.add(obj.class_id)
                pygame.display.flip()
            elif c==137:
                screen.fill(WHITE)
                font = pygame.font.Font(None, FONT_SIZE+50)  # Initialize font
                message = "Exiting the visualization. Comeback soon"
                text_surface = font.render(message, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
                screen.blit(text_surface, text_rect)
                pygame.display.flip()
                time.sleep(2)
                running=False
                #pygame.display.quit()
                pygame.quit()
                sys.exit()
                
                
            elif c<=15:
                array_check=1
                arr=generate_sorted_random_list(obj.class_id)
                history=copy.deepcopy(arr)
                print(arr)
                update_display(-1, -1, 100)
                object_to_bar.add(obj.class_id)
                pygame.display.flip()
 
            self.trigg.add(obj.class_id)
    def remove_tuio_object(self, obj):
        if obj.class_id in self.trigg:
            self.trigg.remove(obj.class_id)
# Create an instance of your custom TUIO listener
listener = CustomTuioListener()

# Create a TUIO client and add the listener
client = TuioClient(("0.0.0.0", 3333))
client.add_listener(listener)

# Start the TUIO client in a separate thread
t = Thread(target=client.start)
t.start()
def update_display3():
    total_width = len(arr) * (BAR_WIDTH + BAR_GAP)
    screen.fill(WHITE)
    display_pseudo_code()
    for i, value in enumerate(arr):
        x = (WIDTH - total_width) // 2 + i * (BAR_WIDTH + BAR_GAP)
        y = HEIGHT - value * 30
        pygame.draw.rect(screen, GREEN, pygame.Rect(x, y, BAR_WIDTH, value * 30))

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
        elif i==k:
            pygame.draw.rect(screen, YELLOW, pygame.Rect(x, y, BAR_WIDTH, value * 30))
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
    #if sorting:
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
    x = 0  # Adjust the x-coordinate for the code block
    y = 0  # Adjust the y-coordinate for the code block
    code_font = pygame.font.Font(None, 24)
    block_width = WIDTH // 3
    block_height = 220
    global current_i
    global current_j
    global array_check
    global current_step
    global g,h
    # Fill the code block area with a grey background color
    pygame.draw.rect(screen, (200, 200, 200), (x, y, block_width, block_height))
    
    # Draw a border around the right side of the pseudo code section
    pygame.draw.rect(screen, (0, 0, 0), (x + block_width - 2, y, 2, block_height), 2)  # Border is 2 pixels wide
    
    # Display the pseudo code
    for i, line in enumerate(pseudo_code):
        text_surface = code_font.render(line, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x + 10, y + 10 + i * 30)
        
        if i == current_step:
            pygame.draw.rect(screen, (255, 165, 0), (x + 6, y + 10 + i * 30, block_width - 8, 30))  # Highlight the current step
        else:
            pygame.draw.rect(screen, (200, 200, 200), (x + 6, y + 10 + i * 30, block_width - 8, 30))
        
        screen.blit(text_surface, text_rect)
    
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
    elif current_step == 5 and g<len(arr): 
        comments.append(f"Bring {arr[g]} at its correct place")
   
    elif current_step==6:
        comments.append(f"Finished iteration")  # Add comments for other steps
    comment_block_width = WIDTH // 3
    comment_block_height = 220
    pygame.draw.rect(screen, (200, 200, 200), (x + block_width, y, comment_block_width, block_height))
    pygame.draw.rect(screen, (0, 0, 0), (x + block_width, y, 2, block_height), 2)  # Border on the left side
    
    # Add the comments above the code
    for i, comment in enumerate(comments):
        comment_surface = code_font.render(comment, True, (0, 0, 0))
        comment_rect = comment_surface.get_rect()
        comment_rect.topleft = (x + block_width + 20, y + 30 + i * 30)
        screen.blit(comment_surface, comment_rect)

    # Draw a border around the pseudo code section
    
    print(g,h)
        # Display i value in a separate block next to the comments section
    ij_block_width = WIDTH // 3
    ij_block_height = 80
    pygame.draw.rect(screen, (200, 200, 200), (x + block_width + comment_block_width, y, ij_block_width, block_height))
    pygame.draw.rect(screen, (0, 0, 0), (x + block_width + comment_block_width, y, 2, block_height), 2)  # Border
    ij_font = pygame.font.Font(None, 24)
    i_text_surface = ij_font.render(f"i = {current_i}", True, (0, 0, 0))
    i_text_rect = i_text_surface.get_rect()
    i_text_rect.topleft = (x + block_width + comment_block_width + 10, y + 20)
    screen.blit(i_text_surface, i_text_rect)
    
    # Display j value in the separate block next to the comments section
    j_text_surface = ij_font.render(f"local mis is at index = {g}", True, (0, 0, 0))
    j_text_rect = j_text_surface.get_rect()
    j_text_rect.topleft = (x + block_width + comment_block_width + 10, y + 50)
    screen.blit(j_text_surface, j_text_rect)

    j_text_surface = ij_font.render(f"j = {h}", True, (0, 0, 0))
    j_text_rect = j_text_surface.get_rect()
    j_text_rect.topleft = (x + block_width + comment_block_width + 10, y + 80)
    screen.blit(j_text_surface, j_text_rect)

    instruction_width=WIDTH//2
    instruction_height=HEIGHT//2
    if array_check == 0:
        # Display a message if the array size is zero
        #screen.fill(B_BLUE)  # Clear the screen before drawing
        font = pygame.font.Font(None, FONT_SIZE)  # Initialize font
        message = "Choose size n to generate an array of size n"
        text_surface = font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(instruction_width, instruction_height))
        screen.blit(text_surface, text_rect)


# Main loop
display_pseudo_code()
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
