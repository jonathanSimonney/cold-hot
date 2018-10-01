import numpy as np
import matplotlib.pyplot as pyp


class SteelPlate:
    def __init__(self, x_dim, y_dim, ambiant_temperature, object_temp):
        self.x_dim = x_dim + 2
        self.y_dim = y_dim + 2

        outer_and_inner_temp = np.zeros((self.x_dim, self.y_dim)) + object_temp
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if self._coords_are_on_side(x, y):
                    outer_and_inner_temp[x, y] = ambiant_temperature
        self.grid = outer_and_inner_temp

    def get_inner_grid(self):
        ret = np.zeros((self.x_dim - 2, self.y_dim - 2))
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if not self._coords_are_on_side(x, y):
                    ret[x - 1, y - 1] = self.grid[x, y]
        return ret

    def draw_picture(self):
        pyp.clf()
        pyp.imshow(self.get_inner_grid(), origin="upper", extent=[0, self.x_dim - 2, 0, self.y_dim - 2],
                   interpolation="bilinear")
        pyp.draw()
        pyp.axis('off')

    def change_temp_inside_once(self):
        future_grid = np.copy(self.grid)
        max_delta = 0

        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if not self._coords_are_on_side(x, y):
                    new_value = (self.grid[x - 1, y] + self.grid[x + 1, y] + self.grid[x, y + 1] + self.grid[x, y - 1] +
                                 self.grid[x, y]) / 5
                    future_grid[x, y] = new_value

                    candidate_delta = new_value - self.grid[x, y]
                    if max_delta < candidate_delta:
                        max_delta = candidate_delta
        self.grid = future_grid
        return max_delta

    def change_temp_inside_until_max_delta_is_reached(self, max_delta):
        current_delta = self.change_temp_inside_once()
        while current_delta > max_delta:
            current_delta = self.change_temp_inside_once()
            print(current_delta)
            self.draw_picture()
            pyp.pause(1)
        self.draw_picture()

    def change_temp_outside(self, x, y, temp):
        if self._coords_are_on_side(x, y):
            self.grid[x, y] = temp
        else:
            raise ValueError("the coords given aren't on the side of the plate")

    def _coords_are_on_side(self, x, y):
        return x == 0 or x + 1 == self.x_dim or y == 0 or y + 1 == self.y_dim


steel_plate = SteelPlate(1000, 1000, 25, 13)

steel_plate.change_temp_outside(0, 1, 0)
steel_plate.change_temp_outside(1, 0, 0)
steel_plate.change_temp_outside(1001, 1000, 1000)
steel_plate.change_temp_outside(1000, 1001, 1000)
steel_plate.change_temp_inside_once()

steel_plate.change_temp_inside_until_max_delta_is_reached(0.1)

