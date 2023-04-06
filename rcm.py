""" This file simulates an RCM for pygame """
from itertools import product
import numpy as np
import numpy.random as npr
import pygame

grey = pygame.Color(80, 90, 90)
blue = pygame.Color(40, 40, 200)


class RCM:
    """Generates an RCM with draw functionallity"""

    def __init__(self, loc_x=0, loc_y=0, scale=20):
        """Initializes RCM"""
        self.screen = None
        self.scale = scale
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.WIDTH = 20
        self.HEIGHT = 13
        self.lambda_max = 5
        self.lambda_cur = 1
        self.p_cur = 0.5
        self.show_largest = False

        self.N = npr.poisson(self.WIDTH * self.HEIGHT * self.lambda_max)
        self.all_particles = npr.uniform(size=(self.N, 3))

        self.all_particles[:, 0] *= self.WIDTH
        self.all_particles[:, 1] *= self.HEIGHT
        self.all_particles[:, 2] *= self.lambda_max

        # We sort by intensity (this will help with loop breaking)
        self.all_particles = self.all_particles[self.all_particles[:, 2].argsort()]

        self.hash_mat = [
            [[] for j in range(int(self.HEIGHT) + 1)]
            for i in range(int(self.WIDTH) + 1)
        ]

        for i, x in enumerate(self.all_particles):
            self.hash_mat[int(x[0])][int(x[1])].append((i, x))

        self.connection_matrix = npr.random(size=(self.N, self.N))

        self.current_connection = np.zeros_like(self.connection_matrix)
        for idx, x in enumerate(all_particles):
            if x[-1] > self.lambda_cur:
                break
            for idy, y in self.get_hash_nbhd((int(x[0]), int(x[1]))):
                if y[-1] > x[-1]


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

    def get_hash_nbhd(self, hk):
        nbhd = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= hk[0] + i < self.WIDTH and 0 <= hk[1] + j < self.HEIGHT:
                    nbhd = nbhd + self.hash_mat[(hk[0] + i)][(hk[1] + j)]
        return nbhd

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
        self.all_particles = self.all_particles[self.all_particles[:, 2].argsort()]

        self.hash_mat = [
            [[] for j in range(int(self.HEIGHT) + 1)]
            for i in range(int(self.WIDTH) + 1)
        ]
        for i, x in enumerate(self.all_particles):
            self.hash_mat[int(x[0])][int(x[1])].append((i, x))

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

            for i, x in enumerate(self.all_particles):
                self.hash_mat[int(x[0])][int(x[1])].append((i, x))

    def draw(self):
        """Draws rcm to `self.screen`"""
        for idx, x in enumerate(self.all_particles):
            if x[-1] > self.lambda_cur:
                break
            pygame.draw.circle(
                self.screen,
                blue,
                (
                    self.scale * x[0] + self.loc_x,
                    self.scale * x[1] + self.loc_y,
                ),
                5,
            )
            for idy, y in self.get_hash_nbhd((int(x[0]), int(x[1]))):
                if y[-1] > x[-1]:
                    continue
                if (
                    np.linalg.norm(x[:2] - y[:2]) <= 1
                    and self.connection_matrix[idx, idy] < self.p_cur
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
