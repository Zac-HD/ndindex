from operator import index

class NDIndex:
    """
    Represents an index into an nd-array (i.e., a numpy array)
    """
    def __new__(cls, *args):
        obj = object.__new__(cls)
        obj.args = args
        return obj

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(map(str, self.args))})"

    def __hash__(self):
        return hash(self.args)

class Slice(NDIndex):
    """
    Represents a slice on an axis of an nd-array
    """
    def __new__(cls, start, stop=None, step=None):
        # Canonicalize
        if step is None:
            step = 1
        if step == 0:
            raise ValueError("slice step cannot be zero")

        if start is not None:
            start = index(start)
        if stop is not None:
            stop = index(stop)
        step = index(step)

        if start is not None and stop is not None:
            r = range(start, stop, step)
            # We can reuse some of the logic built-in to range(), but we have to
            # be careful. range() only acts like a slice if the start <= stop (or
            # visa-versa for negative step). Otherwise, slices are different
            # because of wrap-around behavior. For example, range(-3, 1)
            # represents [-3, -2, -1, 0] whereas slice(-3, 1) represents the slice
            # of elements from the third to last to the first, which is either an
            # empty slice or a single element slice depending on the shape of the
            # axis.
            if len(r) == 0 and (
                    (step > 0 and start <= stop) or
                    (step < 0 and stop <= start)):
                start, stop, step = 0, 0, 1
            if len(r) == 1:
                return Integer(r[0])

        args = (start, stop, step)

        return super().__new__(cls, *args)

    @property
    def raw(self):
        return slice(*self.args)

class Integer(NDIndex):
    """
    Represents an integer index on an axis of an nd-array
    """
    def __new__(cls, idx):
        idx = index(idx)

        return super().__new__(cls, idx)

    @property
    def raw (self):
        return self.args[0]
