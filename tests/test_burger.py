"""Модуль содержит тесты для класса Burger"""

import pytest

from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient


class TestBurger:
    """
    Набор тестов для класса Burger
    """

    @pytest.fixture
    def bun(self):
        """
        Фикстура, создающая тестовую булочку для бургера
        """
        return Bun("white bun", 100.0)

    @pytest.fixture
    def ingredient_sauce(self):
        """
        Фикстура, создающая тестовый ингредиент - соус
        """
        return Ingredient("SAUCE", "hot sauce", 90.0)

    @pytest.fixture
    def ingredient_filling(self):
        """
        Фикстура, создающая тестовый ингредиент - начинку
        """
        return Ingredient("FILLING", "cheese", 200.0)

    @pytest.fixture
    def burger_with_ingredients(self, bun, ingredient_sauce, ingredient_filling):
        """
        Создает бургер с булочкой и двумя ингредиентами (соус и начинка) для тестирования
        """
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient_sauce)
        burger.add_ingredient(ingredient_filling)
        return burger

    def test_set_buns(self, bun):
        """Проверка установки булочки в бургер"""
        burger = Burger()
        burger.set_buns(bun)
        assert burger.bun == bun

    def test_add_ingredient(self, bun, ingredient_sauce):
        """Проверка добавления ингредиента в бургер"""
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient_sauce)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ingredient_sauce

    def test_remove_ingredient(self, burger_with_ingredients):
        """Проверка удаления ингредиента из бургера"""
        initial_count = len(burger_with_ingredients.ingredients)
        burger_with_ingredients.remove_ingredient(0)
        assert len(burger_with_ingredients.ingredients) == initial_count - 1

    def test_move_ingredient(self, burger_with_ingredients):
        """Тест на перемещение ингредиентов"""
        burger_with_ingredients.ingredients = []

        hot_sauce = Ingredient("SAUCE", "hot sauce", 90.0)
        cheese = Ingredient("FILLING", "cheese", 200.0)
        burger_with_ingredients.add_ingredient(hot_sauce)
        burger_with_ingredients.add_ingredient(cheese)

        initial_order = [ingredient.get_name() for ingredient in burger_with_ingredients.ingredients]
        assert initial_order == ["hot sauce", "cheese"]

        burger_with_ingredients.move_ingredient(0, 1)

        result_order = [ingredient.get_name() for ingredient in burger_with_ingredients.ingredients]
        assert result_order == ["cheese", "hot sauce"]

    def test_get_price(self, mocker):
        """Проверка расчета цены бургера с моками"""
        mock_bun = mocker.Mock()
        mock_bun.get_price.return_value = 100.0

        mock_ingredient1 = mocker.Mock()
        mock_ingredient1.get_price.return_value = 50.0

        mock_ingredient2 = mocker.Mock()
        mock_ingredient2.get_price.return_value = 75.0

        burger = Burger()
        burger.bun = mock_bun
        burger.ingredients = [mock_ingredient1, mock_ingredient2]

        expected_price = 100.0 * 2 + 50.0 + 75.0
        assert burger.get_price() == expected_price

        mock_bun.get_price.assert_called_once()
        mock_ingredient1.get_price.assert_called_once()
        mock_ingredient2.get_price.assert_called_once()

    def test_get_receipt(self, mocker):
        """Проверка формирования чека"""
        mock_bun = mocker.Mock()
        mock_bun.get_name.return_value = "white bun"

        mock_ingredient1 = mocker.Mock()
        mock_ingredient1.get_type.return_value = "SAUCE"
        mock_ingredient1.get_name.return_value = "hot sauce"

        mock_ingredient2 = mocker.Mock()
        mock_ingredient2.get_type.return_value = "FILLING"
        mock_ingredient2.get_name.return_value = "cheese"

        burger = Burger()
        burger.bun = mock_bun
        burger.ingredients = [mock_ingredient1, mock_ingredient2]

        mocker.patch.object(burger, 'get_price', return_value=390.0)

        expected_receipt = (
            "(==== white bun ====)\n"
            "= sauce hot sauce =\n"
            "= filling cheese =\n"
            "(==== white bun ====)\n\n"
            "Price: 390.0"
        )

        assert burger.get_receipt() == expected_receipt

        assert mock_bun.get_name.call_count == 2
        mock_ingredient1.get_type.assert_called_once()
        mock_ingredient1.get_name.assert_called_once()
        mock_ingredient2.get_type.assert_called_once()
        mock_ingredient2.get_name.assert_called_once()

    def test_remove_nonexistent_ingredient(self, burger_with_ingredients):
        """Проверка обработки попытки удаления несуществующего ингредиента"""
        initial_ingredients = burger_with_ingredients.ingredients.copy()

        with pytest.raises(IndexError):
            burger_with_ingredients.remove_ingredient(999)

        assert burger_with_ingredients.ingredients == initial_ingredients

    def test_move_nonexistent_ingredient(self, burger_with_ingredients):
        """Проверка обработки попытки перемещения несуществующего ингредиента"""
        # Сохраняем начальное состояние
        initial_ingredients = burger_with_ingredients.ingredients.copy()
        
        with pytest.raises(IndexError):
            burger_with_ingredients.move_ingredient(999, 0)

        assert burger_with_ingredients.ingredients == initial_ingredients

    def test_move_to_nonexistent_position(self, burger_with_ingredients):
        """Проверка обработки попытки перемещения в несуществующую позицию"""
        initial_ingredients = burger_with_ingredients.ingredients.copy()
        burger_with_ingredients.move_ingredient(0, 999)

        assert len(burger_with_ingredients.ingredients) == len(initial_ingredients)
        assert set(burger_with_ingredients.ingredients) == set(initial_ingredients)

    def test_get_price_without_bun(self, burger_with_ingredients):
        """Проверка расчета цены без установленной булочки"""
        burger_with_ingredients.bun = None
        with pytest.raises(AttributeError):
            burger_with_ingredients.get_price()

    def test_get_receipt_without_bun(self, burger_with_ingredients):
        """Проверка формирования чека без установленной булочки"""
        burger_with_ingredients.bun = None
        with pytest.raises(AttributeError):
            burger_with_ingredients.get_receipt()
