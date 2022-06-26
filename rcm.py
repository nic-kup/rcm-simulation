""" This file simulates an RCM for pygame """
from itertools import product
import numpy as np
import numpy.random as npr
import pygame

grey = pygame.Color(80, 90, 90)
blue = pygame.Color(40, 40, 200)


class RCM:
    """Generates an RCM with draw functionallity"""

    def __init__(self, loc_x=0, loc_y=0, scale=60):
        """Initializes RCM"""
        self.screen = None
        self.scale = scale
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.WIDTH = 15
        self.HEIGHT = 10
        self.lambda_max = 5
        self.lambda_cur = 1
        self.p_cur = 0.5

        self.N = npr.poisson(self.WIDTH * self.HEIGHT * self.lambda_max)
        self.all_particles = npr.uniform(size=(self.N, 3))

        self.all_particles[:, 0] *= self.WIDTH
        self.all_particles[:, 1] *= self.HEIGHT
        self.all_particles[:, 2] *= self.lambda_max
        self.all_particles = np.concatenate(
            (self.all_particles, np.array(range(self.N)).reshape((self.N, 1))), axis=-1
        )

        self.hash_mat = [
            [[] for j in range(int(self.HEIGHT) + 1)]
            for i in range(int(self.WIDTH) + 1)
        ]

        for x in self.all_particles:
            for (i, j) in product([-1, 0, 1], [-1, 0, 1]):
                self.hash_mat[int(x[0]) + i][int(x[1]) + j].append(x)

        self.connection_matrix = npr.random(size=(self.N, self.N))

        print(self.N)

    @property
    def get_lambda_simp(self):
        return np.round(self.lambda_cur, 1)

    @property
    def get_p_simp(self):
        return np.round(self.p_cur, 2)

    def update_lambda(self, new_lambda):
        """Updates lambda based on given value"""
        if new_lambda is not None:
            self.lambda_cur = new_lambda

    def update_p(self, new_p):
        """Updates p based on given value"""
        if new_p is not None:
            self.p_cur = new_p

    def reshuffle_edges(self):
        """Resamples all edges"""
        self.connection_matrix = npr.random(size=(self.N, self.N))

    def reshuffle_all(self):
        """Resample all points and edges"""
        self.N = npr.poisson(self.WIDTH * self.HEIGHT * self.lambda_max)
        self.all_particles = npr.uniform(size=(self.N, 3))

        self.all_particles[:, 0] *= self.WIDTH
        self.all_particles[:, 1] *= self.HEIGHT
        self.all_particles[:, 2] *= self.lambda_max
        self.all_particles = np.concatenate(
            (self.all_particles, np.array(range(self.N)).reshape((self.N, 1))), axis=-1
        )

        self.hash_mat = [
            [[] for j in range(int(self.HEIGHT) + 1)]
            for i in range(int(self.WIDTH) + 1)
        ]

        for x in self.all_particles:
            for (i, j) in product([-1, 0, 1], [-1, 0, 1]):
                self.hash_mat[int(x[0]) + i][int(x[1]) + j].append(x)

        self.connection_matrix = npr.random(size=(self.N, self.N))

    def perturb(self):
        """Brownian-motions the particles around"""
        self.all_particles[:, :2] += npr.standard_normal(size=(self.N, 2)) * 0.01
        self.all_particles[:, :2] = np.clip(
            self.all_particles[:, :2], 0, (self.WIDTH - 0.01, self.HEIGHT - 0.01)
        )

        # Ocationally update hash_mat
        if npr.random() < 0.01:
            self.hash_mat = [
                [[] for j in range(int(self.HEIGHT) + 1)]
                for i in range(int(self.WIDTH) + 1)
            ]

            for x in self.all_particles:
                for (i, j) in product([-1, 0, 1], [-1, 0, 1]):
                    self.hash_mat[int(x[0]) + i][int(x[1]) + j].append(x)

    def draw(self):
        """Draws rcm to `self.screen`"""
        lambda_cut_ind = np.where(self.all_particles[:, 2] < self.lambda_cur)
        for x in self.all_particles[lambda_cut_ind]:
            pygame.draw.circle(
                self.screen,
                blue,
                (
                    self.scale * x[0] + self.loc_x,
                    self.scale * x[1] + self.loc_y,
                ),
                5,
            )
            for y in self.hash_mat[int(x[0])][int(x[1])]:
                if (
                    x[3] > y[3]
                    and y[2] < self.lambda_cur
                    and np.linalg.norm(x[:2] - y[:2]) <= 1
                    and self.connection_matrix[int(x[3]), int(y[3])] < self.p_cur
                ):
                    pygame.draw.line(
                        self.screen,
                        grey,
                        (
                            self.scale * x[0] + self.loc_x,
                            self.scale * x[1] + self.loc_y,
                        ),
                        (
                            self.scale * y[0] + self.loc_x,
                            self.scale * y[1] + self.loc_y,
                        ),
                        2,
                    )
