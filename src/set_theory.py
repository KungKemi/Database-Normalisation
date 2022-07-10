__author__ = "Alexander Johnson"
__email__ = "work.a.a.johnson@gmail.com"
__date__ = "20/06/2021"


class Set(object):
    """A class which implements sets and basic set theory operations."""

    def __init__(self, *args):
        """Construct a set using the list data type. Set contains only
        distinct elements.

        Parameters:
            args: a hashable element of the set.
        """
        S = []
        for element in args:
            S.append(element)
        S_dupes = []
        S_copy = S.copy()
        for entry in S:
            S_count = S.count(entry)
            if S_count > 1:
                if S_dupes.count(entry) - S_count < -1:
                    S_dupes.append(entry)
                    S_copy.remove(entry)
        self._Set = S_copy

    def elements(self):
        """(list) Returns a list of elements in the set"""
        return self._Set

    def card(self):
        """(int) Return the cardinality of the set"""
        return len(self._Set)

    def copy(self):
        """Create a copy of the set"""
        S_copy = Set(*self.elements().copy())
        return S_copy

    def sort(self):
        """Sort elements in the set"""
        S = self._Set.copy()
        S.sort()
        return Set(*S)

    def union(self, other):
        """Return a set 'S' such that for every 'x' in set 1, and every
        'y' in set 2, then 'x' in 'S' and 'y' in 'S'

        Returns:
            (Set) A set containing all elements in both sets.
        """
        S = []
        for element in self._Set + other._Set:
            S.append(element)
        return Set(*S)

    def append(self, other):
        """Analogous to union except self is overwritten by the set
        formed through union."""
        self._Set = self.union(other)._Set

    def intersect(self, other):
        """Return a set 'S' such that for every 'x' in set 1 and set 2,
        then 'x' in 'S'.

        Returns:
            (Set) A set containing all common elements in both sets.
        """
        S = []
        for x in self._Set:
            for y in other._Set:
                if x == y:
                    S.append(x)
                    break
        return Set(*S)

    def __sub__(self, other):
        """Return a set 'S' such that for every 'x' in set 1 that is not
        in set 2, then 'x' in 'S'.

        Returns:
            (Set): A set formed from the set difference of set 1 and
            set 2.
        """
        S = []
        I = self.intersect(other)
        for entry in self.elements():
            if not Set(entry).subset(I):
                S.append(entry)
        return Set(*S)

    def subset(self, other):
        """(bool) Return True if set 1 is a subset of set 2.
        False otherwise.
        """
        I = self.intersect(other)
        if I.card() == self.card():
            return True
        else:
            return False

    def __eq__(self, other):
        """Return true iff set 1 and set 2 contain the same elements"""
        if self.subset(other) and other.subset(self):
            return True
        return False

    def partition(self, num):
        """Partitions the set into all unique subsets which can be
        generated using 'num' elements.
        If self has n elements and the subsets have r elements, then
        there will be a total of n!/(r!(n-r)!) unique subsets in the
        partition.

        Parameters:
            num(int): the number of elements in the subset

        Returns:
            list<set>: a list of partitions
        """
        if num < 0 or not isinstance(num, int):
            return TypeError('num must be a non-negtive integer')
        elif num > self.card():
            return ValueError('num cannot exceed cardinality of set')
        if num == 0:
            return [Set()]
        part_set = []
        ele = self.elements()
        if num == 1:
            for i in ele:
                part_set.append(Set(i))
            return part_set
        indexes = []
        for i in range(num):
            indexes.append(i)
        while indexes[0] != self.card() - num + 1:
            part = []
            for i in indexes:
                part.append(ele[i])
            part_set.append(Set(*part))
            if indexes[-1] % (self.card() - 1) == 0:
                for i, j in enumerate(indexes[1:], 1):
                    if j % (self.card() + i - num) == 0:
                        indexes[i - 1] += 1
                        for k in range(len(indexes[i:])):
                            indexes[i + k] = indexes[i - 1] + k + 1
                        break
            else:
                indexes[-1] += 1
        return part_set

    def power_set(self, num=None):
        """Computes the power set of self; i.e., a list containing all
        unique subsets which can be generated from self.
        If self has n elements, then the power set contains 2**n unique
        subsets.

        Parameters:
            num(int>=0): the size cut-off for subsets to include
            in the power set. None by default.
        
        Returns:
            list<set>: the power set of self
        """
        if num is not None:
            if num < 0 or not isinstance(num, int):
                return TypeError('num must be a non-negtive integer')
        power_set = []
        for i in range(self.card() + 1):
            power_set.extend(self.partition(i))
            if i == num:
                break
        return power_set

    def __repr__(self):
        """The string representation of the set."""
        return 'Set' + str(self._Set)
