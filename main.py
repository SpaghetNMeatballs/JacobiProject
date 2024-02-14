from math import sin, cos, sqrt
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class Phi:
    tgn: float
    cos: float
    sin: float


class Jacobi:
    def __init__(self, a: list[list[float]]):
        self.iterations = 0
        self.a = []
        self.height = len(a)
        self.s = 0
        self.v = [[1 for _ in range(self.height)].copy() for _ in range(self.height)]

        flag = True
        row0len = len(a)
        for i in range(0, len(a)):
            self.s -= a[i][i] ** 2
            if len(a) != row0len:
                flag = False
        assert flag, "Matrix does not have consistent dimensions"

        for row in a:
            self.s += sum([i**2 for i in row])
            self.a.append(row.copy())

    def gen_p(self, phi: Phi, p: int, q: int):
        assert p != q, "p equals q"
        temp_p = [[0 for _ in range(self.height)].copy() for _ in range(self.height)]
        for i in range(self.height):
            temp_p[i][i] = 1
        temp_p[p][p] = temp_p[q][q] = phi.cos
        p, q = max(p, q), min(p, q)
        temp_p[q][p] = phi.sin
        temp_p[p][q] = -phi.sin
        return temp_p

    def calc_phi(self, p: int, q: int) -> Phi:
        assert p != q, "p equals q"
        top = self.a[q][q] - self.a[p][p]
        bot = 2 * self.a[p][q]
        if bot == 0:
            pass
        c = top / bot
        if c >= 0:
            tgphi = 1 / (c + sqrt(c**2 + 1))
        else:
            tgphi = 1 / (c - sqrt(c**2 + 1))
        cosphi = 1 / (sqrt(1 + tgphi**2))
        sinphi = tgphi * cosphi
        return Phi(tgphi, cosphi, sinphi)

    def zero_element(self, p: int, q: int):
        new_field = []
        for i in range(self.height):
            new_field.append([])
            for j in range(self.height):
                new_field[i].append(self.a[i][j])

        phi = self.calc_phi(p, q)
        new_field[p][q] = new_field[q][p] = 0
        new_field[p][p] = self.a[p][p] - self.a[p][q] * phi.tgn
        new_field[q][q] = self.a[q][q] - self.a[p][q] * phi.tgn
        for i in range(self.height):
            if i == p or i == q:
                continue
            if i != p:
                new_field[i][p] = new_field[p][i] = self.a[i][p] - phi.sin * (
                    self.a[i][q] + phi.sin / (1 + phi.cos) * self.a[i][p]
                )
                self.v[i][p] = self.v[i][p] * phi.cos - self.v[i][q] * phi.sin
            if i != q:
                new_field[i][q] = new_field[q][i] = self.a[i][q] + phi.sin * (
                    self.a[i][p] - phi.sin / (1 + phi.cos) * self.a[i][q]
                )
                self.v[i][q] = self.v[i][p] * phi.sin + self.v[i][q] * phi.cos
                pass
        self.s -= 2*self.a[p][q] ** 2
        self.a = deepcopy(new_field)

    def iterate(self):
        p, q = 0, 1
        for i in range(self.height):
            for j in range(self.height):
                if abs(self.a[i][j]) > abs(self.a[p][q]) and i != j:
                    p, q = i, j
        self.zero_element(p, q)


if __name__ == "__main__":
    a = [[i for i in range(j, j + 3 * 5, 3)] for j in range(1, 14, 3)]
    test = Jacobi(a)
    phi = test.calc_phi(1, 3)
    p_cur = test.gen_p(phi, 1, 3)
    for i in range(20):
        test.iterate()
        print(f"\t\tIteration №{i+1}\n\t\tS = {test.s}")
        for row in test.a:
            print(*[f"{i:.2f}" for i in row], sep="\t")
    pass
