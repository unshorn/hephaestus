from copy import deepcopy

from src.ir import ast
from src.analysis.call_analysis import CallAnalysis, CNode
from tests.resources import (program1, program4, program5, program8, program9,
        program10)


def str2node(string):
    segs = tuple(string.split("/"))
    return CNode(segs)


def assert_nodes(nodes, expected_nodes):
    assert len(nodes) == len(expected_nodes)
    assert (nodes - expected_nodes) == set()


def assert_nodes_len(nodes, length):
    assert len(nodes) == length


# Simple function call from method to method declared in the same class
def test_program1():
    ca = CallAnalysis(program1.program)
    cg, calls = ca.result()

    foo = str2node("global/A/foo")
    bar = str2node("global/A/bar")
    buz = str2node("global/A/buz")
    spam = str2node("global/A/spam")

    assert_nodes(cg[foo], {bar})
    assert_nodes_len(calls[foo], 0)
    assert_nodes(cg[bar], set())
    assert_nodes_len(calls[bar], 1)
    assert_nodes(cg[buz], set())
    assert_nodes_len(calls[buz], 0)
    assert_nodes(cg[spam], set())
    assert_nodes_len(calls[spam], 0)


# Inner method call
def test_program4():
    ca = CallAnalysis(program4.program)
    cg, calls = ca.result()

    foo = str2node("global/A/foo")
    bar = str2node("global/A/foo/bar")

    assert_nodes(cg[foo], {bar})
    assert_nodes_len(calls[foo], 0)
    assert_nodes(cg[bar], set())
    assert_nodes_len(calls[bar], 1)


# Multiple method calls
def test_program5():
    ca = CallAnalysis(program5.program)
    cg, calls = ca.result()


    foo = str2node("global/A/foo")
    bar = str2node("global/A/bar")
    baz = str2node("global/A/bar/baz")
    quz = str2node("global/A/quz")

    assert_nodes(cg[foo], set())
    assert_nodes_len(calls[foo], 1)
    assert_nodes(cg[bar], {foo, baz, quz})
    assert_nodes_len(calls[bar], 0)
    assert_nodes(cg[baz], set())
    assert_nodes_len(calls[baz], 1)
    assert_nodes(cg[quz], set())
    assert_nodes_len(calls[quz], 1)


# There is a call from foo to x.length() which is not a user defined function.
# Currently, we skip such calls.
def test_program8():
    ca = CallAnalysis(program8.program)
    cg, calls = ca.result()

    foo = str2node("global/A/foo")

    assert_nodes(cg[foo], set())
    assert_nodes_len(calls[foo], 0)


# Simple function call
def test_program9():
    ca = CallAnalysis(program9.program)
    cg, calls = ca.result()

    foo = str2node("global/foo")
    bar = str2node("global/bar")

    assert_nodes(cg[foo], set())
    assert_nodes_len(calls[foo], 1)
    assert_nodes(cg[bar], {foo})
    assert_nodes_len(calls[bar], 0)


# Variable receivers
def test_program10():
    ca = CallAnalysis(program10.program)
    cg, calls = ca.result()

    first_foo = str2node("global/First/foo")
    second_foo = str2node("global/Second/foo")
    third_foo = str2node("global/Third/foo")
    global_foo = str2node("global/foo")
    global_bar = str2node("global/bar")

    assert_nodes(cg[first_foo], set())
    assert_nodes_len(calls[first_foo], 2)
    assert_nodes(cg[second_foo], set())
    assert_nodes_len(calls[second_foo], 1)
    assert_nodes(cg[third_foo], {first_foo})
    assert_nodes_len(calls[third_foo], 0)
    assert_nodes(cg[global_foo], {first_foo})
    assert_nodes_len(calls[global_foo], 0)
    assert_nodes(cg[global_bar], {second_foo})
    assert_nodes_len(calls[global_bar], 0)
