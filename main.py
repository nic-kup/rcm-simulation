"""We create an interactive simulation of a random connection model"""
from sys import exit
import os
import datetime

import numpy as np
import pygame

import slider
import rcm

grey = pygame.Color(125, 125, 125)

# Note to self: I want to write everything in terms of relative coordinates
#        for some hypothetical 16x9 window.

if __name__ == "__main__":

    if not os.path.exists('pics'):
        os.mkdir('pics')

    pygame.display.init()
    disp_size = (1280, 720)

    rect = np.array([0, 0, disp_size[0], disp_size[1]])
    screen = pygame.display.set_mode(disp_size)
    pygame.display.set_caption("Soft Random Geometric Graph")
    RUNNING = True

    pygame.font.init()
    helvetica_path = pygame.font.match_font("helvetica")
    font = pygame.font.Font(helvetica_path, 14)

    my_rcm = rcm.RCM(250, 50, 60)
    my_rcm.screen = screen

    lambda_slider = slider.VerticalSlider((0, my_rcm.lambda_max), 300, (50, 50))
    lambda_slider.screen = screen
    p_slider = slider.VerticalSlider((0, 1), 300, (100, 50))
    p_slider.screen = screen

    my_rcm.lambda_cur = lambda_slider.cur_value
    my_rcm.p_cur = p_slider.cur_value

    while RUNNING:
        screen.fill((255, 255, 255))

        if pygame.mouse.get_pressed()[0] != 0:
            pos = pygame.mouse.get_pos()
            my_rcm.update_lambda(lambda_slider.full_update(pos))
            my_rcm.update_p(p_slider.full_update(pos))

        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_p]:
            my_rcm.perturb()

        lambda_text = font.render(
            str(int(lambda_slider.cur_value * 10) / 10), True, grey
        )
        p_text = font.render(str(int(p_slider.cur_value * 100) / 100), True, grey)
        screen.blit(lambda_text, (40, 400))
        screen.blit(p_text, (90, 400))

        lambda_slider.draw()
        p_slider.draw()
        my_rcm.draw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False
                if event.key == pygame.K_s:
                    date_str = str(datetime.datetime.today())[:16]
                    para_str = (
                        str(my_rcm.get_lambda_simp) + "-" + str(my_rcm.get_p_simp)
                    )
                    pygame.image.save(
                        screen, "pics/test" + date_str + "-" + para_str + ".png"
                    )
                    screen.fill((255, 255, 255))
                if event.key == pygame.K_r:
                    my_rcm.reshuffle_edges()
                if event.key == pygame.K_t:
                    my_rcm.reshuffle_all()

        pygame.display.update()
        pygame.event.clear()

    pygame.quit()
    exit()
