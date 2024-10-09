def show_function_from_cs(cs):
    if not cs:
        return ""
    h, *t = cs
    return f"{h} * x1" + "".join(f"{' - ' if c < 0 else ' + '}{abs(c)} * x{i}"
                                 for i, c in enumerate(t, start=2))


class simplex:
    MODE_MAXIMIZE = "max"
    MODE_MINIMIZE = "min"

    def init(self, mode, c, a, b, eps):
        if mode not in {self.MODE_MAXIMIZE, self.MODE_MINIMIZE}:
            raise Exception(f"Unknown mode: {mode}")
        self.mode = mode
        self.c = c
        self.a = a
        self.b = b
        self.eps = eps
        self.base = []
        self.solution = 0

    def print_problem(self):
        print(f"{self.mode} z = {show_function_from_cs(self.c)}")
        print("subject to the constraints:")
        print("\n".join(f"{show_function_from_cs(cs)} <= {rhs}" for cs, rhs in zip(self.a, self.b)))

    def to_standard_form(self):
        for row in range(len(self.a)):
            if 1 not in self.a[row]:
                for row2 in range(len(self.a)):
                    self.a[row2].append(1 if row == row2 else 0)
                # slack variables are denoted by 0
                self.base.append(0)
                self.c.append(0)
            else:
                self.base.append(self.a[row].index(1))

    def pivot_column(self):
        r = min(((i, self.c[i])
                 for i in range(len(self.c))
                 if self.c[i] < 0),
                default=None,
                key=lambda x: x[1])
        if r:
            return r[0]
        else:
            return r

    def pivot_row(self, col):
        r = min(((i, self.b[i] / self.a[i][col])
                 for i in range(len(self.a))
                 if self.b[i] / self.a[i][col] > 0),
                default=None,
                key=lambda x: x[1])
        if r:
            return r[0]
        else:
            return r

    def step(self):
        c = self.pivot_column()
        if c is None:
            return None
        r = self.pivot_row(c)
        if r is None:
            return None
        k = self.a[r][c]

        # target row
        for col in range(len(self.a[r])):
            self.a[r][col] /= k
        self.b[r] /= k

        # set base variable
        self.base

        # divide all other rows by the target row
        for row in range(len(self.a)):
            # skip the target row
            if row == r:
                continue
            m = self.a[row][c] / self.a[r][c]
            for col in range(len(self.a[row])):
                self.a[row][col] -= m * self.a[r][col]
            self.b[row] -= m * self.b[r]

        # for obj function
        m = self.c[c]
        for col in range(len(self.c)):
            self.c[col]-= m *self.a[r][col]

        self.solution -= m *self.b[r]
        return 1

    def solve(self):
        self.to_standard_form()
        while True:
            if self.step() is None:
                return


if __name__ == "__main__":
    pass

solver = simplex()
objective_function = [-9, -10, -16]  # целевая функция
constraints_matrix = [
    [18, 15, 12],
    [6, 4, 8],
    [5, 3, 3]
]

constraints_rhs = [360, 192, 180]
epsilon = 1e-9
solver.init(solver.MODE_MAXIMIZE, objective_function, constraints_matrix, constraints_rhs, epsilon)
solver.print_problem()
print()
solver.solve()
solver.print_problem()