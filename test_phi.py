from main import Phi, Jacobi
from pytest import fixture, approx


def test_phi():
    a = [[i for i in range(j, j + 3 * 5, 3)] for j in range(1, 14, 3)]
    jac = Jacobi(a)
    phi = jac.calc_phi(1, 3)
    assert phi.tgn == approx(0.64, 0.1)
    assert phi.cos == approx(0.842, 0.1)
    assert phi.sin == approx(0.539, 0.1)


def test_zero():
    a = [[i for i in range(j, j + 3 * 5, 3)] for j in range(1, 14, 3)]
    jac = Jacobi(a)
    jac.zero_element(1, 3)
    assert jac.a[1][3] == jac.a[3][1] == 0
