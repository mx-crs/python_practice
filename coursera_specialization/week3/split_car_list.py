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

    def __init__(self, passenger_seats_count=0, car_type=None,
                 photo_file_name=None, brand=None, carrying=None):
        super().__init__(car_type, photo_file_name, brand, carrying)
        self.passenger_seats_count = passenger_seats_count

    @classmethod
    def create_machine(cls, car_str):
        return cls(passenger_seats_count=int(car_str[2]), car_type=car_str[0],
                   photo_file_name=car_str[3], brand=car_str[1], carrying=float(car_str[5]))

class Truck(BaseCar):

    """Truck class"""

    def __init__(self, whl, car_type=None, photo_file_name=None, brand=None, carrying=None):
        super().__init__(car_type, photo_file_name, brand, carrying)
        self.body_width = whl[0]
        self.body_height = whl[1]
        self.body_length = whl[2]

    def get_body_volume(self):
        return self.body_width * self.body_length * self.body_height

    @classmethod
    def create_machine(cls, car_str):
        whl = [.0, .0, .0]
        t_whl = car_str[4].split('x')
        if len(t_whl) == 3:
            whl[0] = float(t_whl[0])
            whl[1] = float(t_whl[1])
            whl[2] = float(t_whl[2])
        return cls(whl, car_type=car_str[0], photo_file_name=car_str[3],
                   brand=car_str[1], carrying=float(car_str[5]))

class SpecMachine(BaseCar):

    def __init__(self, extra=0.0, car_type=None, photo_file_name=None, brand=None, carrying=None):
        super().__init__(car_type, photo_file_name, brand, carrying)
        self.extra = extra

    @classmethod
    def create_machine(cls, car_str):
        return cls(extra=car_str[6], car_type=car_str[0], photo_file_name=car_str[3],
                   brand=car_str[1], carrying=float(car_str[5]))

def get_car_list(csv_file_name):
    car_list = []
    with open(csv_file_name) as fd:
        reader = csv.reader(fd, delimiter=';')
        next(reader)
        for row in reader:
            if len(row) == 7:
                if row[0] == 'car':
                    car_list.append(Car.create_machine(row))
                elif row[0] == 'truck':
                    car_list.append(Truck.create_machine(row))
                elif row[0] == 'spec_machine':
                    car_list.append(SpecMachine.create_machine(row))
    return car_list

"""
    argv[1] - csv file with list of car of 3 different types
"""

if __name__ == "__main__":
    print(get_car_list(sys.argv[1]))