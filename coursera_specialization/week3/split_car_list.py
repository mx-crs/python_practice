import csv
import os
import sys


class BaseCar:

    """Base class with common methods and attributes"""

    def __init__(self, car_type, photo_file_name, brand, carrying):
        self.car_type = car_type
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]

class Car(BaseCar):

    """Car class"""

    def __init__(self, passenger_seats_count=0):
        self.passenger_seats_count = passenger_seats_count

class Truck(BaseCar):

    """Truck class"""

    def __init__(self, body_width=0.0, body_height=0.0, body_length=0.0):
        self.body_width = body_width
        self.body_height = body_height
        self.body_length = body_length

    def get_body_volume(self):
        return self.body_width * self.body_length * self.body_height

class SpecMachine(BaseCar):

    def __init__(self, extra=0.0):
        self.extra = extra

def create_car(car_str):
    car = Car()
    car.car_type = car_str[0]
    car.brand = car_str[1]
    car.photo_file_name = car_str[3]
    car.carrying = float(car_str[5])
    return car

def create_truck(car_str):
    truck = Truck()
    whl = car_str[4].split('x')
    truck.car_type = car_str[0]
    truck.brand = car_str[1]
    truck.photo_file_name = car_str[3]
    truck.carrying = float(car_str[5])
    truck.body_length = 0.0 if len(whl) != 3 else float(whl[0])
    truck.body_width = 0.0 if len(whl) != 3 else float(whl[1])
    truck.body_height = 0.0 if len(whl) != 3 else float(whl[2])
    return truck

def create_spec_machine(car_str):
    spec = SpecMachine()
    spec.car_type = car_str[0]
    spec.brand = car_str[1]
    spec.photo_file_name = car_str[3]
    spec.carrying = car_str[5]
    spec.extra = car_str[6]
    return spec

def get_car_list(csv_file_name):
    car_list = []
    with open(csv_file_name) as fd:
        reader = csv.reader(fd, delimiter=';')
        next(reader)
        for row in reader:
            if len(row) == 7:
                if row[0] == 'car':
                    car_list.append(create_car(row))
                elif row[0] == 'truck':
                    car_list.append(create_truck(row))
                elif row[0] == 'spec_machine':
                    car_list.append(create_spec_machine(row))
    return car_list

"""
    argv[1] - csv file with list of car of 3 different types
"""

if __name__ == "__main__":
    print(get_car_list(sys.argv[1]))