import numpy as np


def interpolant(t: np.ndarray) -> np.ndarray:
    """
    Fonction d'interpolation pour le bruit de Perlin.

    :param t: Un tableau numpy de valeurs entre 0 et 1.
    :type t: numpy.ndarray
    :return: Un tableau numpy de valeurs interpolées.
    :rtype: numpy.ndarray
    """
    return t * t * t * (t * (t * 6 - 15) + 10)


def generate_perlin_noise_2d(
    shape, res, tileable=(False, False), interpolant=interpolant
):
    """
    Génération de bruit de Perlin 2D.

    :param shape: La forme du tableau numpy généré (tuple de deux entiers).
    :type shape: tuple
    :param res: Le nombre de périodes de bruit à générer le long de chaque axe.
    :type res: tuple
    :param tileable: Si le bruit doit être tuilable le long de chaque axe.
    :type tileable: tuple
    :param interpolant: La fonction d'interpolation.
    :type interpolant: function
    :return: Un tableau numpy de bruit de Perlin.
    :rtype: numpy.ndarray
    """
    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = (
        np.mgrid[0 : res[0] : delta[0], 0 : res[1] : delta[1]].transpose(
            1, 2, 0
        )
        % 1
    )
    # Gradients
    angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    if tileable[0]:
        gradients[-1, :] = gradients[0, :]
    if tileable[1]:
        gradients[:, -1] = gradients[:, 0]
    gradients = gradients.repeat(d[0], 0).repeat(d[1], 1)
    g00 = gradients[: -d[0], : -d[1]]
    g10 = gradients[d[0] :, : -d[1]]
    g01 = gradients[: -d[0], d[1] :]
    g11 = gradients[d[0] :, d[1] :]
    # Ramps
    n00 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1])) * g00, 2)
    n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)
    # Interpolation
    t = interpolant(grid)
    n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
    n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
    return np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)
