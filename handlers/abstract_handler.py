# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class Interface(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_client(cls):
        pass

    @classmethod
    @abstractmethod
    def start_main(cls):
        pass

    # utilities
    def get_alternative_name(self, delimeter, name):
        split_list = name.split(delimeter)
        if split_list[-1].isdecimal():
            split_list[-1] = str(int(split_list[-1]) + 1)
            return delimeter.join(split_list)
        else:
            return name + delimeter + '1'