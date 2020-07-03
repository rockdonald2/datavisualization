student_data = [
    {'name': 'Bob', 'id': 0, 'scores':[68, 75, 56, 81]},
    {'name': 'Alice', 'id': 1, 'scores':[75, 90, 64, 88]},
    {'name': 'Carol', 'id': 2, 'scores':[59, 74, 71, 68]},
    {'name': 'Dan', 'id': 3, 'scores':[64, 58, 53, 62]},
]

def process_student_data(data, pass_threshold=60, merit_threshold=75):
    """ egy egyszerű statisztikát hoz létre a tanulók adataiból """
    # a fenti doc-string automatikusan hozzárendelődik a __doc__ attribútumhoz.

    for sdata in data:
        av = sum(sdata['scores']) / float(len(sdata['scores']))
        sdata['average'] = av

        if av > merit_threshold:
            sdata['assessment'] = 'passed with merit'
        elif av > pass_threshold:
            sdata['assessment'] = 'passed'
        else:
            sdata['assessment'] = 'failed'

        print("{}'s (id: {}) final asessment is {}.".format(sdata['name'], sdata['id'], sdata['assessment'].upper()))


if __name__ == '__main__':
    process_student_data(student_data)

# bármikor amikor a Python interpreterje értelmez egy forrásállományt,
# két dolgoz tesz:
#   - beállít néhány speciális változót, mint pl. a 'name',
#   - lefuttatja a fájlban található összes utasítást.
# a name speciális változó értéke akkor lesz 'main', ha elsődleges forrásként futtassuk.

#########################################

import logging

logger = logging.getLogger(__name__)

logger.debug('Some useful debugging output')
logger.info('Some general information')
logger.warning('Some warning')

#########################################

foo = {'first_key': 1, 'second_key': 2}

for item in foo:
    print(item)

# Ebben az esetben nem a dict itemet fogja kiírna, hanem annak kulcsát.

for item in foo.items():
    print(item)

# Ebben az esetben már a dict itemet fogja kiírni key-value páronként, tuple típusban. 

######################################### 

class Citizen(object):
    def __init__(self, name, country):
        self.name = name
        self.country = country

    def print_details(self):
        print('Citizen {} from {}.'.format(self.name, self.country))

c = Citizen('Lukács Zs.', 'Hungary')
c.print_details()

######################################### 

class Winner(Citizen):
    def __init__(self, name, country, category, year):
        super(Winner, self).__init__(name, country)
        self.category = category
        self.year = year

    def print_details(self):
        print('Nobel winner {} from {}, category {}, year {}'.format(self.name, self.country, self.category, self.year))

w = Winner('Albert E.', 'Switzerland', 'Physics', 1921)
w.print_details()

#########################################

names = ['Alice', 'Bob', 'Carol']

for i, n in enumerate(names):
    print('{}: {}'.format(i, n))

#########################################

def fibonacci(n):
    x, y = 0, 1

    for i in range(n):
        print(x)
        x, y = y, x + y

fibonacci(4)

#########################################

from collections import Counter

items = ['F', 'B', 'B', 'F', 'A', 'C', 'D', 'D']

cntr = Counter(items)
# a Counter függvény megszámolja az elemek gyakoriságát

print(cntr)