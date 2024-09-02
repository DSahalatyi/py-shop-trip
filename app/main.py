from app.shop_trip_functions import get_data_from_file, print_trip_log
from app.customers.customer import Customer
from app.shops.shop import Shop


def shop_trip() -> None:

    fuel_price, customers, shops = get_data_from_file()
    customers = [Customer(**customer_info) for customer_info in customers]
    shops = [Shop(**shop_info) for shop_info in shops]

    for customer in customers:
        print_trip_log(fuel_price, customer, shops)
