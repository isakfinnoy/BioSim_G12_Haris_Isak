from biosim.animals import Herbivore, Carnivore, Animals
import pytest
from scipy.stats import kstest
ALPHA = 0.01

__author__ = 'Haris Karovic', 'Isak Finnøy'
__email__ = 'harkarov@nmbu.no', 'isfi@nmbu.no'


class TestAnimals:
    """
    Testing methods of animal file.
    """

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_constructor(self, Species):
        s = Species(5, 15.0)
        assert hasattr(s, 'age')
        assert hasattr(s, 'weight')
        assert hasattr(s, 'fitness')
        assert hasattr(s, 'has_migrated')
        assert s.age == 5
        assert s.weight == 15.0
        assert isinstance(s, Animals)
        assert isinstance(s.has_migrated, bool)
        with pytest.raises(TypeError, match="'age' must be of type int "):
            assert Animals(age=3.4)
        with pytest.raises(TypeError, match='Weight must be either of type int or type float'):
            assert Animals(weight='string')
        with pytest.raises(ValueError, match="'age' must be greater than or equal to zero"):
            assert Animals(age=-1)
        with pytest.raises(ValueError, match="'weight' must be greater than or equal to zero"):
            assert Animals(weight=-1)

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_set_has_migrated(self, Species):
        """
        Asserts that the set_has_migrated method updates the boolean value.
        """
        s = Species()
        s.has_migrated = False
        s.set_has_migrated(True)
        assert s.has_migrated
        with pytest.raises(TypeError):
            assert s.set_has_migrated([3, 2])

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_new_animal(self, Species):
        """
        asserts that a new herbivore has age 0.
        """
        s = Species()
        assert s.age == 0

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_animal_age(self, Species):
        """
        Tests that the update age method ages the animal by one year
        """
        s = Species(2, 5.0)
        old_fitness = s.fitness
        s.update_age()
        new_fitness = s.fitness
        assert s.age == 3
        assert new_fitness != old_fitness

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_subclass(self, Species):
        """
        Tests that Herbivore and Carnivore is a subclass of Animals
        """
        s = Species()
        assert issubclass(s.__class__, Animals)

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_instance_super(self, Species):
        """
        Tests that Herbivore-object and Carnivore-object is an instance of Animals
        """
        s = Species()
        assert isinstance(s, Animals)

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_initial_weight(self, Species):
        """
        Testing if the birth weight is positive
        """
        s = Species()
        assert s.weight >= 0

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_yearly_weight_loss(self, Species):
        """
        Testing if yearly_weight_loss results in lower weight
        """

        s = Species(2, 20)
        old_weight = s.weight
        old_fitness = s.fitness
        s.yearly_weight_loss()
        new_weight = s.weight
        new_fitness = s.fitness
        assert new_weight < old_weight
        assert new_fitness < old_fitness

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_eat_limits(self, Species):
        """
        Testing if available food lower than appetite leads to expected weight increase
        """
        s = Species(2, 5.0)
        s.eat(7.0)
        exp_inc_s = s.params['beta'] * 7.0
        assert s.weight == (5.0 + exp_inc_s)

    def test_eat_appetite(self):
        """
        Testing if available food higher than appetite results in weight increase limited by the
        appetite
        """
        h = Herbivore(2, 5.0)
        c = Carnivore(3, 7.0)
        h.eat(15)
        c.eat(75)
        exp_inc_h = h.params['beta'] * 10.0
        exp_inc_c = c.params['beta'] * 50.0
        assert h.weight == (5.0 + exp_inc_h) and c.weight == (7.0 + exp_inc_c)

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_update_fitness_new_param(self, Species):
        """
        Testing if update_fitness updates fitness with different parameters
        """
        s = Species(2, 5.0)
        f1 = s.fitness
        s.age = 5
        s.weight = 10.0
        s.update_fitness()
        f2 = s.fitness
        assert f1 < f2

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_update_fitness_same_param(self, Species):
        """
        Testing that the update_fitness function doesnt change fitness for same parameters.
        """
        s = Species(2, 5.0)
        f1 = s.fitness
        s.update_fitness()
        f2 = s.fitness
        assert f1 == f2

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_fitness(self, Species):
        """
        Testing that the fitness attribute is a float.
        """
        s = Species(2, 5.0)
        assert isinstance(s.fitness, float)

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_fitness_weight(self, Species):
        """
        Testing that fitness equals zero if weight is zero.
        """
        s = Herbivore(2, 0.0)
        s.update_fitness()
        assert s.fitness == 0

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_eat_valerr(self, Species):
        """
        Asserts that input of negative fodder raises a ValueError.
        """
        s = Species(2, 5.0)
        with pytest.raises(ValueError):
            assert s.eat(-1)

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_eat_fodder(self, Species):
        """
        Asserts that animal eat all of the fodder if it is less than its appetite.
        """
        s = Species(2, 5.0)
        fodder = s.params['F'] - 5
        assert s.eat(fodder) == fodder

    def test_eat_food_eaten(self):
        """
        Testing that fodder is float.
        """
        h = Herbivore(2, 5.0)
        float_ = 5.0
        fodder = h.eat(float_)
        assert isinstance(fodder, float)

    def test_set_params(self):
        """
        Testing if the set_params method updates herbivore's default parameters with new_parameters.
        """
        h = Herbivore()
        new_parameters = {
            'w_birth': 8.0, 'sigma_birth': 2.0, 'beta': 1.5, 'eta': 0.25, 'a_half': 40.0,
            'phi_age': 0.6, 'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2,
            'zeta': 3.5, 'xi': 1.2, 'omega': 0.4, 'F': 10.0
        }
        h.set_params(new_parameters)
        assert h.params == new_parameters
        false_parameter = {'nice': 69}
        with pytest.raises(KeyError):
            assert h.set_params(false_parameter)
        with pytest.raises(TypeError, match='params must be of type dict'):
            assert h.set_params([1])

    def test_birth(self, mocker):
        """
        Testing the birth function. Mocks out the random function with 0, guaranteeing that the
        probability for death exceeds the random function, which should yield the boolean True.
        """
        mocker.patch("numpy.random.uniform", return_value=0)
        h = Herbivore(2, 50.0)
        c = Carnivore(3, 50.0)
        h2 = Herbivore(0, 0)
        herb = h.birth(30)
        carni = c.birth(50)
        assert isinstance(herb, Herbivore)
        assert isinstance(carni, Carnivore)
        assert h2.birth(10) is None

    def test_death(self, mocker):
        """
        Testing the death function. Mocks out the random function with 0, guaranteeing that the
        probability for death exceeds the random function, which should yield the boolean True.
        """
        mocker.patch("numpy.random.uniform", return_value=0)
        h = Herbivore(2, 5.0)
        c = Carnivore(3, 7.0)
        dead_herb = h.death()
        dead_carn = c.death()
        assert dead_herb is True
        assert dead_carn is True

    def test_death2(self):
        """
        Testing that an animal with zero weight will return True, which means the animal is dead
        :return: Boolean (True = dead)
        """
        h = Herbivore(0, 0)
        assert h.death() is True

    def test_migrate(self, mocker):
        """
        Testing the migration function. Mocks out the random function with 0, guaranteeing that the
        probability for migration exceeds the random function, which will then yield the boolean
        True.
        """
        mocker.patch('numpy.random.uniform', return_value=0)
        h = Herbivore(2, 5.0)
        c = Carnivore(3, 7.0)
        move_herb = h.migrate()
        move_carn = c.migrate()
        assert move_herb is True
        assert move_carn is True

    def test_slay(self, mocker):

        mocker.patch('numpy.random.uniform', return_value=0)

        h = Herbivore()
        c = Carnivore()
        h.fitness = 10
        c.fitness = 5

        carn_slay_herb = c.slay(h)

        h2 = Herbivore()
        c2 = Carnivore()
        h2.fitness = 5
        c2.fitness = 10

        carn_slay_herb2 = c2.slay(h2)

        assert carn_slay_herb is False
        assert carn_slay_herb2 is True

    def test_eat_carn(self):
        herb_list = [Herbivore(5, 20) for _ in range(10)]
        for herbivore in herb_list:
            herbivore.fitness = 1
        carn_list = [Carnivore(5, 20) for _ in range(10)]
        for carnivore in carn_list:
            carnivore.fitness = 0.5
            dead_herbs = carnivore.eat_carn(herb_list)

            assert len(dead_herbs) == 0

    def test_slay2(self, mocker):
        mocker.patch('numpy.random.uniform', return_value=1)
        h3 = Herbivore()
        c3 = Carnivore()
        h3.fitness = 5
        c3.fitness = 10
        c3.set_params({'DeltaPhiMax': 0.1})

        carn_slay_herb3 = c3.slay(h3)
        assert carn_slay_herb3 is True

    def test_eat_carn2(self):

        h = Herbivore(2, 10)
        h.fitness = 10
        h_list = [h]

        c = Carnivore(5, 20)
        c.fitness = 20
        c.set_params({'DeltaPhiMax': 10.0})
        c.eat_carn(h_list)
        assert c.weight == 20 + 0.75 * h.weight

    def test_eat_carn3(self):

        h = Herbivore(2, 60)
        h.fitness = 10
        h_list = [h]

        c = Carnivore(5, 20)
        c.fitness = 20
        old_weight = c.weight
        c.set_params({'DeltaPhiMax': 10.0})
        c.eat_carn(h_list)
        assert c.weight == old_weight + c.params['beta'] * (h.weight-10)

    def test_slay_fitness(self):
        """
        Asserts that Carnivores with a lower fitness than
        """
        c = Carnivore()
        h = Herbivore()
        c.fitness = 0.5
        h.fitness = 0.75
        assert c.slay(h) is False

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_initial_weight_gaussian_dist(self, Species):
        """
        Testing if the initial weight of the animals is normally distributed. Inital weight is
        initialised using numpy.random.normal with respective birth parameters as input. We are
        testing against an critical value of 0.01 to validate for a confidence level of 99%.
        """

        list_of_initial_weights = []
        for _ in range(5000):
            s = Species()
            list_of_initial_weights.append(s.weight)
            ks_stat, p_val = kstest(list_of_initial_weights, 'norm')
            assert p_val < ALPHA
