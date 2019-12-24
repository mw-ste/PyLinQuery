#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:51:21 2019

@author: michi
"""

import inspect
from types import FunctionType

# In[]
class Enumerable:
    _generator = None
    _values    = None
    
    
    # In[]
    def __init__(self, values):
        if Enumerable._is_generator_type(values):
            self._generator = values
        elif Enumerable._is_list_type(values):
            self._generator = Enumerable._create_generator(values)
        else:
            error  = "Values need to be of type generator function, list or tuple, but was: "
            error += str(type(values))
            raise TypeError(error)


    # In[]
    def to_list(self):
        if self._values == None:
            self._values = list(self._generator())
        return self._values


    # In[]
    def where(self, method):
        Enumerable._check_is_function(method)
        def generate():
            for element in self._get_values():
                if(method(element)):
                    yield element
        return Enumerable(generate)


    # In[]
    def select(self, method):
        Enumerable._check_is_function(method)
        def generate():
            for element in self._get_values():
                yield method(element)
        return Enumerable(generate)


    # In[]
    def for_each(self, method):
        Enumerable._check_is_function(method)
        for element in self._get_values():
            method(element)


    # In[]
    def all(self, method):
        Enumerable._check_is_function(method)
        return all([method(element) for element in self._get_values()])


    # In[]
    def any(self, method):
        Enumerable._check_is_function(method)
        return any([method(element) for element in self._get_values()])


    # In[]
    def sort(self, method, descending = False):
        Enumerable._check_is_function(method)
        values = sorted(self._get_values(), key = method, reverse = descending)
        return Enumerable(values)


    # In[]
    def group_by(self, method):
        Enumerable._check_is_function(method)
        grouped = {}
        for element in self._get_values():
            key = method(element)
            if not key in grouped.keys():
                grouped[key] = []
            grouped[key].append(element)
        return grouped


    # In[]
    def _get_values(self):
        return self._generator()


    # In[]
    def _check_is_function(method):
        if not Enumerable._is_function_type(method):
            error  = "Method need to be of type function, but was: "
            error += str(type(method))
            raise TypeError(error)


    # In[]
    def _create_generator(elements):
        def generate():
            for element in elements:
                yield element
        return generate


    # In[]
    def _is_function_type(element):
        generator_types = [FunctionType]
        return Enumerable._check_type(element, generator_types)


    # In[]
    def _is_generator_type(element):
        return inspect.isgeneratorfunction(element)

    
    # In[]    
    def _is_list_type(element):
        list_types = [list, tuple]
        return Enumerable._check_type(element, list_types)

    
    # In[]    
    def _check_type(element, types):
        is_type_instance = [isinstance(element, current_type) for current_type in types]
        is_any_element_of_type = sum(is_type_instance) > 0
        return is_any_element_of_type