import json
import math
from pathlib import Path
from typing import NamedTuple

from app.customers.customer import Customer


class Point(NamedTuple):
    px: int
    py: int


base_dir = Path(__file__).resolve().parent
file_name = "config.json"


def get_data_from_file() -> tuple:
    with open(base_dir / file_name, "r") as file:
        file_data = json.load(file)
        return (
            file_data["FUEL_PRICE"],
            file_data["customers"],
            file_data["shops"]
        )


def calculate_distance(p1: list, p2: list) -> float:
    p1 = Point(*p1)
    p2 = Point(*p2)

    return math.sqrt((p2.px - p1.px) ** 2 + (p2.py - p1.py) ** 2)


def calculate_fuel_spent(
        fuel_price: float,
        car: dict,
        distance: float
) -> float:
    return car["fuel_consumption"] / 100 * distance * fuel_price


def calculate_product_cost(cart: dict, products: dict) -> int | float:
    total_cost = 0
    for product in cart:
        total_cost += cart[product] * products[product]
    return total_cost


def generate_receipt(cart: dict, products: dict) -> None:
    for product in cart:
        product_cost = cart[product] * products[product]

        # removing .0 from product_cost
        product_cost = int(product_cost) \
            if product_cost % 1 == 0 else product_cost

        print(f"{cart[product]} {product}s for {product_cost} dollars")


def print_trip_log(fuel_price: float, customer: Customer, shops: list) -> None:
    print(f"{customer.name} has {customer.money} dollars")

    shops_trip_cost = {}
    for shop in shops:
        distance = calculate_distance(customer.location, shop.location)
        trip_fuel_price = 2 * calculate_fuel_spent(
            fuel_price, customer.car, distance
        )

        product_cost = calculate_product_cost(customer.cart, shop.products)

        total_spending = round(product_cost + trip_fuel_price, 2)

        print(
            f"{customer.name}'s trip to the {shop.name} costs {total_spending}"
        )

        shops_trip_cost[shop] = {
            "products_cost": product_cost,
            "total": total_spending
        }

    closest_shop = min(
        shops_trip_cost, key=lambda shop: shops_trip_cost[shop]["total"]
    )

    total_spending = shops_trip_cost[closest_shop]["total"]

    if customer.money > total_spending:
        print(f"{customer.name} rides to {closest_shop.name}\n")

        # left str date for tests, otherwise:
        # datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
        print("Date: 04/01/2021 12:33:41")

        print(f"Thanks, {customer.name}, for your purchase!")
        print("You have bought:")
        generate_receipt(customer.cart, closest_shop.products)
        print(
            f"Total cost is "
            f"{shops_trip_cost[closest_shop]['products_cost']} dollars"
        )

        customer.money -= total_spending
        print("See you again!\n")

        print(f"{customer.name} rides home")

        print(f"{customer.name} now has {customer.money} dollars\n")

    else:
        print(
            f"{customer.name} doesn't have enough "
            f"money to make a purchase in any shop"
        )
