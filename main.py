import pygame, sys, colorama, winsound,time,random

from colorama import Fore, Back, Style

colorama.init()

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Enter game language / Oyun dili girin")

BG = pygame.image.load("assets/Background.png")

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

class Langs():
    #TR
    tr_playbutton = "oyna"
    tr_optionsbutton = "yapımcı"
    tr_quitbutton = "çıkış"
    tr_tutorial1 = "nasıl oynanır?"
    tr_tutorial2 = "---------------"
    tr_tutorial3 = "yön tuşları ile"
    tr_tutorial4 = "SNEKKI'ye yön verin"
    tr_tutorial5 = "ESC ile çıkış yapabilirsiniz"

    #EN
    en_playbutton = "play"
    en_optionsbutton = "author"
    en_quitbutton = "quit"
    en_tutorial1 = "how to play?"
    en_tutorial2 = "-------------"
    en_tutorial3 = "use arrow keys to"
    en_tutorial4 = "rotate SNEKKI"
    en_tutorial5 = "you can exit with ESC"


screen_width = 1280
screen_height = 720

gridsize = 20
grid_witdh = screen_width / gridsize
grid_height = screen_height / gridsize



light_green = (84,84,84)
dark_green = (60,60,60)
random_food_color = (178,59,100) #[0,216,223],[223,208,0],[223,0,7],[0,223,119],[119,0,223]
food_color = (0,255,246)#(random.choice(random_food_color))
snekki_color = (216,216,216)

up = (0,-1)
down = (0,1)
right = (1,0)
left = (-1,0)

