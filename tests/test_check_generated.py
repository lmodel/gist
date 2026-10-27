"""Unit tests for the RDF comparison in scripts/check_generated_current.py."""
from rdflib import BNode, Graph, Literal, Namespace

import check_generated_current as C

EX = Namespace("https://example.org/")


def _shape(*values, labels=("a", "b", "c")) -> Graph:
    """A node shape with one property shape per value, each under its own blank node."""
    g = Graph()
    for label, value in zip(labels, values):
        prop, path = BNode(label), BNode(label + "_path")
        g.add((EX.PersonShape, EX.property, prop))
        g.add((prop, EX.path, path))
        g.add((path, EX.name, Literal(value)))
    return g


class TestTreeSignature:
    def test_relabelled_blank_nodes_are_the_same(self):
        assert C.same_graph(_shape("x", "y"), _shape("y", "x", labels=("q", "r")))

    def test_a_literal_deep_in_a_tree_differs(self):
        assert not C.same_graph(_shape("x", "y"), _shape("x", "z"))

    def test_two_equal_trees_are_counted_twice(self):
        assert not C.same_graph(_shape("x", "x"), _shape("x", "y"))
        assert C.same_graph(_shape("x", "x"), _shape("x", "x", labels=("q", "r")))

    def test_a_shared_blank_node_falls_back_to_rdflib(self):
        g = _shape("x")
        g.add((EX.OtherShape, EX.property, BNode("a")))
        assert C.tree_signature(g) is None
        assert C.same_graph(g, g)

    def test_a_cycle_has_no_signature(self):
        g = Graph()
        g.add((BNode("a"), EX.next, BNode("b")))
        g.add((BNode("b"), EX.next, BNode("a")))
        assert C.tree_signature(g) is None
