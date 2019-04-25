# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 10:22:06 2019

@author: Michi
"""

from enumerable import Enumerable
import unittest


# In[]
def generate():
    for i in range(8):
        yield i


# In[]
class Dummy:
    A = None
    B = None
    
    def __init__(self, A = 0, B = 0):
        self.A = A
        self.B = B


# In[]
class EnumerableTests(unittest.TestCase):

    # In[]
    def test_when_create_enumerable_with_list_then_create_valid_enumerable(self):
        self.assertIsNotNone(Enumerable([1, 2, 3]))
        self.assertIsNotNone(Enumerable(["a", "b", "c"]))


    # In[]
    def test_when_create_enumerable_with_tuple_then_create_valid_enumerable(self):
        self.assertIsNotNone(Enumerable((1, 2, 3)))
        self.assertIsNotNone(Enumerable(("a", "b", "c")))


    # In[]
    def test_when_create_enumerable_with_generator_function_then_create_valid_enumerable(self):
        self.assertIsNotNone(Enumerable(generate))


    # In[]
    def test_when_create_enumerable_with_generator_then_raise_type_error(self):
        with self.assertRaises(TypeError):
            Enumerable(generate())


    # In[]
    def test_when_create_enumerable_with_dictionary_then_raise_type_error(self):
        with self.assertRaises(TypeError):
            Enumerable({"1" : 1, "2" : 2, "3" : 3})


    # In[]
    def test_when_create_enumerable_with_string_then_raise_type_error(self):
        with self.assertRaises(TypeError):
            Enumerable("test")


    # In[]
    def test_when_run_where_then_return_correct_values(self):
        enumerable = Enumerable(generate)
        
        where_enumerable = enumerable.where(lambda x: x > 2)
        self.assertIsInstance(where_enumerable, Enumerable)
        
        values = where_enumerable.to_list()
        self.assertSequenceEqual(values, [3, 4, 5, 6, 7])


    # In[]
    def test_when_run_several_where_in_sequence_then_return_correct_values(self):
        enumerable = Enumerable(generate)
        
        where_enumerable = enumerable.where(lambda x: x > 2).where(lambda x: x < 6)
        self.assertIsInstance(where_enumerable, Enumerable)
        
        values = where_enumerable.to_list()
        self.assertSequenceEqual(values, [3, 4, 5])


    # In[]
    def test_when_run_where_then_enumerate_only_after_to_list(self):
        sequence = []
        
        def less_than_5(x):
            w = x < 5
            sequence.append(5)
            return w
        
        enumerable = Enumerable(generate).where(less_than_5).where(less_than_5)
        self.assertTrue(len(sequence) == 0)
        
        enumerable.to_list()
        self.assertTrue(len(sequence) > 0)


    # In[]
    def test_when_run_to_list_several_times_then_enumerate_only_once(self):
        sequence = []
        
        def less_than_5(x):
            w = x < 5
            sequence.append(5)
            return w
        
        enumerable = Enumerable(generate).where(less_than_5)
        
        enumerable.to_list()
        counter = len(sequence)
        
        enumerable.to_list()
        self.assertEqual(counter, len(sequence))


    # In[]
    def test_when_run_several_where_in_sequence_then_run_interleaved(self):
        sequence = []
        
        def less_than_5(x):
            w = x < 5
            sequence.append(5)
            return w
        
        def greater_than_2(x):
            w = x > 2
            sequence.append(2)
            return w
        
        enumerable = Enumerable(generate)
        values = enumerable.where(greater_than_2).where(less_than_5).to_list()
        
        self.assertSequenceEqual(values, [3, 4])
        self.assertSequenceEqual(sequence, [2, 2, 2, 2, 5, 2, 5, 2, 5, 2, 5, 2, 5])


    # In[]
    def test_when_create_several_enumerables_from_same_enumerable_then_return_correct_values(self):
        enumerable_1 = Enumerable(generate).where(lambda x: x > 0)
        
        enumerable_2 = enumerable_1.where(lambda x: x > 4)
        enumerable_3 = enumerable_1.where(lambda x: x < 4)
        
        self.assertSequenceEqual(enumerable_3.to_list(), [1, 2, 3])
        self.assertSequenceEqual(enumerable_2.to_list(), [5, 6, 7])


    # In[]
    def test_when_run_select_then_return_correct_values(self):
        dummies = [Dummy(1, 2), Dummy(2, 4), Dummy(3, 6), Dummy(4, 8)]
        
        values = Enumerable(dummies).select(lambda x: x.A).to_list()
        self.assertSequenceEqual(values, [1, 2, 3, 4])
        
        values = Enumerable(dummies).select(lambda x: x.B).to_list()
        self.assertSequenceEqual(values, [2, 4, 6, 8])


    # In[]
    def test_when_run_where_and_select_in_sequence_then_return_correct_values(self):
        dummies = [Dummy(1, 2), Dummy(2, 4), Dummy(3, 6), Dummy(4, 8)]
        
        values = Enumerable(dummies).where(lambda x: x.A < 3).select(lambda x: x.B).to_list()
        self.assertSequenceEqual(values, [2, 4])  


    # In[]
    def test_when_run_for_each_then_execute_method_on_each_element(self):
        dummies = [Dummy(1, 2), Dummy(2, 4), Dummy(3, 6), Dummy(4, 8)]
        values = []
        Enumerable(dummies).for_each(lambda x: values.append(x.B))
        self.assertSequenceEqual(values, [2, 4, 6, 8])


    # In[]
    def test_when_run_all_and_all_are_true_then_return_true(self):
        dummies = [Dummy(1, 2), Dummy(2, 4), Dummy(3, 6), Dummy(4, 8)]
        all_true = Enumerable(dummies).all(lambda x: x.B > 1)
        self.assertTrue(all_true)


    # In[]
    def test_when_run_all_and_not_all_are_true_then_return_false(self):
        dummies = [Dummy(1, 2), Dummy(2, 4), Dummy(3, 6), Dummy(4, 8)]
        all_true = Enumerable(dummies).all(lambda x: x.B > 2)
        self.assertFalse(all_true)


    # In[]
    def test_when_run_any_and_at_least_one_is_true_then_return_true(self):
        dummies = [Dummy(1, 2), Dummy(2, 4), Dummy(3, 6), Dummy(4, 8)]
        all_true = Enumerable(dummies).any(lambda x: x.B > 7)
        self.assertTrue(all_true)


    # In[]
    def test_when_run_any_and_none_is_true_then_return_false(self):
        dummies = [Dummy(1, 2), Dummy(2, 4), Dummy(3, 6), Dummy(4, 8)]
        all_true = Enumerable(dummies).any(lambda x: x.B > 8)
        self.assertFalse(all_true)


    # In[]
    def test_when_sort_then_return_values_sorted_ascending(self):
        a = Dummy(1, 8)
        b = Dummy(2, 6)
        c = Dummy(3, 4)
        d = Dummy(4, 2)
        dummies = [a, b, c, d]
        values = Enumerable(dummies).sort(lambda x: x.B)
        self.assertSequenceEqual(values.to_list(), [d, c, b, a])


    # In[]
    def test_when_sort_descending_then_return_values_sorted_descending(self):
        a = Dummy(1, 8)
        b = Dummy(2, 6)
        c = Dummy(3, 4)
        d = Dummy(4, 2)
        dummies = [a, b, c, d]
        values = Enumerable(dummies).sort(lambda x: x.B, descending = True)
        self.assertSequenceEqual(values.to_list(), [a, b, c, d])


    # In[]
    def test_when_group_by_member_then_return_correct_dictionary(self):
        a = Dummy(1, "a")
        b = Dummy(1, "b")
        c = Dummy(2, "c")
        d = Dummy(2, "d")
        e = Dummy(3, "e")
        dummies = [a, b, c, d, e]
        values = Enumerable(dummies).group_by(lambda x: x.A)
        self.assertIsInstance(values, dict)
        self.assertDictEqual(values, {1 : [a, b], 2 : [c, d], 3 : [e]})


# In[]
if __name__ == '__main__':
    unittest.main()
    