class SNEKKI:
    def __init__(self):
        self.positions = [((screen_width/2),(screen_height/2))]
        self.length = 1
        self.direction = random.choice([up,down,right,left])
        self.color = snekki_color
        self.score = 0
    def draw(self,surface):
        for p in self.positions:
            rect = pygame.Rect((p[0],p[1]),(gridsize,gridsize))
            pygame.draw.rect(surface,self.color,rect)
    def move(self):
        current = self.positions[0]
        x,y = self.direction
        new = ((current[0] + (x * gridsize)) , (current[1] + (y * gridsize)))

        if new[0] in range(0,screen_width) and new[1] in range(0,screen_height) and not new in self.positions[2:]:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()
        else:
            self.reset()
        
    def reset(self): #gameover
        self.length = 1
        self.positions = [((screen_width/2),(screen_height/2))]
        self.direction = random.choice([up,down,right,left])
        self.score = 0
        winsound.Beep(100, 500)

    def handle_keys(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.turn(up)
                        winsound.Beep(150, 100)
                    elif event.key == pygame.K_DOWN:
                        self.turn(down)
                        winsound.Beep(150, 100)
                    elif event.key == pygame.K_RIGHT:
                        self.turn(right)
                        winsound.Beep(150, 100)
                    elif event.key == pygame.K_LEFT:
                        self.turn(left)
                        winsound.Beep(150, 100)
                    elif event.key == pygame.K_ESCAPE:
                        winsound.Beep(100, 100)
                        winsound.Beep(150, 100)
                        winsound.Beep(250, 100)
                        pygame.quit()
                        sys.exit()
    def turn(self,direction):
        if (direction[0] * -1 , direction[1] * -1) == self.direction:
            return
        else:
            self.direction = direction

class FOOD:
    def __init__(self):
        self.position = (0,0)
        self.color = food_color
        self.random_position()
    def random_position(self):
        self.position = (random.randint(0,grid_witdh-1)*gridsize , random.randint(0,grid_height-1)*gridsize)
    def draw(self, surface):
        rect = pygame.Rect((self.position[0],self.position[1]), (gridsize,gridsize))
        pygame.draw.rect(surface,self.color,rect)

def drawGrid(surface):
    for y in range(0,int(grid_height)):
        for x in range(0,int(grid_witdh)):
            if (x + y) % 2 == 0:
                light = pygame.Rect((x * gridsize , y * gridsize) , (gridsize,gridsize))
                pygame.draw.rect(surface,light_green, light)
            else:
                dark = pygame.Rect((x * gridsize , y * gridsize) , (gridsize,gridsize))
                pygame.draw.rect(surface,dark_green, dark)

def game():
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/font.ttf",60)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    food = FOOD()
    snekki = SNEKKI()
    
    while True:
        clock.tick(5)
        snekki.handle_keys()
        snekki.move()
        drawGrid(surface)
        if  snekki.positions[0] == food.position:
            snekki.length += 1
            snekki.score += 1
            winsound.Beep(400, 100)
            winsound.Beep(500, 100)
            clock.tick(15)
            food.random_position()
            pygame.display.update()
            #if lang_select == "en":
            #    print(Back.GREEN + Fore.BLACK,en_score.format(snekki.score))
            #else:
            #    print(Back.GREEN + Fore.BLACK,tr_score.format(snekki.score))

        food.draw(surface)
        snekki.draw(surface)
        screen.blit(surface,(0,0))
        pygame.display.set_caption("SNEKKI v3.2")
        score_text = font.render("{0}".format(snekki.score),True,(216,216,216))
        screen.blit((score_text),(10,10))
        
        pygame.display.update()




############################################################################################################################
#                                                   ASIL KODLAR BURADA                                                     #
############################################################################################################################


#    _/_/    _/    _/  _/    _/  _/_/_/    
# _/    _/  _/    _/  _/    _/  _/    _/   
#_/    _/  _/    _/  _/    _/  _/    _/    
# _/_/      _/_/_/    _/_/_/  _/    _/     
#              _/                          
#         _/_/ 


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
   
LANG_ = get_font(45).render('Enter Language', True, '#F2FFAE')
LANG_RECT = LANG_.get_rect(center=(640, 260))
SCREEN.blit(LANG_,LANG_RECT)

class language():
    print(Fore.CYAN,"Enter game language",Fore.YELLOW,"/",Fore.CYAN,"Oyun dili girin\n",Fore.YELLOW,"[en/tr]\n") #dil soru
    lang_select = input("") #dil cevap

pygame.display.set_caption("SNEKKI")



def play():
    game()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(get_font(25).render("        v3.4", True, "#00fff6"),(640, 158))
        if language.lang_select == "tr":
            OPTIONS_TEXT = get_font(25).render("SHNdev tarafından geliştirildi", True, "#68fffa")
        if language.lang_select == "en":
            OPTIONS_TEXT = get_font(25).render("Developed by SHNdev", True, "#68fffa")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="<", font=get_font(75), base_color="#AEAFAB", hovering_color="#68fffa")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    winsound.Beep(222,100)
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        

        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(25).render("                    v3.4", True, "#00fff6")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 170))
        if language.lang_select == "tr":

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                                text_input=Langs.tr_playbutton, font=get_font(75), base_color="#AEAFAB", hovering_color="#68fffa")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                                text_input=Langs.tr_optionsbutton, font=get_font(75), base_color="#AEAFAB", hovering_color="#68fffa")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                                text_input=Langs.tr_quitbutton, font=get_font(75), base_color="#AEAFAB", hovering_color="#68fffa")
        if language.lang_select == "en":
            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                                text_input=Langs.en_playbutton, font=get_font(75), base_color="#AEAFAB", hovering_color="#68fffa")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                                text_input=Langs.en_optionsbutton, font=get_font(75), base_color="#AEAFAB", hovering_color="#68fffa")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                                text_input=Langs.en_quitbutton, font=get_font(75), base_color="#AEAFAB", hovering_color="#68fffa")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    winsound.Beep(333,100)
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    winsound.Beep(333,100)
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    winsound.Beep(111,100)
                    pygame.quit()
                    sys.exit()

        #tutorial
        if language.lang_select == "tr":
            SCREEN.blit(get_font(15).render((Langs.tr_tutorial1), True, "#AEAFAB"),(25, 580))
            SCREEN.blit(get_font(15).render((Langs.tr_tutorial2), True, "#00fff6"),(25, 595))
            SCREEN.blit(get_font(15).render((Langs.tr_tutorial3), True, "#AEAFAB"),(25, 610))
            SCREEN.blit(get_font(15).render((Langs.tr_tutorial4), True, "#AEAFAB"),(25, 640))
            SCREEN.blit(get_font(15).render((Langs.tr_tutorial5), True, "#AEAFAB"),(25, 670))
        else:
            SCREEN.blit(get_font(15).render((Langs.en_tutorial1), True, "#AEAFAB"),(25, 580))
            SCREEN.blit(get_font(15).render((Langs.en_tutorial2), True, "#00fff6"),(25, 595))
            SCREEN.blit(get_font(15).render((Langs.en_tutorial3), True, "#AEAFAB"),(25, 610))
            SCREEN.blit(get_font(15).render((Langs.en_tutorial4), True, "#AEAFAB"),(25, 640))
            SCREEN.blit(get_font(15).render((Langs.en_tutorial5), True, "#AEAFAB"),(25, 670))
        #tutorial

        pygame.display.update()

    
        
main_menu()

