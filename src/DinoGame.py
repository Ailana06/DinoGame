import pygame #импортирование библиотеки pygame
import random #импортирование библиотеки random

pygame.init() #инициализация

display_width = 800 #дисплей, размеры игры
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Run Motya! Run!') #название игры

icon = pygame.image.load('icon.png') #иконка
pygame.display.set_icon(icon) #функция которая как бы запускаяет

cactus_img = [pygame.image.load('Cactus0.bmp'), pygame.image.load('Cactus1.bmp'), pygame.image.load('Cactus2.bmp')] #массив в котором хранятся изображения кактусов
cactus_options = [69, 449, 37, 410, 40, 420]

stone_img = [pygame.image.load('Stone0.bmp'), pygame.image.load('Stone1.bmp')]
cloud_img = [pygame.image.load('Cloud0.bmp'), pygame.image.load('Cloud1.bmp')]

dino_img = [pygame.image.load('Dino0.bmp'), pygame.image.load('Dino1.bmp'), pygame.image.load('Dino2.bmp'),
            pygame.image.load('Dino3.bmp'), pygame.image.load('Dino4.bmp')]
img_counter = 0


class Object: #класс кактусов
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y)) #закидываем в дисплей изображение
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


usr_width = 60 #ширина персонажа
usr_height = 100 #высота персонажа
usr_x = display_width // 3 #персонаж занимает 1/3 экрана
usr_y = display_height - usr_height - 100

cactus_width = 20 #ширина кактуса
cactus_height = 70 #высота кактуса
cactus_x = display_width - 50
cactus_y = display_height - cactus_height - 100

clock = pygame.time.Clock() #как часто обновляется кадр игры

make_jump = False
jump_counter = 30 #щётчик

scores = 0
max_scores = 0
max_above = 0


def run_game(): #функция запуска игры
    global make_jump
    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)#добавление дополнительных функций в основную функцию
    land = pygame.image.load(r'Land.bmp') #загружаем землю

    stone, cloud = open_random_objects()

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed() #прочитать все клавиши которые нажал персонаж
        if keys[pygame.K_SPACE]: #если игрок нажал на пробел
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        count_scores(cactus_arr)

        display.blit(land, (0, 0)) #вывод картинки
        print_text('Scores: ' + str(scores), 600, 10)

        draw_array(cactus_arr)
        move_objects(stone, cloud)

        draw_dino()

        if check_collision(cactus_arr):
            game = False

        pygame.display.update() #обновление дисплея
        clock.tick(70)
    return game_over()


def jump(): #функция прыжка
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30: #логика прыжка
        usr_y -= jump_counter / 2.5 #реализация прыжка
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array): #функция которая за нас создает массив кактусов
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 280
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 400)

    return radius


def draw_array(array): #отвечает за прорисовку массива
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]

            cactus.return_self(radius, height, width, img)


def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
    cloud = Object(display_width, 80, 70, img_of_cloud, 2)

    return stone, cloud


def move_objects(stone, cloud): #открывает когда объекты зашли за границы экрана
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10, 200), stone.width, img_of_cloud)


def draw_dino():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    display.blit(dino_img[img_counter // 5], (usr_x, usr_y))
    img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Paused. Press enter to continue', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)


def check_collision(barriers): # не каснулся ли персонаж кактуса
    for barrier in barriers:
        if barrier.y == 449: #маленький кактус
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 0 <= barrier.x + barrier.width:
                    return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 0 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 0 <= barrier.x + barrier.width:
                        return True
            else:
                if usr_y + usr_height - 0 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.width:
                        return True
        else:
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 0 <= barrier.x + barrier.width:
                    return True
            elif jump_counter == 0:
                if usr_y + usr_height - 0 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 0 <= barrier.x + barrier.width:
                        return True
            elif jump_counter >= -0: #!!!!!!!!!!!!
                if usr_y + usr_height - 0 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 0 <= barrier.x + barrier.width:
                        return True
                else:
                    if usr_y + usr_height - 0 >= barrier.y:
                        if barrier.x <= usr_x + 0 <= barrier.x + barrier.width:
                            return True
    return False


def count_scores(barriers):
    global scores, max_above
    above_cactus = 0

    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_height - 5 <= barrier.y:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_cactus += 1
                elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                    above_cactus += 1

        max_above = max(max_above, above_cactus)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0


def game_over():
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over. Press Enter to play again, Esc to exit', 40, 300)
        print_text('Max scores: ' + str(max_scores), 300, 350)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


while run_game():
    scores = 0
    make_jump = False
    jump_counter = 30
    usr_y = display_height - usr_height - 100
pygame.quit()
quit()
