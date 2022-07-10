from set_theory import Set

ARROW = '\u2192'


class Rel(object):
    """A class which defines a relation, its attributes and any
    functional dependencies."""

    def __init__(self, *args):
        """Construct a relation using the list data type. The attributes
        of the relation are stored such that they are sorted and
        distinct.

        Parameters:
            args: an attribute of the relation.

        Preconditions:
            args are of immutable type.
        """
        S = []
        d = {}
        for element in args:
            S.append(element)
        for index, entry in enumerate(S):
            d[entry] = index
        R = list(d.keys())
        R.sort()
        self._Rel = R
        self._FD = []
        self._LHS_FD = []
        self._RHS_FD = []

    def num_FD(self):
        """Returns the number of functional dependencies defined.

        Returns:
            (int): the number of dependencies
        """
        return len(self._FD)

    def attributes_list(self):
        """Returns a list of attributes defined in the relation"""
        return self._Rel

    def attributes(self):
        """Returns a set of attributes defined in the relation"""
        return Set(*self._Rel)

    def add_attributes(self, set_attr):
        """Adds set of attribute(s) to relation.

        Parameters:
            set_attr(Set): A set of attributes to be added to the
            relation.
        """
        if not isinstance(set_attr, Set):
            return TypeError('attributes must be type Set')
        self._Rel.extend(set_attr.elements())

    def get_relation(self):
        """ Returns a string representation of the relation.

        Parameters:
            None

        Returns:
            (str): a string representation of the relation
        """
        return f'R{get_list_string(self._Rel)}'

    def get_dependencies(self):
        """ Returns a string reprentation of the dependencies.
        If no dependencies are present, returns
        "No non-trivial dependencies"

        Parameters:
            None

        Returns:
            (str): a string representation of the dependencies
        """
        dependencies = ''
        # Iterate through each dependency and add to string
        for index, FD in enumerate(self._FD, 1):
            if index != 1:
                dependencies += '\n'
            dependencies += f'{index}. {FD}'
        if dependencies == '':
            # No dependencies defined yet
            dependencies += 'No non-trivial dependencies'
        return dependencies

    def contains_FD(self, FD):
        """ Returns True iff the relation contains the given FD.
        Returns False otherwise.

        Parameters:
            FD(str): the functional dependency

        Returns:
            (bool): True if the given FD is already defined. False otherwise.
        """
        return FD in self._FD

    def add_FD(self, X, A):
        """Add a non-trivial functional dependency composed of
        attributes in the relation.

        Parameters:
            X(list): A list of attributes on the LHS of the FD.
            A(list): A list of attributes on the RHS of the FD.
        """
        if not isinstance(X, list):
            return TypeError('X must be a list')
        elif not isinstance(A, list):
            return TypeError('A must be a list')
        if not Set(*X).subset(self.attributes()):
            return ValueError('X must contain attributes in the relation')
        elif not Set(*A).subset(self.attributes()):
            return ValueError('A must contain attributes in the relation')
        if Set(*X).intersect(Set(*A)) != Set():
            return ValueError('FD should be non-trivial')
        X_sort = sorted(X)
        A_sort = sorted(A)
        self._LHS_FD.append(Set(*X_sort))
        self._RHS_FD.append(Set(*A_sort))
        self._FD.append(get_FD_string(X, A))

    def FD_LHS(self):
        """Return a list of all attributes on the LHS of FD's defined
        for the relation.

        Returns:
            list<set>
        """
        return self._LHS_FD

    def FD_RHS(self):
        """Return a list of all attributes on the RHS of FD's defined
        for the relation.

        Returns:
            list<set>
        """
        return self._RHS_FD

    def get_FD(self, num):
        """Returns a list of attributes involved in a functional
        dependency of the relation.

        Parameters:
            num(int>0): the number of the FD
        """
        if num <= 0 or not isinstance(num, int):
            return TypeError('num must be a positive integer')
        if num > len(self._FD):
            return ValueError('There are only ' + str(len(self._FD)) + ' FDs')
        return self._LHS_FD[num - 1].union(self._RHS_FD[num - 1])

    def copy_FD(self, other, num):
        """Copies the specified FD from other to self, if legal.

        Parameters:
            num(int>0): the number of the FD to be copied from other
        """
        if num <= 0 or not isinstance(num, int):
            return TypeError('num must be a positive integer')
        if num > len(other._FD):
            return ValueError('There are only ' + str(len(other._FD)) +
                              ' FDs in other')
        FD_LHS_other = other.FD_LHS()[num - 1].elements()
        FD_RHS_other = other.FD_RHS()[num - 1].elements()
        self.add_FD(FD_LHS_other, FD_RHS_other)

    def remove_FD(self, num):
        """Remove a functional dependency from the relation.

        Parameters:
            num(int>0): the number of the FD to remove
        """
        if num <= 0 or not isinstance(num, int):
            return TypeError('num must be a positive integer')
        if num > len(self._FD):
            return ValueError('There are only ' + str(len(self._FD)) + ' FDs')
        self._FD.pop(num - 1)
        self._LHS_FD.pop(num - 1)
        self._RHS_FD.pop(num - 1)

    def reset_FD(self):
        """Remove all functional dependencies from the relation"""
        self._FD = []
        self._LHS_FD = []
        self._RHS_FD = []

    def copy(self):
        """Create a copy of the relation and its functional
        dependencies."""
        R_copy = Rel(*self._Rel)
        R_copy._FD = self._FD.copy()
        R_copy._LHS_FD = self._LHS_FD.copy()
        R_copy._RHS_FD = self._RHS_FD.copy()
        return R_copy

    def expand_FD(self):
        """Replace all FD X -> A in self, where A consists of attributes
        A1, A2,...,An, with FD's X -> A1, X -> A2,..., X -> An."""
        R_copy = self.copy()
        R_copy.reset_FD()
        for index, FD in enumerate(self.FD_RHS()):
            LHS_attr = self.FD_LHS()[index].elements()
            for RHS_attr in FD.elements():
                R_copy.add_FD(LHS_attr, [RHS_attr])
        self._FD = R_copy._FD
        self._LHS_FD = R_copy._LHS_FD
        self._RHS_FD = R_copy._RHS_FD

    def closure(self, set_attr, ignore=None):
        """Find the closure of a set of attributes in a relation with
        option to skip a functional dependency.

        Parameters:
            set_attr(Set): A set of attributes in the relation.
            ignore(int>0): specify what FD to ignore. None by default.

        Returns:
            (Set): The closure of the set of attributes.
        """
        R_copy = self.copy()
        rel_attr = R_copy.attributes()
        set_close = set_attr.sort()
        if not isinstance(set_attr, Set):
            return TypeError('attributes must be type Set')
        elif set_close - rel_attr != Set():
            return ValueError('attributes must be a subset of relation')
        if rel_attr == set_close:
            return set_close
        if not R_copy._FD:
            return set_close
        if ignore is not None:
            if ignore <= 0 or not isinstance(ignore, int):
                return TypeError('ignore must be a positive integer')
            if ignore > len(self._FD):
                return ValueError('There are only ' + str(len(self._FD)) + ' FDs')
            R_copy.remove_FD(ignore)
        FD_skip = 0
        while FD_skip != len(R_copy._FD):
            FD_skip = 0
            for num, FD in enumerate(R_copy.FD_LHS(), 1):
                if FD.subset(set_close):
                    set_close.append(R_copy.get_FD(num))
                    R_copy.remove_FD(num)
                    FD_skip -= 1
                else:
                    FD_skip += 1
        return set_close.sort()

    def trans_FD(self, num):
        """Return True iff given FD is the result of a transitivity; i.e., for X -> Y
        there exists Z such that X -> Z and Z -> Y. Return False otherwise.

        Parameters:
            num(int>0): the number of the FD to check for transitivity.

        Returns:
            (bool): True if FD is transitive. False otherwise.
        """
        if num <= 0 or not isinstance(num, int):
            return TypeError('num must be a positive integer')
        if num > len(self._FD):
            return ValueError('There are only ' + str(len(self._FD)) + ' FDs')
        FD_LHS = self.FD_LHS()[num - 1]  # X
        FD_RHS = self.FD_RHS()[num - 1]  # Y
        if FD_RHS.subset(self.closure(FD_LHS, num)):
            return True
        return False

    def union_FD(self):
        """Return a copy of the relation with the set of FD's condensed.
        I.e., if two FD's exist in the relation with X -> A and X -> B,
        then they are replaced by X -> AB in the copy.

        Returns:
            (Rel): A copy of self but with condensed FD's
        """
        R_copy = self.copy()
        R_copy.reset_FD()
        FD_indexed = []
        for FD_1_LHS in self.FD_LHS():
            if FD_1_LHS not in FD_indexed:
                FD_indexed.append(FD_1_LHS)
                FD_RHS_tot = Set()
                for index, FD_2_LHS in enumerate(self.FD_LHS()):
                    if FD_2_LHS == FD_1_LHS:
                        FD_RHS_tot.append(self.FD_RHS()[index])
                R_copy.add_FD(FD_1_LHS.elements(), FD_RHS_tot.elements())
        return R_copy

    def infer_FD(self, set_attr):
        """Returns a relation whose attributes are in the closure of
        set_attr on self, including all non-trivial FD's from self which
        hold on the new relation.

        Parameters:
            set_attr(Set): A set of attributes in the relation.

        Returns:
            (Rel): A new relation containing all FD's inferred from
            set_attr on self, with union.
        """
        if not isinstance(set_attr, Set):
            return TypeError('attributes must be type Set')
        elif set_attr - self.attributes() != Set():
            return ValueError('attributes must be a subset of relation')
        R_new = Rel(*set_attr.elements())
        num = 0
        for FD_LHS in self.FD_LHS():  # Greatly improve the efficacy of this
            if FD_LHS.card() > num:
                num = FD_LHS.card()
        set_ps = set_attr.power_set(num + 1)[1:-1]
        for FD_LHS in set_ps:
            FD_RHS = self.closure(FD_LHS).intersect(set_attr) - FD_LHS
            if FD_RHS.card() != 0:
                R_new.add_FD(FD_LHS.elements(), FD_RHS.elements())
        return R_new

    def min_cover(self, union=None):
        """Return the minimal cover for a relation. If union = True,
        return minmal cover with union.

        Minimal cover definition:
            The set of non-trivial functional dependencies defined over
            the relation, with any redundancies removed.
        """
        R_copy = self.copy()
        R_empty = self.copy()
        R_empty.reset_FD()
        # Step 1 - simplify RHS
        R_copy.expand_FD()
        # Step 2 - simplify LHS
        for index, FD_LHS in enumerate(R_copy.FD_LHS()):
            FD_RHS = R_copy.FD_RHS()[index]
            FD_LHS_copy = FD_LHS.copy()
            if FD_LHS.card() > 1:
                FD_LHS_ele = FD_LHS.elements()
                for attr in FD_LHS_ele:
                    if FD_LHS_copy.card() > 1:  # Use intersection
                        if FD_LHS_copy.subset(self.closure(FD_LHS_copy - Set(attr))):
                            FD_LHS_copy -= Set(attr)
            R_empty.add_FD(FD_LHS_copy.elements(), FD_RHS.elements())
        # Step 3 - remove redundancies
        R_copy = R_empty.copy()
        num_FDs_rmvd = 0
        for index, FD_1_LHS in enumerate(R_empty.FD_LHS()):
            R_copy_index = index - num_FDs_rmvd + 1
            if R_copy.trans_FD(R_copy_index):
                R_copy.remove_FD(R_copy_index)
                num_FDs_rmvd += 1
            else:
                FD_1_RHS = R_empty.FD_RHS()[index]
                if FD_1_RHS.subset(R_copy.closure(FD_1_LHS, R_copy_index)):
                    R_copy.remove_FD(R_copy_index)
                    num_FDs_rmvd += 1
        if union:
            return R_copy.union_FD()
        return R_copy

    def super_key(self, set_attr):
        """Return True iff set_attr is a superkey for the relation.
        Return False otherwise.

        Parameters:
            set_attr(Set): A set of attributes in the relation.

        Superkey definition:
            A set of attributes is a superkey for the relation if
            its closure contains all attributes in the relation.
        """
        rel_attr = self.attributes()
        if not isinstance(set_attr, Set):
            return TypeError('attributes must be type Set')
        elif set_attr - rel_attr != Set():
            return ValueError('attributes must be a subset of relation')
        if self.closure(set_attr) == rel_attr:
            return True
        else:
            return False

    def keys(self):
        """Return a set of all candidate keys for the relation.

        Candidate key definition:
            A set of attributes is a candidate key for the relation if
            it is a minimal superkey.
        """
        K = []
        # Add any attributes to candidate key not on RHS of FD's
        k = self.attributes()
        for FD in self.FD_RHS():
            k -= FD
        # Check to see if any FD's have been defined
        if self.num_FD() == 0:
            # Trivial case
            return Set(k)
        # Iterate through each FD (at least one exists)
        for FD in self.FD_LHS():
            k_copy = k.sort()
            k_copy.append(FD)
            if not self.super_key(k_copy):
                k_rem = self.attributes() - self.closure(k_copy)
                if k_rem.card() == 1:
                    K.append(k_copy.union(k_rem))
                else:
                    k_minus = Set()
                    for i in range(1, 4):
                        if k_rem.card() >= i:
                            for attr in k_rem.partition(i):
                                k_temp = k_copy.union(attr)
                                if self.super_key(k_temp):
                                    K.append(k_temp.sort())
                                    if i == 1:
                                        k_minus.append(attr)
                            k_rem -= k_minus
            else:
                K.append(k_copy.sort())
        K_remove = []
        for key_1 in K:
            for key_2 in K:
                if key_2.subset(key_1) and key_2 != key_1:
                    K_remove.append(key_1)
                    break
        for key in K_remove:
            K.remove(key)
        return Set(*K)

    def prime_attr(self, attr):
        """Return True iff attr is a prime attribute for the relation.
        Return False otherwise.

        Parameters:
            attr: An attribute in the relation.

        Prime attribute definition:
            An attribute is prime iff it is a participant in a candidate
            key.
        """
        rel_attr = self.attributes()
        if not Set(attr).subset(rel_attr):
            return ValueError('must be an attribute of the relation')
        K = Set()
        for key in self.keys().elements():
            K.append(key)
        if Set(attr).subset(K):
            return True
        else:
            return False

    def key_subset(self, set_attr, reason=None):
        """Return True iff set_attr is a proper subset of a candidate
        key for the relation. Return False otherwise. If reason = True,
        return first key for which set_attr is a proper subset.

        Parameters:
            set_attr(Set): A set of attributes in the relation.
        """
        rel_attr = self.attributes()
        if not isinstance(set_attr, Set):
            return TypeError('attributes must be type Set')
        elif set_attr - rel_attr != Set():
            return ValueError('attributes must be a subset of relation')
        for key in self.keys().elements():
            if set_attr.subset(key):
                if set_attr == key:
                    return False
                if reason:
                    set_attr = get_list_string(set_attr.elements())
                    key = get_list_string(key.elements())
                    return (set_attr, key)
                return True
        return False

    def two_NF(self, reason=None):
        """Return True iff relation is in 2NF. If reason != True,
        return False. If reason = True, return first instance of
        violation.

        2NF definition:
            A given FD in the relation is in 2NF iff the LHS is not a
            proper subset of a candidate key, or its RHS is a prime
            attribute.
        """
        for index, FD_LHS in enumerate(self.FD_LHS()):
            FD_RHS = self.FD_RHS()[index]
            if self.key_subset(FD_LHS):
                for attr in FD_RHS.elements():
                    if not self.prime_attr(attr):
                        if reason:
                            return (index, *self.key_subset(FD_LHS, True), attr)
                        return False
        return True

    def two_NF_reason(self):
        """ Prints the first violation instance of 2NF.

        Requires:
            The normal form of the relation is no higher than 1NF
        """
        index, subset, key, attribute = self.two_NF(True)
        print(f'Violation: first instance at dependency {index + 1}.')
        print(
            f'Reason: {subset} is a proper subset of key {key},\n'
            f'{8 * " "}and {attribute} is not a prime attribute.'
        )

    def three_NF(self, reason=None):
        """Return True iff relation is in 3NF. If reason != True,
        return False. If reason = True, return first instance of
        violation.

        3NF definition:
            A given FD in the relation is in 3NF iff the LHS is a
            superkey, or its RHS is a prime attribute.
        """
        for index, FD_LHS in enumerate(self.FD_LHS()):
            FD_RHS = self.FD_RHS()[index]
            if not self.super_key(FD_LHS):
                for attr in FD_RHS.elements():
                    if not self.prime_attr(attr):
                        if reason:
                            FD_LHS = get_list_string(FD_LHS.elements())
                            return (index, FD_LHS, attr)
                        return False
        return True

    def three_NF_reason(self):
        """ Prints the first violation instance of 3NF.

        Requires:
            The normal form of the relation is no higher than 2NF
        """
        index, subset, attribute = self.three_NF(True)
        print(f'Violation: first instance at dependency {index + 1}.')
        print(
            f'Reason: {subset} is not a superkey, and {attribute} '
            'is not a prime attribute.'
        )

    def BCNF(self, reason=None):
        """Return True iff relation is in BCNF. If reason != True,
        return False. If reason = True, return first instance of
        violation.

        BCNF definition:
            A given FD in the relation is in BCNF iff the LHS is a
            superkey.
        """
        for index, FD in enumerate(self.FD_LHS()):
            if not self.super_key(FD):
                if reason:
                    FD = get_list_string(FD.elements())
                    return (index, FD)
                return False
        return True

    def BCNF_reason(self):
        """ Prints the first violation instance of BCNF.

        Requires:
            The normal form of the relation is no higher than 3NF
        """
        index, subset = self.BCNF(True)
        print(f'Violation: first instance at dependency {index + 1}.')
        print(f'Reason: {subset} is not a superkey.')

    def highest_NF(self):
        """Return the highest normal form of the relation.

        Returns:
            (str): Either 1NF, 2NF, 3NF or BCNF

        Assumption:
            The relation is always at least in 1NF; i.e, no attributes
            are multi-valued or nested.
        """
        if not self.two_NF():
            return '1NF'
        elif not self.three_NF():
            return '2NF'
        elif not self.BCNF():
            return '3NF'
        return 'BCNF'

    def three_NF_decomp(self):
        """Decomposes the relation into 3NF iff its highest normal form
        is 2NF or lower.

        3NF decomposition:
            computes minimal cover and then generates
            relations for each FD, eliminating redundancies.
            Adds additional relation for key(s) if not referenced.
        """
        # Check to see whether self is in 3NF
        if self.three_NF():
            return 'Relation is already in 3NF.'
        # Compute minimal cover with union
        R_copy = self.min_cover(True)
        R_decomp = []
        R_empty = Rel()
        # Create a relation for each FD in min cover
        for index, FD_LHS in enumerate(R_copy.FD_LHS(), 1):
            R_empty_copy = R_empty.copy()
            R_empty_copy.add_attributes(R_copy.get_FD(index))
            R_empty_copy.copy_FD(R_copy, index)
            R_decomp.append(R_empty_copy)
        R_decomp_min = R_decomp.copy()
        R_indexed = []
        # Remove redundant relations
        for rel_1 in R_decomp:
            rel_1_attr = rel_1.attributes()
            if rel_1 not in R_indexed:
                R_indexed.append(rel_1)
                for rel_2 in R_decomp:
                    if rel_2 != rel_1:
                        if rel_2.attributes().subset(rel_1_attr):
                            R_indexed.append(rel_2)
                            R_decomp_index = R_decomp_min.index(rel_1)
                            R_decomp_min[R_decomp_index].copy_FD(rel_2, 1)
                            R_decomp_min.remove(rel_2)
        # Add relation for keys (if applicable)
        three_NF_string = ''
        for key in self.keys().elements():
            for rel in R_decomp_min:
                if key.subset(rel.attributes()):
                    for index, rel in enumerate(R_decomp_min, 1):
                        if index != 1:
                            three_NF_string += '\n'
                        three_NF_string += f'Relation {index} : {rel}\n'
                    return three_NF_string
        R_decomp_min.append(Rel(*self.keys().elements()[0].elements()))
        for index, rel in enumerate(R_decomp_min, 1):
            if index != 1:
                three_NF_string += '\n'
            three_NF_string += f'Relation {index} : {rel}\n'
        return three_NF_string

    def BCNF_decomp(self):
        """Decomposes the relation into BCNF iff its highest normal form
        is 3NF or lower.

        BCNF decomposition:
            iterates through each FD in relation R from top to bottom
            until first instance of BCNF violation is found.
            Decomposes FD in violation X -> Y into two relations:
            R1(X&Y) and R2(R - Y).
            If any other non-trivial FD's from R hold on R2 which are
            not in BCNF, then R2 is decomposed again as above.
            Repeat until all relations are in BCNF.
        """
        # Check to see whether self is in BCNF
        if self.BCNF():
            return 'Relation is already in BCNF.'
        R_temp = []
        R_BCNF = []
        R_not_BCNF = []
        # Decompose into BCNF using top-down approach
        for FD_LHS in self.FD_LHS():
            if not self.super_key(FD_LHS):
                rel_1 = self.infer_FD(self.closure(FD_LHS))
                rel_2_attr = self.attributes() - rel_1.attributes()
                rel_2 = self.infer_FD(rel_2_attr.union(FD_LHS))
                break
        R_temp.extend([rel_1, rel_2])
        for rel in R_temp:
            if rel.BCNF():
                R_BCNF.append(rel)
            else:
                R_not_BCNF.append(rel)
        R_temp = []
        for rel in R_not_BCNF:
            for FD_LHS in rel.FD_LHS():
                if not rel.super_key(FD_LHS):
                    rel_1 = rel.infer_FD(rel.closure(FD_LHS))
                    rel_2_attr = rel.attributes() - rel_1.attributes()
                    rel_2 = rel.infer_FD(rel_2_attr.union(FD_LHS))
                    break
            R_temp.extend([rel_1, rel_2])
            for rel in R_temp:
                if rel.BCNF():
                    R_BCNF.append(rel)
                else:
                    R_not_BCNF.append(rel)
            R_temp = []
        for i, rel in enumerate(R_BCNF):
            R_BCNF.pop(i)
            R_BCNF.insert(i, rel.min_cover(True))
        R_join = self.copy()
        R_join.reset_FD()
        for rel in R_BCNF:
            num_FDs = len(rel.FD_LHS())
            for i in range(1, num_FDs + 1):
                R_join.copy_FD(rel, i)
        BCNF_string = ''
        for index, rel in enumerate(R_BCNF, 1):
            if index != 1:
                BCNF_string += '\n'
            BCNF_string += f'Relation {index} : {rel}\n'
        BCNF_string += '\nFunctional Dependencies lost: \n'
        num_FD_lost = 0
        R_min = self.min_cover(True)
        for FD_LHS in R_min.FD_LHS():
            attr_lost = R_min.closure(FD_LHS) - R_join.closure(FD_LHS)
            if attr_lost != Set():
                num_FD_lost += 1
                FD_string = get_FD_string(FD_LHS.elements(), attr_lost.elements())
                BCNF_string += f'{num_FD_lost}. {FD_string}\n'
        if num_FD_lost == 0:
            BCNF_string += 'None\n'
        return BCNF_string

    def __repr__(self):
        """The human-readable representation of the relation and its
        non-trivial functional dependencies."""
        return f'{self.get_relation()}\n\n{self.get_dependencies()}'


def get_FD_string(X, A):
    """ Returns the string representation of the FD with
    left-hand side X and right-hand side A.

    Parameters:
        X(list): A list of attributes on the LHS of the FD.
        A(list): A list of attributes on the RHS of the FD.

    Returns:
        (str): the string representation of the FD
    """
    X_sort = sorted(X)
    A_sort = sorted(A)
    return f'{get_list_string(X_sort)} {ARROW} {get_list_string(A_sort)}'


def get_list_string(elements):
    """ Returns a string representation of the list which
    is pretty.

    Parameters:
        elements(list): the list of elements

    Returns:
        (str): a formated string representation of the list
    """
    string = '['
    for index, element in enumerate(elements):
        if index != 0:
            string += ', '
        string += element
    string += ']'
    return string
