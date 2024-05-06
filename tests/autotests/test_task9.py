# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import itertools
from copy import deepcopy
import pytest
from grammars_constants import REGEXP_CFG, GRAMMARS, GRAMMARS_DIFFERENT, EBNF_GRAMMARS
from helper import generate_rnd_start_and_final
from rpq_template_test import rpq_cfpq_test, different_grammars_test
from fixtures import graph

# Fix import statements in try block to run tests
try:
    from project.task2 import graph_to_nfa, regex_to_dfa
    from project.task3 import FiniteAutomaton
    from project.task4 import reachability_with_constraints
    from project.task7 import cfpq_with_matrix
    from project.task6 import cfpq_with_hellings
    from project.task8 import cfpq_with_tensor, cfg_to_rsm, ebnf_to_rsm
    from project.task9 import cfpq_with_gll
except ImportError:
    pytestmark = pytest.mark.skip("Task 9 is not ready to test!")


class TestReachabilityGllAlgorithm:
    @pytest.mark.parametrize("regex_str, cfg_list", REGEXP_CFG.items())
    def test_rpq_cfpq_gll(self, graph, regex_str, cfg_list) -> None:
        rpq_cfpq_test(graph, regex_str, cfg_list, cfpq_with_gll)

    @pytest.mark.parametrize("eq_grammars", GRAMMARS)
    def test_different_grammars(self, graph, eq_grammars):
        different_grammars_test(graph, eq_grammars, cfpq_with_gll)

    @pytest.mark.parametrize("grammar", GRAMMARS_DIFFERENT)
    def test_hellings_matrix_tensor(self, graph, grammar):
        start_nodes, final_nodes = generate_rnd_start_and_final(graph)
        hellings = cfpq_with_hellings(
            deepcopy(grammar), deepcopy(graph), start_nodes, final_nodes
        )
        matrix = cfpq_with_matrix(
            deepcopy(grammar), deepcopy(graph), start_nodes, final_nodes
        )
        tensor = cfpq_with_tensor(
            cfg_to_rsm(deepcopy(grammar)), deepcopy(graph), start_nodes, final_nodes
        )
        gll = cfpq_with_gll(
            cfg_to_rsm(deepcopy(grammar)), deepcopy(graph), start_nodes, final_nodes
        )
        assert (hellings == matrix) and (matrix == tensor) and (tensor == gll)

    @pytest.mark.parametrize(
        "cfg_grammar, ebnf_grammar", (zip(GRAMMARS_DIFFERENT, EBNF_GRAMMARS))
    )
    def test_ebnf_cfg(self, graph, cfg_grammar, ebnf_grammar):
        start_nodes, final_nodes = generate_rnd_start_and_final(graph)
        cfg_cfpq = cfpq_with_gll(
            cfg_to_rsm(cfg_grammar), deepcopy(graph), start_nodes, final_nodes
        )
        ebnf_cfpq = cfpq_with_gll(
            ebnf_to_rsm(ebnf_grammar), deepcopy(graph), start_nodes, final_nodes
        )
        assert ebnf_cfpq == cfg_cfpq

    @pytest.mark.parametrize("regex_str, cfg_list", REGEXP_CFG.items())
    def test_cfpq_gll(self, graph, regex_str, cfg_list):
        start_nodes, final_nodes = generate_rnd_start_and_final(graph)
        eq_cfpqs = [
            cfpq_with_gll(
                cfg_to_rsm(deepcopy(cf_gram)), deepcopy(graph), start_nodes, final_nodes
            )
            for cf_gram in cfg_list
        ]
        eq_cfpqs.append(
            cfpq_with_gll(
                ebnf_to_rsm(f"S -> {regex_str}"),
                deepcopy(graph),
                start_nodes,
                final_nodes,
            )
        )
        for a, b in itertools.combinations(eq_cfpqs, 2):
            assert a == b