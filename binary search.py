import pygame
import sys
from pythontuio import TuioListener, TuioClient
from threading import Thread
import time
import random
import copy
def generate_sorted_random_list(n):
    random_list = [random.randint(1, 10) for _ in range(n)]  # Generating a list of n random numbers
    random_list.sort()  # Sorting the list in ascending order
    return random_list

# Constants
WIDTH, HEIGHT = 800, 200
WHITE = (255, 255, 255)
GREEN =(0,233,0)
B_BLUE=(253, 219, 202)
BLACK = (0, 0, 0)
GREY = (223,223,223)
BOX_SIZE = 80
MARGIN = 5
object_to_bar = set()
FONT_SIZE = 20
screen_width = 800
screen_height = 600
# Pygame initialization
pygame.init()
screen_info = pygame.display.Info()  # Get display information
screen_width = screen_info.current_w  # Screen width
screen_height = screen_info.current_h  # Screen height
WIDTH=screen_width
HEIGHT=screen_height
key=-1
flags = pygame.FULLSCREEN
screen = pygame.display.set_mode((screen_width, screen_height), flags)
pygame.display.set_caption('Matrix-like Box with One Row')

num_columns=[]  # Default number of columns
history=[]
# Function to draw the matrix box
highlight_step=1
def binary_s():

    s=0
    mid=0
    e=len(num_columns)-1
    while(s<=e):
            mid=(int)((e-s)/2)+s
            draw_matrix(num_columns,s,e,mid,2)
            pygame.display.flip()
            time.sleep(4)
            if(num_columns[mid]==key):
                draw_matrix(num_columns,s,e,mid,3)
                pygame.display.flip()
                time.sleep(4)
                draw_matrix(num_columns,s,e,mid,4)
                pygame.display.flip()
                time.sleep(4)
                break
            elif(num_columns[mid]>key):
                draw_matrix(num_columns,s,e,mid,5)
                pygame.display.flip()
                time.sleep(4)
                e=mid-1
                draw_matrix(num_columns,s,e,mid,6)
                pygame.display.flip()
                time.sleep(4)
                
            else:
                s=mid+1
                draw_matrix(num_columns,s,e,mid,7)
                pygame.display.flip()
                time.sleep(4)
                draw_matrix(num_columns,s,e,mid,8)
                pygame.display.flip()
                time.sleep(4)
    if s>e:
        draw_matrix(num_columns,s,e,mid,11)
    else:
        draw_matrix(num_columns,s,e,mid,12)
        
        
