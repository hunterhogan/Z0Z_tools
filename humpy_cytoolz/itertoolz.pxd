cdef class accumulate:
    cdef object binop
    cdef object iter_seq
    cdef object result
    cdef object initial


cpdef dict groupby(object key, object seq)


cdef class interleave:
    cdef object iters
    cdef list newiters


cpdef object isiterable(object x)


cpdef object take(Py_ssize_t n, object seq)


cpdef object tail(Py_ssize_t n, object seq)


cpdef object drop(Py_ssize_t n, object seq)


cpdef object take_nth(Py_ssize_t n, object seq)


cpdef object first(object seq)


cpdef object second(object seq)


cpdef object nth(Py_ssize_t n, object seq)


cpdef object last(object seq)


cpdef object rest(object seq)


cpdef object get(object ind, object seq, object default=*)


cpdef object cons(object el, object seq)


cpdef object mapcat(object func, object seqs)


cpdef dict frequencies(object seq)


cpdef dict reduceby(object key, object binop, object seq, object init=*)


cpdef object sliding_window(Py_ssize_t n, object seq)


cpdef object partition(Py_ssize_t n, object seq, object pad=*)


cpdef object partition_all(Py_ssize_t n, object seq)


cdef class _pluck_index:
    cdef object ind
    cdef object iterseqs


cdef class _pluck_index_default:
    cdef object ind
    cdef object iterseqs
    cdef object default


cdef class _pluck_list:
    cdef list ind
    cdef object iterseqs
    cdef Py_ssize_t n


cdef class _pluck_list_default:
    cdef list ind
    cdef object iterseqs
    cdef object default
    cdef Py_ssize_t n


cpdef object pluck(object ind, object seqs, object default=*)


cdef class _getter_index:
    cdef object ind


cdef class _getter_list:
    cdef list ind
    cdef Py_ssize_t n


cdef class _getter_null:
    pass


cpdef object getter(object index)


cpdef object join(object leftkey, object leftseq,
                  object rightkey, object rightseq,
                  object left_default=*,
                  object right_default=*)

cdef class _join:
    cdef dict d
    cdef list matches
    cdef set seen_keys
    cdef object leftseq
    cdef object rightseq
    cdef object _rightkey
    cdef object right
    cdef object left_default
    cdef object right_default
    cdef object keys
    cdef Py_ssize_t N
    cdef Py_ssize_t i
    cdef bint is_rightseq_exhausted

    cdef object rightkey(self)


cdef class _inner_join(_join):
    pass

cdef class _right_outer_join(_join):
    pass

cdef class _left_outer_join(_join):
    pass

cdef class _outer_join(_join):
    pass


cdef class _inner_join_key(_inner_join):
    pass

cdef class _inner_join_index(_inner_join):
    pass

cdef class _inner_join_indices(_inner_join):
    pass

cdef class _right_outer_join_key(_right_outer_join):
    pass

cdef class _right_outer_join_index(_right_outer_join):
    pass

cdef class _right_outer_join_indices(_right_outer_join):
    pass

cdef class _left_outer_join_key(_left_outer_join):
    pass

cdef class _left_outer_join_index(_left_outer_join):
    pass

cdef class _left_outer_join_indices(_left_outer_join):
    pass

cdef class _outer_join_key(_outer_join):
    pass

cdef class _outer_join_index(_outer_join):
    pass

cdef class _outer_join_indices(_outer_join):
    pass


cdef class _diff_key:
    cdef Py_ssize_t N
    cdef object iters
    cdef object key


cdef class _diff_identity:
    cdef Py_ssize_t N
    cdef object iters


cdef object c_diff(object seqs, object default=*, object key=*)


cpdef object topk(Py_ssize_t k, object seq, object key=*)


cpdef object peek(object seq)


cpdef object peekn(Py_ssize_t n, object seq)


cdef class random_sample:
    cdef object iter_seq
    cdef object prob
    cdef object random_func
