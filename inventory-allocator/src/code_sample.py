import unittest

class Warehouse:
    def __init__(self, name='', inventory={}):
        self.name = name
        self.inventory = inventory



# input: 
#  - map<item: amount>
#  - sorted list of warehouse objects
# output: list of map<name: map<item: amount>>
class InventoryAllocator:
    def get_cheapest(self, orders, warehouses):
        cheapest = []
        if not warehouses: return cheapest
        for item, needed in orders.items():
            unchange = needed # check if all warehouses are empty.
            while needed:
                for w in warehouses:
                    if item in w.inventory:
                        if needed < w.inventory[item]:
                            cheapest.append({w.name: {item: needed}})
                            w.inventory[item] -= needed
                            needed = 0 
                            break
                        else:
                            if w.inventory[item]:
                                cheapest.append({w.name: {item: w.inventory[item]}})
                            needed -= w.inventory[item]
                            del(w.inventory[item])
                if needed == unchange: break
        return cheapest




class TestInventoryAllocator(unittest.TestCase):
    def test_get_cheapest1(self):
        orders = {'apple':1}
        inv = {'apple':1}
        wh = Warehouse('owd', inv)
        IA = InventoryAllocator()
        self.assertEqual(IA.get_cheapest(orders, [wh]), [{'owd': {'apple': 1}}])


    def test_get_cheapest2(self):
        orders = {'apple':1}
        inv = {'apple': 0}
        wh = Warehouse('owd', inv)
        IA = InventoryAllocator()
        self.assertEqual(IA.get_cheapest(orders, [wh]), [])


    def test_get_cheapest3(self):
        orders = {'apple':10}
        inv1 = {'apple': 5}
        inv2= {'apple': 5}
        owd = Warehouse('owd', inv1)
        dm= Warehouse('dm', inv2)
        IA = InventoryAllocator()
        self.assertEqual(IA.get_cheapest(orders, [owd, dm]), [{'owd': {'apple': 5}}, {'dm':{'apple':5}}])


    def test_get_cheapest4(self):
        orders = {'apple': 5, 'banana': 5, 'orange': 5}
        inv1 = {'apple':5, 'orange':10}
        inv2 = {'banana':5, 'orange':10}
        owd = Warehouse('owd', inv1)
        dm = Warehouse('dm', inv2)
        wh = [owd, dm]
        IA = InventoryAllocator()
        self.assertEqual(IA.get_cheapest(orders, wh), [{'owd': {'apple': 5}}, {'dm': {'banana': 5}}, {'owd': {'orange': 5}}])


    def test_empty_input(self):
        orders1 = {'apple': 5, 'banana': 5, 'orange': 5}
        wh1 = []
        orders2 = {}
        inv1 = {'apple':5, 'orange':10}
        inv2 = {'banana':5, 'orange':10}
        owd = Warehouse('owd', inv1)
        dm = Warehouse('dm', inv2)
        wh2 = [owd, dm]
        IA = InventoryAllocator()
        self.assertEqual(IA.get_cheapest(orders1, wh1), [])
        self.assertEqual(IA.get_cheapest(orders2, wh2), [])



if __name__ == '__main__':
    unittest.main()



# Script for running the tests: 
# python3 -m unittest -v code_sample.py