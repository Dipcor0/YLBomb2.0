import pygame
import os
import sys
import random


class Bomb(pygame.sprite.Sprite):
    def __init__(self, *args, screen=None):
        super().__init__(*args)
        self.group = args[0]
        self.screen = screen
        self.flag = False

        image_bomb = load_image('bomb2.png')
        self.bomb = pygame.transform.scale(image_bomb, (image_bomb.get_width() // 2, image_bomb.get_height() // 2))
        image_boom = load_image('boom.png')
        self.boom = pygame.transform.scale(image_boom, (image_boom.get_width() // 2, image_boom.get_height() // 2))

        self.image = self.bomb
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        while True:
            check = True
            self.rect.x = random.randint(0, self.screen.get_width() - self.image.get_width())
            self.rect.y = random.randint(0, self.screen.get_height() - self.image.get_height())
            if self.group:
                for spr in self.group:
                    if id(spr) != id(self) and pygame.sprite.collide_mask(self, spr):
                        check = False
                        break
            if check:
                break

    def update(self, *args) -> None:
        if args and not self.flag:
            pos = args[0].pos
            if (self.rect.x <= pos[0] <= self.rect.x + self.rect.width and
                    self.rect.y <= pos[1] <= self.rect.y + self.rect.height):
                self.image = self.boom
                new_rect = self.image.get_rect()
                self.rect.x += (self.rect.width - new_rect.width) // 2
                self.rect.y += (self.rect.height - new_rect.height) // 2
                self.flag = True


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


def main():
    pygame.init()
    size = 500, 500
    running = True

    screen = pygame.display.set_mode(size)

    group_bombs = pygame.sprite.Group()
    for _ in range(20):
        Bomb(group_bombs, screen=screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                group_bombs.update(event)
        screen.fill('Black')

        group_bombs.update()
        group_bombs.draw(screen)

        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
