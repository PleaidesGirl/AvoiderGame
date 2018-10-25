import sys, pygame, math, time

# Starter code for an avoider game. Written by David Johnson for COMP1010 University of Utah.

# Finished game authors:
# Celine Cavanaugh
# Nicole Martino
#
## 1. There should be at least 2 levels. When the end color is reached of level 1, a new background should be loaded,
# and the player needs to click on the start color again to begin that level.
# 2. Each level needs at least 1 animated sprite. The sprite can make the player lose, or the sprite can somehow help the
# player. Make the sprite in Piskel or some other program, but the files need to be in a folder and named like Piskel
# does to be loaded by my code.
## 3. A timer is needed to show how fast the player completes each level. Display the time on the screen building on the
# example from the starter code.
# 4. You need to be creative and add something to make the game interesting. A perfectly done game with two levels and two
#  sprites that bounce back and forth will be considered a B grade game. Your creative elements are needed to move into
#  the A and B+ range. Think about animating the whole map (or animating a sprite that looks like part of the map on top
#  of the map), using image rotation, adding different kinds of sprites and triggers and traps. A team from a pair of
# people needs even more. Have fun with it!
# 5. Write a short description of the creative elements of the game so that we are sure to notice them. A paragraph or short
#  bullet list is fine for this. Add a pdf or txt file in the folder with the name "CreativeParts" .txt or .pdf. Make
#  sure it gets zipped up with the rest of the materials.


# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_##. It returns a list of the images.
def load_piskell_sprite(sprite_folder_name, number_of_frames):
    frames = []
    # Figure out how many digits are in the frame number
    padding = math.ceil(math.log(number_of_frames,10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding,'0') +".png"
        frames.append(pygame.image.load(folder_and_file_name).convert_alpha())

    return frames

# This function bounces a rectangle between the start and end pos. The bounce happens over num_frame frames.
# So the bigger the num_frame value is, the slower it goes (the bounce takes more frames).
# The rect is modified to be at the new position - a rect is not returned.
# Start and end pos are tuples of (x,y) coordinates on the window. You will likely need to experiment to find
# good coordinates.
def bounce_rect_between_two_positions( rect, start_pos, end_pos, num_frame, frame_count ):
    if frame_count%num_frame < num_frame/2:
        ### If the remainder of frames per second is less than num_frame/2
        new_pos_x = start_pos[0] + (end_pos[0] - start_pos[0]) * (frame_count%(num_frame/2))/(num_frame/2)
        ### new_pso_x equals start position at index 0 plus end_pos at index 0 minus start_position at index 0. So, if the start position is (3,4) the
        new_pos_y = start_pos[1] + (end_pos[1] - start_pos[1]) * (frame_count%(num_frame/2))/(num_frame/2)
    else:
       new_pos_x = end_pos[0] + (start_pos[0] - end_pos[0]) * (frame_count%(num_frame/2))/(num_frame/2)
       new_pos_y = end_pos[1] + (start_pos[1] - end_pos[1]) * (frame_count%(num_frame/2))/(num_frame/2)

    rect.center = (new_pos_x, new_pos_y)


#### This basically sets the location of the rectangle. It is a defined function where bounce_rect_between_two_positions
#### is the function and the stuff in the parenthesis are the parameters. rect is just the rectangle, start_pos and end_
#### pos set the position, num_frame is the number of frames and frame count counts the number of num frames per second

def main():

    # Initialize pygame
    pygame.init()

    map = pygame.image.load("Map.png")
    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    map_rect = map.get_rect()

    # set the background color to something more pleasing than black
    background_color = 0, 0, 0

    # create the window
    screen = pygame.display.set_mode(map_size)

    map = map.convert()

    # Load the sprite frames from the folder
    Rex = load_piskell_sprite("Rex", 2)
    Rex_rect = Rex[0].get_rect()


    Long_Neck = load_piskell_sprite("LongNeckWalk",2)
    Long_Neck_rect = Long_Neck[0].get_rect()

    # The frame tells which sprite frame to draw
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font - there is some problem on my Mac that makes this pause for 10s of seconds sometimes.
    # I will see if I can find a fix.
    myfont = pygame.font.SysFont('monospace', 24)

    # The started variable records if the start color has been clicked and the level started
    started = False

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # Hide the arrow cursor and replace it with a sprite. Don't make this big or the checking for collisions
    # gets more complicated than just looking at the color under the cursor tip.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene
    my_clock = 120
    start_ticks = pygame.time.get_ticks()

    while is_alive:
        string_of_clock = str(my_clock)
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if(seconds >= 1):
            my_clock -= 1
            start_ticks = pygame.time.get_ticks()
            seconds = 0
        print(seconds)
        # Draw the background
        screen.blit(map, map_rect)

        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
        # Add a mouse down event to look for clicking on the start color

        # Draw a guard
        bounce_rect_between_two_positions(Rex_rect, (440,300), (440, 150), 200, frame_count)
        screen.blit(Rex[frame_count%len(Rex)], Rex_rect)

        # Now check for the color under the cursor. Don't draw the cursor sprite yet or the
        # color will be the cursor sprite color, not the scene.
        pos = pygame.mouse.get_pos()
        color_at_cursor = screen.get_at(pos)

        # In the starter code I just print the color. Don't print it in your game as it will slow
        # things down. But you can use this to see the colors you need to be looking for to see if the cursor
        # is in a safe spot.
        # Note that the color has 4 values - the 4th is alpha, or transparency. If you want to compare colors
        # make sure that you compare all the values. An example would be
        #      color_at_cursor == (255, 0, 0, 255)
        # to see if the cursor is over a pure red area.
        #sprint(color_at_cursor)

        # Once you have the color at the cursor, check to see if you have gone off the path or if you have
        # touched the end color. You need to write code for this. The logic is that you need to see if the
        # level has been started, and then if it is touching something bad.


        # Now move and draw the cursor sprite. Divide the frame_count by 10 to slow the cycle down.
        Long_Neck_rect.center = pygame.mouse.get_pos()
        screen.blit(Long_Neck[(frame_count//10)%len(Long_Neck)], Long_Neck_rect)

        # Write some text to the screen. You can do something like this to show the time going by.
        label = myfont.render(string_of_clock, True, (255,255,0))
        screen.blit(label, (20,20))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    pygame.quit()
    sys.exit()


# Start the program
main()
# Timer

# import time
# my_clock = pygame.time.Clock()
# label = myfont.render(my_clock, True, (255, 255, 0))
# screen.blit(label, (100, 20))
# set_timer(is_alive, 100)s
# #while value in my_clock>0:
#
#
# start_time = time.time()
# clock = time.clock_gettime()
# print(clock)

'''
def seconds_counting_up(seconds):
    start_timer = time.time()
    time.clock()
    if window.mouse_click == True:
         start_timer += 1
    else:
         start_timer+=1

my_time = 0
starting_time = seconds_counting_up(my_time)

start_timer = time.time() ## Sets the timer to 0
game_time = 0
label = myfont.render(game_time, True, (255,255,0))
screen.blit(label, (20,20))
for count in game_time:
    if mouse_click==True:
        start_timer += 1
    start_timer += 1
'''
# ## Traps

def is_collided_with(self, Long_Neck):
    return self.rect.colliderect(Long_Neck.rect)
#
# ## Rotate Level
#
# while is_alive ==True:
#     pygame.transform.rotate(window,90)
