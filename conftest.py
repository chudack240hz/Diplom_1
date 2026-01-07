import pytest

from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient


@pytest.fixture
def bun():
    """
    Фикстура, создающая тестовую булочку для бургера
    """
    return Bun("white bun", 100.0)


@pytest.fixture
def ingredient_sauce():
    """
    Фикстура, создающая тестовый ингредиент - соус
    """
    return Ingredient("SAUCE", "hot sauce", 90.0)


@pytest.fixture
def ingredient_filling():
    """
    Фикстура, создающая тестовый ингредиент - начинку
    """
    return Ingredient("FILLING", "cheese", 200.0)


@pytest.fixture
def burger_with_ingredients(bun, ingredient_sauce, ingredient_filling):
    """
    Создает бургер с булочкой и двумя ингредиентами (соус и начинка) для тестирования
    """
    burger = Burger()
    burger.set_buns(bun)
    burger.add_ingredient(ingredient_sauce)
    burger.add_ingredient(ingredient_filling)
    return burger
