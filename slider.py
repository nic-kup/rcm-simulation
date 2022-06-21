""" Create slider object."""
import pygame
import numpy as np

red = pygame.Color(240, 20, 20)
mid_red = pygame.Color(140, 25, 25)
grey = pygame.Color(40, 30, 30)


class HorizontalSlider:
    """Generates a slider with logic and show function"""

    def __init__(self, bounds, length, location):
        """Initialize our slider"""
        self.screen = None
        self.cur_value = (bounds[1] - bounds[0]) / 2
        self.min_a = bounds[0]
        self.max_a = bounds[1]
        self.length = length
        self.loc_x = location[0]
        self.loc_y = location[1]

    def update_value(self, new_val):
        """Updates value of cur_value safely"""
        self.cur_value = np.clip(new_val, self.min_a, self.max_a)

    @property
    def rel_x(self):
        return self.length * (self.cur_value - self.min_a) / (self.max_a - self.min_a)

    def draw(self):
        pygame.draw.rect(
            self.screen, grey, pygame.Rect(self.loc_x, self.loc_y - 5, self.length, 10)
        )
        pygame.draw.rect(
            self.screen,
            mid_red,
            pygame.Rect(self.loc_x, self.loc_y - 5, self.rel_x, 10),
        )
        pygame.draw.rect(
            self.screen,
            red,
            pygame.Rect(self.loc_x + self.rel_x - 5, self.loc_y - 20, 10, 40),
        )


class VerticalSlider:
    """Generates a slider with logic and show function"""

    def __init__(self, bounds, length, location):
        """Initialize our slider"""
        self.screen = None
        self.cur_value = (bounds[1] - bounds[0]) / 2
        self.min_a = bounds[0]
        self.max_a = bounds[1]
        self.length = length
        self.loc_x = location[0]
        self.loc_y = location[1]

    @property
    def range(self):
        """Returns range of values for slider"""
        return self.max_a - self.min_a

    def update_value(self, new_val):
        """Safely updates current value for slider"""
        self.cur_value = np.clip(new_val, self.min_a, self.max_a)

    def update_value_loc(self, height):
        # Create value between 0 and 1
        temp_val = 1 - (height - self.loc_y) / self.length
        self.cur_value = np.clip(
            self.range * temp_val + self.min_a, self.min_a, self.max_a
        )

    @property
    def rel_y(self):
        return self.length * (self.cur_value - self.min_a) / (self.max_a - self.min_a)

    def draw(self):
        """Draws slider"""
        pygame.draw.rect(
            self.screen, grey, pygame.Rect(self.loc_x - 5, self.loc_y, 10, self.length)
        )
        pygame.draw.rect(
            self.screen,
            mid_red,
            pygame.Rect(
                self.loc_x - 5, self.loc_y + self.length - self.rel_y, 10, self.rel_y
            ),
        )
        pygame.draw.rect(
            self.screen,
            red,
            pygame.Rect(
                self.loc_x - 20, self.loc_y + self.length - self.rel_y - 5, 40, 10
            ),
        )
