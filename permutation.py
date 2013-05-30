class permutation (object):
    """
    A class to convert cycles into permutation functions.
    
    The perm object is to be called as a function, and implements the
    symmetric group of n elements.
    """
    
    def __init__ (self, *cycles):
        size = max(max(cycle) for cycle in cycles)
        self._lookup = [0] * size
        for i in xrange(1, size + 1):
            result = i # Assume there is no change
            for cycle in reversed(cycles):
                try:
                    result = cycle[cycle.index(result) - len(cycle) + 1]
                except ValueError:
                    pass
            self._lookup[i - 1] = result
    
    def __call__ (self, x):
        """Get the result of the permutation.
        
        Examples
        ========
        
        >>> a = perm((1, 2, 4))
        >>> a(3)
        3
        >>> a(4)
        1
        >>> a(5)
        Traceback (most recent call last):
            ...
        IndexError: 5 not in permutation. Must be between 1 and 4.
        """
        try:
            return self._lookup[x - 1]
        except IndexError:
            message = '{} not in permutation. Must be between 1 and {}.'
            raise IndexError(message.format(x, len(self)))
    
    def __eq__ (self, other):
        return str(self) == str(other)
    
    def __ne__ (self, other):
        return not (self == other)
    
    def __mul__ (self, other):
        """Compose two permutations.
        
        Example
        =======
        
            >>> a, b = perm((1, 2), (3,)), perm((2, 3))
            >>> a * b
            perm((1, 2, 3))
        """
        return perm(*(self._getcycles() + other._getcycles()))
    
    def __pow__ (self, idx):
        """Raise the permutation to an integer power.
        
        Example
        =======
        
        >>> a = perm((1, 2, 3))
        >>> a ** 3
        perm((3,))
        """
        return perm(*(self._getcycles() * idx))
    
    def __str__ (self):
        """Return a string of the permutation in cycle notation.
        
        Example
        =======
        
        >>> a = perm((1, 2), (5, 4, 3, 7))
        >>> str(a)
        '(1 2)(3 7 5 4)'
        """
        cycles = []
        for cycle in self._getcycles():
            cycles.append(' '.join(str(x) for x in cycle).join('()'))
        return ''.join(cycles)
    
    def __repr__ (self):
        """Return the code needed to create the permutation.
        
        Example
        =======
        
        >>> a = perm((1, 2), (5, 4, 3, 7))
        >>> repr(a)
        'perm((1, 2), (3, 7, 5, 4))'
        """
        argument = ', '.join(str(tuple(cycle)) for cycle in self._getcycles())
        return 'perm({})'.format(argument)
    
    def __len__ (self):
        """The length of the permutation (n in Sn).
        
        Examples
        ========
        
        >>> a = perm((1, 2), (4, 3, 6))
        >>> len(a)
        6
        """
        return len(self._lookup)
    
    def _getcycles (self, simplify=True):
        """Get a list of cycles in the permutation.
        
        Examples
        ========
        
        >>> a = perm((1, 2), (5, 4), (3, 6), (7,), (9,))
        >>> a._getcycles()
        [[1, 2], [3, 6], [4, 5], [9]]
        >>> a._getcycles(simplify=False)
        [[1, 2], [3, 6], [4, 5], [7], [8], [9]]
        """
        # Keep track of the numbers we haven't touched yet. I chose to
        # look at what we haven't touched, because it makes the while
        # condition nicer to look at.
        not_done = [True] * len(self)
        cycles = []
        while any(not_done):
            # We start with the lowest number that hasn't yet been
            # listed, and record that we've touched it. We then loop
            # through the permutation until we get back to the original
            # number, at which point we close that cycle and begin a
            # new one.
            start = not_done.index(True) + 1
            cycle = [start]
            not_done[start - 1] = False
            next_element = self(start)
            while next_element != start:
                cycle.append(next_element)
                not_done[next_element - 1] = False
                next_element = self(next_element)
            # We have the option of removing the one-cycles from the
            # list, except possibly for the last one, if it is needed
            # to determine the length of the permutation.
            #
            # For example,
            # The identity permutation in S3 can be written as (3),
            # but cannot be simplified further.
            if not simplify or len(cycle) > 1 or cycle[0] == len(self):
                cycles.append(cycle)
        return cycles
    
    @property
    def order (self):
        """Compute the order of the permutation.
        
        Examples
        ========
        
        >>> a = perm((5,))
        >>> a.order
        1
        >>> b = perm((1, 3), (2, 5), (7, 4, 6))
        >>> b.order
        6
        """
        order = 1
        result = self * self
        while result != self:
            result *= self
            order += 1
        return order
    
    @property
    def sgn (self):
        """Return the parity of the permutation.
        
        The sign of a permutation is -1 for an odd permutation, and +1
        for an even permutation.
        
        Examples
        ========
        
        >>> a = perm((4,))
        >>> a.sgn
        1
        >>> b = perm((1, 3))
        >>> b.sgn
        -1
        >>> (a**2).sgn
        1
        >>> (a * b).sgn
        -1
        """
        even_cycles = filter(lambda x: not (len(x) % 2), self._getcycles())
        return -2 * (len(even_cycles) % 2) + 1

if __name__ == '__main__':
    import doctest
    doctest.testmod()