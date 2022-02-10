# pygame 라이브러리 포함
import pygame

clock = pygame.time.Clock()
fps = 100

# pygame 라이브러리 초기화
pygame.init()

WIDTH = 800
HEIGHT = 600

# 그림이 그려지는 화면 설정
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Escape The Castle')

font = font = pygame.font.Font('DungGeunMo.ttf', 70)

black = (0, 0, 0)
white = (255,255,255)

tile_size = 50
life = 3
get_key = 0
game_over = 0
stage = 0
max_stages = 2

# 화면에 글자 출력
def write_text(text, font, color, x, y):
    text_img = font.render(text, True, color)
    screen.blit(text_img,(x,y))

# empty object
def empty_obj():
    slime_group.empty()
    block_group.empty()
    key_group.empty()
    door_group.empty()
    fly_group.empty()
    heart_group.empty()

# reset stage
def reset_stage(stage,life):
    if stage == 1:
        player.reset(0, 500, life)
        empty_obj()
        world = World(world_data1)

    if stage == 2:
        player.reset(0, 250, life)
        empty_obj()
        world = World(world_data2)

    return world

class Life_Point(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        empty_img = pygame.image.load('img/heartEmpty.png')
        self.empty_image = pygame.transform.scale(empty_img, (20, 20))
        self.rect = self.empty_image.get_rect()

        full_img = pygame.image.load('img/heartFull.png')
        self.full_image = pygame.transform.scale(full_img, (20, 20))

    def update(self, game_over, life):
        if game_over == 0:
            if life == 3:
                screen.blit(self.full_image, (650, 10))
                screen.blit(self.full_image, (700, 10))
                screen.blit(self.full_image, (750, 10))

            if life == 2:
                screen.blit(self.empty_image, (650, 10))
                screen.blit(self.full_image, (700, 10))
                screen.blit(self.full_image, (750, 10))

            if life == 1:
                screen.blit(self.empty_image, (650, 10))
                screen.blit(self.empty_image, (700, 10))
                screen.blit(self.full_image, (750, 10))

            if life == 0:
                game_over = -1

        elif game_over == -1:
            screen.blit(self.empty_image, (650, 10))
            screen.blit(self.empty_image, (700, 10))
            screen.blit(self.empty_image, (750, 10))

class Player():
    def __init__(self,x,y):
        self.reset(x,y,life)

    def reset(self,x,y,life):
        img = pygame.image.load('img/player.png')
        self.image = pygame.transform.scale(img, (35, 35))
        self.return_image = pygame.transform.scale(img, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.move_direction = 1  # 이동 방향
        self.move_counter = 0  # 이동 거리

        attacked_img = pygame.image.load('img/attacked.png')
        self.attacked_image = pygame.transform.scale(attacked_img, (35, 35))

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.gv = 0
        self.jump = False

        self.life = life
        self.get_key = get_key

    def update(self, game_over, life, get_key):
        dx = 0
        dy = 0

        if game_over == 0:

            # 방향키 입력받기
            key = pygame.key.get_pressed()
            if (key[pygame.K_SPACE] or key[pygame.K_UP]) and self.jump == False:
                self.gv = -4
                self.jump = True
            if (key[pygame.K_SPACE] or key[pygame.K_UP]):
                self.jump = False
            if key[pygame.K_RIGHT]:
                dx += 2
            if key[pygame.K_DOWN]:
                dy += 2
            if key[pygame.K_LEFT]:
                dx -= 2

            #중력 추가
            self.gv += 2
            if self.gv > 10:
                self.gv = 10
            dy += self.gv

            # castle tile과의 충돌 감지
            for tile in world.tile_list:
                # x방향으로의 충돌 감지
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # y방향으로의 충돌 감지
                # 실제로 충돌 발생하기 전에 충돌 감지. 충돌이 발생한 후에 감지하면 너무 늦음
                if tile[1].colliderect(self.rect.x, self.rect.y+dy,self.width,self.height):
                    # 점프하다 충돌한 경우(머리를)
                    if self.gv < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.gv = 0
                    # 지상에 떨어지는 경우
                    elif self.gv >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.gv = 0

            # 적과의 충돌 감지-slime
            if pygame.sprite.spritecollideany(self, slime_group):

                # 생명 하나 감소
                self.life += -1
                if self.life == 0:
                    game_over = -1

                # 충돌하면 튕겨져 나오기
                self.move_direction = -1
                dx *= (20 * self.move_direction)
                dy *= (4 * self.move_direction)
                self.gv = 0

                pygame.time.wait(200)

            # 적과의 충돌 감지-fly
            if pygame.sprite.spritecollideany(self, fly_group):

                # 생명 하나 감소
                self.life += -1
                if self.life == 0:
                    game_over = -1

                # 충돌하면 튕겨져 나오기
                self.move_direction = -1
                dx *= (20 * self.move_direction)
                dy *= (4 * self.move_direction)
                self.gv = 0

                pygame.time.wait(200)

            # 적과의 충돌 감지-block
            if pygame.sprite.spritecollideany(self, block_group):

                # 생명 하나 감소
                self.life += -1
                if self.life == 0:
                    game_over = -1

                # 충돌하면 튕겨져 나오기
                self.move_direction = -1
                dx *= (4 * self.move_direction)
                dy *= (4 * self.move_direction)
                self.gv = 0

                pygame.time.wait(400)

            # key와의 충돌 감지
            if pygame.sprite.spritecollide(self, key_group, True):
                self.get_key = 1

            # door와 충돌 감지
            if pygame.sprite.spritecollideany(self, door_group):
                if self.get_key == 1:
                    game_over = 1
                    self.get_key = 0

            # heart와의 충돌 감지
            if pygame.sprite.spritecollide(self, heart_group, True):
                self.life += 1

            # player 위치 update
            self.rect.x += dx
            self.rect.y += dy

            # 화면 좌우 밖으로 나가지 않게 하기
            if self.rect.right > WIDTH or self.rect.x < 0:
                self.rect.x -= dx
            if self.rect.bottom > HEIGHT or self.rect.y < 0:
                self.rect.y -= dy

        elif game_over == -1:
            self.image = self.attacked_image
            write_text("Game Over!",font,white,(WIDTH // 2) - 160, (HEIGHT // 2) -50)

        #화면에 그리기
        screen.blit(self.image, self.rect)

        return game_over, self.life

class World():
    def __init__(self,data):
        self.tile_list = []

        #이미지 로드
        castle_img = pygame.image.load('img/castle.png')
        castle2_img = pygame.image.load('img/castleHalf.png')

        # gird 상에 놓기
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1: # castle
                    img = pygame.transform.scale(castle_img, (tile_size, tile_size))
                    img_rect = img.get_rect()  # 이미지 크기 가져오고 직사각형 생성
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                elif tile == 2:  # half castle
                    img = pygame.transform.scale(castle2_img, (tile_size, tile_size))
                    img_rect = img.get_rect()  # 이미지 크기 가져오고 직사각형 생성
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                elif tile == 3: # left slime
                    slime = Enemy(col_count * tile_size, row_count * tile_size + 25)
                    slime_group.add(slime)

                elif tile == 4: # block
                    block = Block(col_count * tile_size, row_count * tile_size)
                    block_group.add(block)

                elif tile == 5: # key
                    key = Key(col_count * tile_size + 25, row_count * tile_size +25)
                    key_group.add(key)

                elif tile == 6: # door
                    door = Door(col_count * tile_size, row_count * tile_size)
                    door_group.add(door)

                elif tile == 7: # fly Enemy
                    fly = FlyEnemy(col_count * tile_size, row_count * tile_size + 25)
                    fly_group.add(fly)

                elif tile == 8: # life_heart
                    heart = Heart(col_count * tile_size + 25, row_count * tile_size +25)
                    heart_group.add(heart)

                col_count += 1
            row_count += 1

    # 화면에 그리기
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1]) # 이미지, 직사각형

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('img/slimeEnemie.png')
        self.rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y

        self.move_direction = 1 # 이동 방향
        self.move_counter = 0 # 이동 거리

    def update(self):
        self.rect.x += self.move_direction # 오른쪽으로 이동
        self.move_counter += 1

        if self.move_counter > 45:
            self.move_direction *= -1
            self.move_counter *= -0.3

class FlyEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('img/flyEnemie.png')
        self.rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y

        self.move_direction = 1 # 이동 방향
        self.move_counter = 0 # 이동 거리

    def update(self):
        self.rect.x += self.move_direction # 오른쪽으로 이동
        self.move_counter += 1

        if self.move_counter > 90:
            self.move_direction *= -1
            self.move_counter *= -0.3

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        block_img = pygame.image.load('img/blockEnemie.png')
        self.image = pygame.transform.scale(block_img, (tile_size, tile_size))
        self.rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y

class Key(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        key_img = pygame.image.load('img/key.png')
        self.image = pygame.transform.scale(key_img, (40, 35))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (x,y)

class Door(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        lock_img = pygame.image.load('img/doorLock.png')
        self.image = pygame.transform.scale(lock_img, (tile_size, tile_size))
        self.rect = self.image.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y

class Heart(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        heart_img = pygame.image.load('img/heartFull.png')
        self.image = pygame.transform.scale(heart_img, (40, 35))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (x,y)

world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 2, 2, 2, 0, 0, 1, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0],
    [0, 4, 1, 0, 0, 3, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0],
    [0, 1, 0, 0, 2, 2, 2, 0, 0, 3, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 6],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

world_data1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 2, 2, 0, 0, 1, 1],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
    [0, 0, 0, 2, 2, 2, 0, 0, 0, 1, 0, 3, 0, 0, 2, 1],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 4, 0, 0, 0, 2, 2, 0, 6],
    [0, 2, 2, 2, 2, 4, 2, 0, 2, 4, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 3, 0, 0],
    [2, 2, 4, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

world_data2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 2, 2, 2, 0, 0, 1, 0, 0, 1, 2, 0, 2, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2, 4, 0, 0],
    [0, 1, 0, 0, 4, 2, 2, 0, 0, 3, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 8, 0, 2, 2, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 2, 1, 0],
    [0, 7, 0, 0, 0, 0, 0, 2, 5, 4, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

life_point = Life_Point()
player = Player(0,0)
slime_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
fly_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()

world = World(world_data)

# 게임 루프
running = True
while running:

    # fps 설정
    clock.tick(fps)

    #화면에 순서대로 표시
    screen.fill(black)
    world.draw()
    if game_over == 0:
        fly_group.update()
        slime_group.update()

    fly_group.draw(screen)
    slime_group.draw(screen)
    block_group.draw(screen)
    key_group.draw(screen)
    door_group.draw(screen)
    heart_group.draw(screen)

    # stage 통과했을 때
    if game_over == 1:
        #다음 stage로 넘어가기
        stage += 1
        if stage <= max_stages:
            world_data = []
            life = player.life
            world = reset_stage(stage,life)
            game_over = 0

        else:
            write_text("Game Clear!", font, white, (WIDTH // 2) - 180, (HEIGHT // 2) - 50)

    game_over, player.life = player.update(game_over,life,get_key)
    life_point.update(game_over,player.life)

    for event in pygame.event.get():
        # 창 X 누르면 종료
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