def draw_matrix(n, s, e,mid,step):
    if len(n) == 0:
        # Display a message if the array size is zero
        screen.fill(B_BLUE)  # Clear the screen before drawing
        font = pygame.font.Font(None, FONT_SIZE+30)  # Initialize font
        message = "Choose size n to generate an array of size n"
        text_surface = font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)
    else:
        
    
        screen.fill(B_BLUE)
        if key == -1:
            font = pygame.font.Font(None, FONT_SIZE)  # Initialize font
            key_message = "Choose a key"
            key_text_surface = font.render(key_message, True, BLACK)
            key_text_rect = key_text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 80))
            screen.blit(key_text_surface, key_text_rect)
            
        # Clear the screen before drawing
        # Define the dimensions of the top box
    top_box_height = (screen_height // 5)+80
    top_box_width = screen_width

    # Divide the top box into 3 equal parts
    section_width = top_box_width // 3

    # Draw the top box and divide it into three sections
    top_box_rect = pygame.Rect(0, 0, top_box_width, top_box_height)
    pygame.draw.rect(screen, GREY, top_box_rect)

    font = pygame.font.Font(None, FONT_SIZE)  # Initialize font

    pseudocode = [
        "1. Initialize start (s) and end (e) indices.",
        "2. While s is less than or equal to e:",
        "     a. Calculate mid index.",
        "     b. If element at mid is the target:",
        "         - Element found, break the loop.",
        "     c. If element at mid is greater than the target:",
        "         - Update e to mid - 1.",
        "     d. If element at mid is less than the target:",
        "         - Update s to mid + 1."
    ]
    comments = {
        1: "Initialization step.",
        2: "Entering loop to find the target.",
        3: "Calculating mid point.",
        4: "Checking if mid element is the target.",
        5: "Target found, exiting loop.",
        6: "checking if Mid element > target",
        7:  "Since Mid element is greater target we update e",
        8: "Mid element < target.",
        9: "Since element < target we update s",
        11: "Element not found in the array",
        12: "Element found"
    }
    text_color = BLACK  # Default text color
    track=[f"s={s}",f"e={e}",f"mid={mid}",f"key={key}"]
    track_font= pygame.font.Font(None, FONT_SIZE+20)
    for i in range (len(track)):
        
        track_surface=track_font.render(track[i],True,BLACK)
        track_rect =track_surface.get_rect(topleft=(MARGIN+970,50+ i * (FONT_SIZE + MARGIN)))
        screen.blit(track_surface,track_rect)
    for i in range(len(pseudocode)):
        text_surface = font.render(pseudocode[i], True, BLACK)
        text_rect = text_surface.get_rect(topleft=(MARGIN, 0 + MARGIN + i * (FONT_SIZE + MARGIN)))

        # Highlight the current step based on 'highlight_step'
        if i == step:
            pygame.draw.rect(screen, GREEN, (text_rect.x - MARGIN // 2, text_rect.y, screen_width//3, FONT_SIZE + MARGIN), 0)
            text_color = WHITE  # Change text color for highlighted step
        if step + 1 in comments:
            comment = comments[step + 1]
            comment_font = pygame.font.Font(None, FONT_SIZE+8)
            comment_surface = comment_font.render(comment, True, BLACK)
            comment_rect = comment_surface.get_rect(topleft=(MARGIN + 470, 50 + MARGIN))
            screen.blit(comment_surface, comment_rect)
        screen.blit(text_surface, text_rect)
    #screen.fill(B_BLUE)  # Clear the screen before drawing
    if step==11:
        comment = comments[11]
        comment_font = pygame.font.Font(None, FONT_SIZE+5)
        comment_surface = comment_font.render(comment, True, BLACK)
        comment_rect = comment_surface.get_rect(topleft=(MARGIN + 470, 50 + MARGIN))
        screen.blit(comment_surface, comment_rect)
        screen.blit(text_surface, text_rect)
    if step==12:
        comment = comments[12]
        comment_font = pygame.font.Font(None, FONT_SIZE+5)
        comment_surface = comment_font.render(comment, True, BLACK)
        comment_rect = comment_surface.get_rect(topleft=(MARGIN + 470, 50 + MARGIN))
        screen.blit(comment_surface, comment_rect)
        screen.blit(text_surface, text_rect)
        
    # Draw lines to divide the top box into three equal sections
    for i in range(1, 3):
        if i==2:
           pygame.draw.line(screen, BLACK, (section_width * i+80, 0), (section_width * i+80, top_box_height), 2)
        else:
            pygame.draw.line(screen, BLACK, (section_width * i, 0), (section_width * i, top_box_height), 2)

    
    total_width = len(n) * (BOX_SIZE + MARGIN)
    start_x = (screen_width - total_width) // 2 
    total_height = BOX_SIZE + MARGIN  # Height of a single row
    start_y = (screen_height - total_height) // 2
    
    for i in range(len(n)):
        if i >= s and i <= e and i != mid:
            box_rect = pygame.Rect(start_x + i * (BOX_SIZE + MARGIN),start_y, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(screen, BLACK, box_rect, 2)
            font = pygame.font.Font(None, FONT_SIZE+20)  # Initialize font
            text_surface = font.render(str(n[i]), True, BLACK)
            text_rect = text_surface.get_rect(center=box_rect.center)
            screen.blit(text_surface, text_rect)
        elif i==mid:
            box_rect = pygame.Rect(start_x + i * (BOX_SIZE + MARGIN),start_y, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(screen, GREEN, box_rect, 2)
            font = pygame.font.Font(None, FONT_SIZE+20)  # Initialize font
            text_surface = font.render(str(n[i]), True, GREEN)
            text_rect = text_surface.get_rect(center=box_rect.center)
            screen.blit(text_surface, text_rect)
        elif -1==mid:
            box_rect = pygame.Rect(start_x + i * (BOX_SIZE + MARGIN),start_y, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(screen, BLACK, box_rect, 2)
            font = pygame.font.Font(None, FONT_SIZE+20)  # Initialize font
            text_surface = font.render(str(n[i]), True, BLACK)
            text_rect = text_surface.get_rect(center=box_rect.center)
            screen.blit(text_surface, text_rect)
        else:
            box_rect = pygame.Rect(start_x + i * (BOX_SIZE + MARGIN), start_y, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(screen, GREY, box_rect, 2)
            font = pygame.font.Font(None, FONT_SIZE)  # Initialize font
            text_surface = font.render(str(n[i]), True, GREY)
            text_rect = text_surface.get_rect(center=box_rect.center)
            screen.blit(text_surface, text_rect)

    # Draw arrows and labels below s and e
    if key != -1:
        arrow_surface = font.render("↑", True, BLACK)
        arrow_rect_s = arrow_surface.get_rect(center=(start_x + s * (BOX_SIZE + MARGIN) + BOX_SIZE // 2, start_y + BOX_SIZE // 2 + 60))
        arrow_rect_e = arrow_surface.get_rect(center=(start_x + e * (BOX_SIZE + MARGIN) + BOX_SIZE // 2, start_y+ BOX_SIZE // 2 + 60))
        arrow_rect_mid = arrow_surface.get_rect(center=(start_x + mid * (BOX_SIZE + MARGIN) + BOX_SIZE // 2, start_y + BOX_SIZE // 2 + 60))
        screen.blit(arrow_surface, arrow_rect_s)
        screen.blit(arrow_surface, arrow_rect_e)
        screen.blit(arrow_surface, arrow_rect_mid)

        label_font = pygame.font.Font(None, FONT_SIZE)
        label_surface_s = label_font.render(f"s={s}", True, BLACK)
        label_rect_s = label_surface_s.get_rect(midtop=(arrow_rect_s.centerx, arrow_rect_s.bottom + 5))
        screen.blit(label_surface_s, label_rect_s)

        label_surface_e = label_font.render(f"e={e}", True, BLACK)
        label_surface_mid = label_font.render(f"mid={mid}", True, BLACK)
        if  s!=e:
            if mid !=e:
                label_rect_e = label_surface_e.get_rect(midtop=(arrow_rect_e.centerx, arrow_rect_e.bottom + 5))
            else:
                label_rect_e = label_surface_e.get_rect(midtop=(arrow_rect_e.centerx, arrow_rect_e.bottom + 25))
            screen.blit(label_surface_e, label_rect_e)

            
            if mid != s:
                label_rect_mid = label_surface_mid.get_rect(midtop=(arrow_rect_mid.centerx, arrow_rect_mid.bottom + 5))
            else:
                label_rect_mid = label_surface_mid.get_rect(midtop=(arrow_rect_mid.centerx, arrow_rect_mid.bottom + 25))
            screen.blit(label_surface_mid, label_rect_mid)
        else:
            label_rect_e = label_surface_e.get_rect(midtop=(arrow_rect_e.centerx, arrow_rect_e.bottom + 25))
            label_rect_mid = label_surface_mid.get_rect(midtop=(arrow_rect_mid.centerx, arrow_rect_mid.bottom + 45))
            screen.blit(label_surface_e, label_rect_e)
            screen.blit(label_surface_mid, label_rect_mid)
            


class CustomTuioListener(TuioListener):
    def __init__(self):
        super().__init__()
        self.trigg=set()
        
        #self.trigg=0

    def update_tuio_object(self, obj):
        global num_columns
        global key
        global history
        x, y = obj.position
        c = obj.class_id
        # Check if the object ID is not in the mapping object_to_bar.add(obj.class_id)
        if obj.class_id not in self.trigg:
            print(obj.class_id)
            if obj.class_id == 135:
                num_columns=[]
                key=-1
                draw_matrix(num_columns,s,e,mid,2)
                self.trigg.add(obj.class_id)
            elif obj.class_id==134:
                num_columns=copy.deepcopy(history)
                key=-1
                draw_matrix(num_columns,s,e,mid,2)
                self.trigg.add(obj.class_id)
            elif obj.class_id==137:
                screen.fill(WHITE)
                font = pygame.font.Font(None, FONT_SIZE+50)  # Initialize font
                message = "Exiting the visualization. Comeback soon"
                text_surface = font.render(message, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
                screen.blit(text_surface, text_rect)
                pygame.display.flip()
                
                running=False
                #pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif obj.class_id<=15:
                if len(num_columns):
                    key=obj.class_id
                self.trigg.add(obj.class_id)
                if len(num_columns)==0:
                    print(obj.class_id)
                    num_columns=generate_sorted_random_list(obj.class_id)
                    history=copy.deepcopy(num_columns)
                    
                if len(num_columns):
                    draw_matrix(num_columns,s,e,mid,2)
                if key != -1:
                    binary_s()
            
    def remove_tuio_object(self, obj):
        if obj.class_id in self.trigg:
            self.trigg.remove(obj.class_id)
            #print(self.class_id_positions)
            #self.draw_boxes(obj)
            

# Create an instance of your custom TUIO listener
listener = CustomTuioListener()

# Create a TUIO client and add the listener
client = TuioClient(("0.0.0.0", 3333))
client.add_listener(listener)


# Start the TUIO client in a separate thread
t = Thread(target=client.start)
t.start()
# Main loop
running = True

previous_columns = []  # Variable to store the previous number of columns
c=0
s=0
e=len(num_columns)-1

mid=-1

draw_matrix(num_columns,s,e,mid,2)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_UP:
                # Increase number of columns when the UP arrow key is pressed
                #num_columns.append(num_columns[-1]+1)

            if event.key == pygame.K_DOWN:
                running=False

    
    pygame.display.flip()
    #clock.tick(60)

pygame.quit()
sys.exit()
