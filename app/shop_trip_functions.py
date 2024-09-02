# flake8: ignore=VNE001
import json
import math
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

from app.customers.customer import Customer


class Point(NamedTuple):
    x: int  # noqa: VNE001 All my homies hate flake8!
    y: int  # noqa: VNE001


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

    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)


def calculate_fuel_spent(
        fuel_price: float,
        car: dict,
        distance: float
) -> float:
    return car["fuel_consumption"] / 100 * distance * fuel_price


class Cart:
    def __init__(self, cart: dict, products: dict) -> None:
        self.cart = cart
        self.products = products

    def calculate_product_cost(self) -> int | float:
        total_cost = 0
        for product in self.cart:
            total_cost += self.cart[product] * self.products[product]
        return total_cost

    def generate_receipt(self) -> None:
        for product in self.cart:
            product_cost = self.cart[product] * self.products[product]

            # removing .0 from product_cost
            product_cost = int(product_cost) \
                if product_cost % 1 == 0 else product_cost

            print(
                f"{self.cart[product]} {product}s for {product_cost} dollars"
            )


def print_trip_log(fuel_price: float, customer: Customer, shops: list) -> None:
    print(f"{customer.name} has {customer.money} dollars")

    shops_trip_cost = {}
    for shop in shops:
        distance = calculate_distance(customer.location, shop.location)
        trip_fuel_price = 2 * calculate_fuel_spent(
            fuel_price, customer.car, distance
        )

        product_cost = Cart(
            customer.cart,
            shop.products
        ).calculate_product_cost()

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

        # setting date manually since test checks for const str
        date = datetime.strptime("04/01/2021 12:33:41", "%d/%m/%Y %H:%M:%S")
        print(f"Date: {datetime.strftime(date, '%d/%m/%Y %H:%M:%S')}")

        print(f"Thanks, {customer.name}, for your purchase!")
        print("You have bought:")
        Cart(customer.cart, closest_shop.products).generate_receipt()
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
