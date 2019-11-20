class Calculations:
    Y_COORD = 320
    X_R_COORD = 640
    X_L_COORD = 320
    X_MID_COORD = 480

    # x1/y1 are the coordinates on the upper left side of the opencv frame
    # x2/y2 are the coordinates on the lower right side of the opencv frame

    def line_left(self, x1):

        x_l_corr = self.X_L_COORD - x1
        return x_l_corr

    def line_right(self, x2):

        x_r_corr = self.X_R_COORD - x2
        return x_r_corr

    def line_top(self, y1):

        y_corr = self.Y_COORD - y1
        return y_corr

    def line_middle(self, x1, x2):

        box_width = (x2 - x1) / 2
        box_mid = x1 + box_width
        mid_corr = self.X_MID_COORD - box_mid
        return mid_corr

    def step_direction(self, n):

        if n > 0:
            direction = 1
        elif n < 0:
            direction = 0
        else:
            direction = -1

        return direction
