import pytest
import numpy as np
from game.core import generate_perlin_noise_2d, interpolant


class TestPerlinNoise:
    """Tests pour le générateur de bruit de Perlin"""

    @pytest.fixture
    def default_shape(self):
        """Fixture pour la forme par défaut"""
        return (100, 100)

    @pytest.fixture
    def default_res(self):
        """Fixture pour la résolution par défaut"""
        return (10, 10)

    def test_interpolant_function(self):
        """Test de la fonction d'interpolation"""
        # Test des valeurs limites
        assert np.isclose(interpolant(0), 0)
        assert np.isclose(interpolant(1), 1)

        # Test des valeurs intermédiaires
        t = 0.5
        result = interpolant(t)
        assert 0 <= result <= 1

        # Test de la continuité
        t_values = np.linspace(0, 1, 1000)
        results = [interpolant(t) for t in t_values]
        assert all(0 <= r <= 1 for r in results)

    def test_output_shape(self, default_shape, default_res):
        """Test que la sortie a la bonne forme"""
        noise = generate_perlin_noise_2d(default_shape, default_res)
        assert noise.shape == default_shape

    def test_output_range(self, default_shape, default_res):
        """Test que les valeurs sont dans une plage raisonnable"""
        noise = generate_perlin_noise_2d(default_shape, default_res)
        assert -2 <= noise.min() <= -0.5
        assert 0.5 <= noise.max() <= 2

    def test_different_shapes(self, default_res):
        """Test avec différentes formes"""
        shapes = [(50, 50), (200, 100), (100, 200)]

        for shape in shapes:
            noise = generate_perlin_noise_2d(shape, default_res)
            assert noise.shape == shape

    def test_reproducibility(self, default_shape, default_res):
        """Test de la reproductibilité avec une graine aléatoire"""
        np.random.seed(42)
        noise1 = generate_perlin_noise_2d(default_shape, default_res)

        np.random.seed(42)
        noise2 = generate_perlin_noise_2d(default_shape, default_res)

        assert np.allclose(noise1, noise2)

    def test_custom_interpolant(self, default_shape, default_res):
        """Test avec une fonction d'interpolation personnalisée"""

        def custom_interpolant(t):
            return t * t * (3 - 2 * t)

        noise = generate_perlin_noise_2d(
            default_shape, default_res, interpolant=custom_interpolant
        )
        assert noise.shape == default_shape

    @pytest.mark.parametrize(
        "shape,res",
        [((100, 100), (10, 10)), ((200, 100), (20, 10)), ((50, 150), (5, 15))],
    )
    def test_various_configurations(self, shape, res):
        """Test paramétré avec différentes configurations"""
        noise = generate_perlin_noise_2d(shape, res)
        assert noise.shape == shape

    def test_gradient_consistency(self, default_shape, default_res):
        """Test de la cohérence des gradients"""
        noise = generate_perlin_noise_2d(default_shape, default_res)

        # Vérifier que les gradients locaux ne sont pas trop abrupts
        gradient_x = np.diff(noise, axis=0)
        gradient_y = np.diff(noise, axis=1)

        assert np.max(np.abs(gradient_x)) < 1.0
        assert np.max(np.abs(gradient_y)) < 1.0

    def test_memory_efficiency(self, default_shape, default_res):
        """Test de l'efficacité mémoire"""
        import tracemalloc

        tracemalloc.start()
        noise = generate_perlin_noise_2d(default_shape, default_res)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        assert noise is not None

        # Vérifier que l'utilisation de la mémoire reste raisonnable
        # (ajuster la valeur selon les besoins)
        assert peak < 10 * 1024 * 1024  # 10 MB
