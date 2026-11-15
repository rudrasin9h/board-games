import pygame
import sys
import logic

pygame.init()
clock = pygame.time.Clock()
running = True
width = 1800
height = 0.7*width
disp = pygame.display.set_mode((width,height))
offset = 100
board_length = width-offset

#Drawing vertical lines
x1,x2,x3,x4,y1,y2,y3,y4 = 0,0,0,0,0,0,0,0
side = width
cur_player = "p1"
draw_center = ((width-offset)/2,(width-offset)/2)
line_color = "#ffffff"
bg_color = "#2E4E45"

center_set = []
move_set = []
target = [999,999]


def draw_button(x,y,l,b,bg,text,w = 0):
    pygame.draw.rect(disp,bg,(x,y,l,b),width = w)

def draw_board(w: float, h: float,o: float):
    global cur_player,x1,x2,x3,x4,y1,y2,y3,y4,side
    length = (0.7*w)-o
    side = length/3
    lw = 12

    x1,x2,x3,x4 = (o/2),(o/2)+side,(o/2)+(side*2),(o/2)+(side*3)
    y1,y2,y3,y4 = (o/2),(o/2)+side,(o/2)+(side*2),(o/2)+(side*3)
    
    pygame.draw.line(disp,line_color,(x2,y1),(x2,y4),width=lw)
    pygame.draw.line(disp,line_color,(x3,y1),(x3,y4),width=lw)
    pygame.draw.line(disp,line_color,(x1,y2),(x4,y2),width=lw)
    pygame.draw.line(disp,line_color,(x1,y3),(x4,y3),width=lw)

def make_move():
    global cur_player,x1,x2,x3,x4,y1,y2,y3,y4,draw_center,target

    #Check for click
    click_pos = pygame.mouse.get_pos()

    if click_pos[0]<x2:
        target[1] = 0
        if click_pos[1]<y2:
            draw_center = ((x1+x2)/2,(y1+y2)/2)
            target[0] = 0
        elif click_pos[1]>y2 and click_pos[1]<y3:
            draw_center = ((x1+x2)/2,(y3+y2)/2)
            target[0] = 1
        else:
            draw_center = ((x1+x2)/2,(y3+y4)/2)
            target[0] = 2

    elif click_pos[0]>x2 and click_pos[0]<x3:
        target[1] = 1
        if click_pos[1]<y2:
            target[0] = 0
            draw_center = ((x3+x2)/2,(y1+y2)/2)
        elif click_pos[1]>y2 and click_pos[1]<y3:
            draw_center = ((x3+x2)/2,(y3+y2)/2)
            target[0] = 1
        else:
            draw_center = ((x3+x2)/2,(y3+y4)/2)
            target[0] = 2

    elif click_pos[0]>x3 and click_pos[0]<x4:
            target[1] = 2
            if click_pos[1]<y2:
                draw_center = ((x3+x4)/2,(y1+y2)/2)
                target[0] = 0
            elif click_pos[1]>y2 and click_pos[1]<y3:
                target[0] = 1
                draw_center = ((x3+x4)/2,(y3+y2)/2)
            else:
                draw_center = ((x3+x4)/2,(y3+y4)/2)
                target[0] = 2
    
    else:
        print("Overclick!")

def drawO(c):
    global side,cur_player
    rad = (side-(0.177*side))/2
    pygame.draw.circle(disp,line_color,c,rad,width = 14)

def drawX(c):
    global side,cur_player
    eff_len = (side - (0.177*side))/2
    #vertices of x
    v1x = c[0]-eff_len
    v2x = c[0]+eff_len
    v2y = c[1]-eff_len
    v1y = c[1]+eff_len

    pygame.draw.line(disp,line_color,(v1x,v1y),(v2x,v2y),width=14)
    pygame.draw.line(disp,line_color,(v1x,v2y),(v2x,v1y),width=14)

def validate_move(player,center):
    if center not in center_set:
        center_set.append(center)
        move_set.append(player)
    # print(center_set)
    # print(move_set)

def update_player():
    global cur_player
    if cur_player == "p1":
            cur_player = "p2"
    else:
        cur_player = "p1"

def draw_move(l1:list,l2:list):

    for i in range(len(l2)):
        if l2[i] == "p1":
            drawO(l1[i])
        else:
            drawX(l1[i])

def reset_board():
    global cur_player
    logic.board = logic.ini_board.copy()
    move_set.clear()
    center_set.clear()
    cur_player = "p1"
    
def draw_win():
    #Get the addresses of winning row/col/diag from array
    pass
    #choose x and y coords of start and end points 

    #draw the line

def run_game():
    global running,cur_player
    while running:

        disp.fill(bg_color)
        draw_board(width,height,offset)
        draw_button((0.7*width)+100,offset,350,200,"#666666","reset")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    make_move()

                    if logic.update_board(target[0], target[1], cur_player):
                        validate_move(cur_player, draw_center)
                        winner = logic.check_win(logic.board)

                        if winner[0]:
                            print(f"{winner[1]} wins!")
                            reset_board()
                        else:
                            update_player()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_board()

        draw_move(center_set,move_set)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
