import datetime

import pygame as pg
from vehicle import Vehicle
import sys
from model import Evolution
import numpy as np

BORDER_COLOR = (255, 255, 255, 255)
BEST_REZ = 0
SAVE_LOADED = False


def load_save():

    sys.stdin = open("best.txt", 'r')
    t = []
    for i in range(2):
        t.append(list(map(float, input().split())))
    best = [np.matrix(t), float(input())]
    return best



def sorted_models_by_reward(models, rew):
    return [x[0] for x in sorted(zip(models, rew), key=lambda tup: tup[1])]


def tune_models(models, rew, ep):

    flag = 1
    for i in range(len(rew)-1):
        if rew[i] != rew[i+1] and rew[i] != 303:

            flag = 0
    if flag:
        print(":(")
        return [Evolution() for _ in range(16)]

    models = sorted_models_by_reward(models, rew)

    # choose 8 best
    new_models = [Evolution() for _ in range(16)]

    models = models[14:]
    k = 0
    print(max(rew))
    for m in models:
        for j in range(8):
            new_models[k + j].w2 = m.w2
            new_models[k + j].activation_level = m.activation_level
        k += 8

    models[0] = Evolution()

    for m in new_models:
        m.make_evolution()
    return new_models


if __name__ == '__main__':
    pg.init()
    texttype = pg.font.Font(None, 24)
    screen = pg.display.set_mode((1366, 768))  # Размер окна
    pg.display.set_caption("evoCar")
    clock = pg.time.Clock()

    model = [Evolution() for _ in range(16)]
    running = True

    tmp_click = 0
    dists = [[] for i in range(16)]
    output = [[0 for _ in range(4)] for _ in range(16)]
    MAP = pg.image.load('sprites/map.png').convert()
    reward = [0 for _ in range(16)]
    current_model = 0
    epoch = 0

    fps = 60
    destroyed = [False for _ in range(16)]
    while running:
        if current_model == 0:
            cars = [Vehicle(pg.image.load('sprites/car.png'), 102, 300, 0.01) for i in range(16)]
            all_sprites = pg.sprite.Group([_ for _ in cars])
            current_model = 16
            model = tune_models(model, reward, epoch)
            if not SAVE_LOADED:
                t = load_save()
                print(t)
                model[0].w2 = t[0]
                SAVE_LOADED = True
                model[0].activation_level = t[1]
            reward = [0 for _ in range(16)]
            destroyed = [False for _ in range(16)]
            epoch += 1
        # Map creating
        for i in pg.event.get():
            if i.type == pg.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if tmp_click == 0:
                        tmp_click = i.pos
                    else:
                        tmp2_click = i.pos
                        lines.append([tmp_click, tmp2_click])
                        tmp_click = i.pos

                if i.button == 3:
                    tmp_click = 0
                if i.button == 2:
                    lines = []
            # onExit
            if i.type == pg.QUIT:
                sys.stdout = open("save.txt", 'w')
                max_rew = 0
                k = 0
                for i in range(16):
                    if max_rew < cars[i].reward:
                        max_rew = cars[i].reward
                        k = i
                if BEST_REZ != 0:
                    if max_rew > BEST_REZ[1]:
                        for i in model[k].w2:
                            print(*i)
                        print(model[k].activation_level)
                    else:
                        for i in BEST_REZ[0]:
                            print(*i)
                        print(BEST_REZ[1])
                else:
                    for i in model[k].w2:
                        print(*i[0])
                    print(model[k].activation_level)
                running = False

        # Car control
        keys_pressed = pg.key.get_pressed()

        for i in range(16):
            cars[i].boost = -3
            if not destroyed[i]:
                cars[i].boost = -3
                if keys_pressed[pg.K_LEFT] or output[i][1]:
                    cars[i].rotation_l()
                if keys_pressed[pg.K_RIGHT] or output[i][0]:
                    cars[i].rotation_r()
                # if keys_pressed[pg.K_UP] or output[i][0]:
                #    cars[i].boost_up()

                dists[i] = cars[i].point_distanse(screen, MAP)

                if dists[i] != [0 for _ in range(5)]:
                    output[i] = model[i].get_output(dists[i])
                    if cars[i].destroy(dists[i]):
                        destroyed[i] = True
                        current_model -= 1
                        reward[i] = cars[i].reward

                # using dist like reward
                cars[i].reward += abs(cars[i].boost)
                # using checks like reward
                # if cars[i].is_cross_checkpoint():
                #    cars[i].start_time = datetime.datetime.now()
                #    cars[i].reward += 1
                #    reward[i] += 1

        if keys_pressed[pg.K_PAGEUP]:
            fps += 1
        if keys_pressed[pg.K_PAGEDOWN]:
            fps -= 1
        # print(output)
        # bg
        screen.fill((255, 255, 255))

        # map
        # for _ in lines:
        #    pg.draw.line(screen, (0, 0, 0), _[0], _[1], 5)
        # for _ in checks:
        #    pg.draw.line(screen, (255, 0, 0), _[0], _[1], 5)
        ## Lidar
        screen.blit(MAP, (0, 0))
        all_sprites.update(screen)
        all_sprites.draw(screen)

        # calculate ai

        # text

        text4 = texttype.render("Epoch: " + str(epoch),
                                1, (0, 0, 0))
        text5 = texttype.render("Model: " + str(current_model),
                                1, (0, 0, 0))
        text6 = texttype.render("G Speed: " + str(fps / 60)[:5],
                                1, (0, 0, 0))

        screen.blit(text4, (0, 0))
        screen.blit(text5, (0, 20))
        screen.blit(text6, (0, 40))

        pg.display.update()
        clock.tick(fps)

    pg.quit()
