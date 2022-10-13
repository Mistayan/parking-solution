# -*- coding: utf-8 -*-
"""
Created by: Mistayan
Project: pythonProject4
IDE: PyCharm
Creation-date: 10/12/22
"""

import logging
from collections import Counter
from typing import Final

import coloredlogs

ACCEPTS: Final = {"moto": 1, "car": 1, "van": 3}  # vehicle: used_spaces
coloredlogs.install(logging.DEBUG)


class ParkingSolution:
    def __init__(self, lines, spots, accepts=None) -> None:
        self._accepts = accepts
        self._logger = logging.getLogger(self.__class__.__name__)
        self._park = [[None for _ in range(spots)] for _ in range(lines)]
        self._counter = Counter()
        self._total = lines * spots
        self._update()

    def get_used(self) -> int:
        return self._used

    def _update(self):
        # updating self.counter beforehand
        update_counter = Counter()
        for line in self._park:
            update_counter.update(line)
        self._counter = update_counter
        total_used = 0
        for elem in self._counter:
            total_used += self._counter[elem] if elem else 0
        self._used = total_used

    def get_total(self):
        return self._total

    def show(self):
        for line in self._park:
            print(line)
        print()

    def count(self, vehicle) -> int:
        if not self._valid_input(vehicle):
            return 0
        vehicle_size = self._accepts.get(vehicle)
        return self._counter[vehicle] // vehicle_size

    def allow_vehicles(self, new_vehicles: dict[str, int]):
        if not type(new_vehicles) is dict:
            raise ValueError("Only new_vehicles dict {'vehicle': size, ...}")
        if self._accepts:
            self._accepts.update(new_vehicles)
        else:  # first time
            self._accepts = new_vehicles

    def _valid_input(self, elem):
        if not self._accepts or not type(self._accepts) is dict:
            raise NotImplementedError("parking does not accept any vehicle.\n"
                                      "have you _used (set/add)_accepts({'allowed': size, ...}) ?")
        return elem in self._accepts.keys()

    def _add(self, vehicle) -> bool:
        ui = f"{vehicle} entered parking"
        vehicle_size: int = self._accepts.get(vehicle)
        for x in range(len(self._park)):
            for y in range(len(self._park[x])):
                if self._park[x][y]:
                    continue  # Spot taken, skip tests

                # On an empty slot, ensure there is enough space for current vehicle:
                test_space = self._park[x][y: y + vehicle_size]
                if Counter(test_space)[None] == vehicle_size:
                    for i in range(vehicle_size):
                        self._park[x][y + i] = vehicle
                    ui += f", parked at line: {x + 1} / spot {y + 1}"
                    ui += f" to spot : {y + vehicle_size}" if vehicle_size > 1 else ""
                    self._logger.info(ui)
                    return True
        self._logger.info(ui)
        return False  # No 'open' and/or 'large enough' spot found

    def _sub(self, vehicle) -> None:
        vehicle_size: int = self._accepts.get(vehicle)
        for x in range(len(self._park)):
            for y in range(len(self._park[x])):
                if not self._park[x][y] == vehicle:
                    continue
                for i in range(vehicle_size):
                    self._park[x][y + i] = None
                self._logger.info(f"{vehicle} left the park, freeing {vehicle_size} spaces.")
                return

    def __add__(self, elem: str | list[str]) -> bool:
        if type(elem) is list:  # Recursive on list of vehicles
            return False not in [self.__add__(one_elem) for one_elem in elem]

        if not self._valid_input(elem):
            self._logger.error(f"{elem}: Not a Valid vehicle")
            return False

        vehicle_size = self._accepts[elem]
        if not self.get_remaining() >= vehicle_size or not self._add(elem):
            self._logger.warning(f"{elem} could NOT park. NOT ENOUGH SPACE.")
            return False

        # vehicle is valid, there is still space in parking, found a spot according to it's size.
        self._logger.debug(f"{[_ for _ in self._park]}")
        self._update()
        return True

    def __sub__(self, elem: str | list[str]) -> None:
        if type(elem) is list:  # Recursive on list of vehicles
            [self.__sub__(one_elem) for one_elem in elem]
        if self._valid_input(elem):
            self._sub(elem)
            self._update()

    def get_remaining(self):
        return self.get_total() - self.get_used()

