from time import time

from django.core.files.base import ContentFile

AMOUNT_INDEX = 0  # index of name in dict result
UNIT_INDEX = 1  # index of measurement unit in dict result


def cart_format(item: tuple) -> str:
    ingredient_name = item[0]
    amount, unit = item[1]

    return (
        f"{ingredient_name}: {amount} {unit}."
    )


def get_ingredients(cart) -> list[str]:
    dict_result = {}  # {'name'}: [amount, measurement_unit]
    result = []

    for element in cart:
        recipe = element.recipe

        for ingredient_amount in recipe.ingredients.all():
            ingredient = ingredient_amount.ingredient

            ingredient_name = ingredient.name
            unit = ingredient.measurement_unit
            amount = int(ingredient_amount.amount)

            if (
                ingredient_name in list(dict_result.keys())
                and dict_result[ingredient_name][UNIT_INDEX] == unit
            ):
                dict_result[ingredient_name][AMOUNT_INDEX] += amount

            else:
                dict_result[ingredient_name] = [amount, unit]

    for res in dict_result.items():
        result.append(cart_format(res))

    return result


def make_shopping_file(cart) -> ContentFile:
    text = '\n'.join(get_ingredients(cart))
    text += '\n' + "Enjoy your lunch :)"
    return ContentFile(text.encode(), "shopping_list_" + str(time()) + ".pdf")
