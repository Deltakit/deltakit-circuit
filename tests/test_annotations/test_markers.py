# (c) Copyright Riverlane 2020-2026. All rights reserved.

import deltakit_stim as stim
import pytest

import deltakit_circuit as sp


@pytest.mark.parametrize(
    ("marker", "expected"),
    [
        (sp.MarkX(1), "#!pragma MARKX(0) 1"),
        (sp.MarkY(2, index=4), "#!pragma MARKY(4) 2"),
        (sp.MarkZ(3, index=9), "#!pragma MARKZ(9) 3"),
    ],
)
def test_crumble_marker_string(marker: sp.Pragma, expected: str):
    assert str(marker) == expected


@pytest.mark.parametrize("index", [-1, 10, 1.5, True])
def test_crumble_marker_rejects_invalid_index(index):
    with pytest.raises(ValueError, match="index must be an integer from 0 to 9"):
        sp.MarkX(1, index=index)


def test_marker_is_a_circuit_layer_and_stim_omits_only_the_pragma():
    circuit = sp.Circuit(
        [
            sp.GateLayer(sp.gates.H(1)),
            sp.MarkX(1),
            sp.GateLayer(sp.gates.MZ(1)),
        ]
    )
    assert circuit.as_crumble_string() == "H 1\nTICK\n#!pragma MARKX(0) 1\nM 1"
    assert circuit.as_stim_circuit() == stim.Circuit("H 1\nTICK\nM 1")
    assert sp.MarkX(1) in circuit.layers


def test_marker_qubit_is_included_in_mapping_and_can_be_transformed():
    qubit = sp.Qubit(sp.Coordinate(1, 3))
    circuit = sp.Circuit([sp.MarkZ(qubit, index=2), sp.GateLayer(sp.gates.X(qubit))])
    mapping = {qubit: 7}
    assert set(circuit.qubits) == {qubit}
    assert circuit.as_crumble_string(mapping) == (
        "QUBIT_COORDS(1, 3) 7\n#!pragma MARKZ(2) 7\nX 7"
    )
    circuit.transform_qubits({sp.Coordinate(1, 3): sp.Coordinate(2, 4)})
    assert sp.MarkZ(sp.Coordinate(2, 4), index=2) in circuit.layers
    assert sp.Qubit(sp.Coordinate(2, 4)) in circuit.qubits


def test_marker_in_repeat_block_keeps_its_timestep_and_braces():
    repeated = sp.Circuit(
        [sp.GateLayer(sp.gates.X(0)), sp.MarkY(0, index=1)], iterations=2
    )
    circuit = sp.Circuit([sp.GateLayer(sp.gates.H(0)), repeated])
    expected = "H 0\nTICK\nREPEAT 2 {\n    X 0\n    #!pragma MARKY(1) 0\n    TICK\n}"
    assert circuit.as_crumble_string() == expected
    assert stim.Circuit(expected) == circuit.as_stim_circuit()


def test_multiple_markers_preserve_order_and_separate_indices():
    circuit = sp.Circuit(
        [
            sp.MarkX(0, index=0),
            sp.MarkZ(2, index=1),
            sp.GateLayer(sp.gates.CX(0, 2)),
        ]
    )
    assert circuit.as_crumble_string() == (
        "#!pragma MARKX(0) 0\n#!pragma MARKZ(1) 2\nCX 0 2"
    )


def test_circuit_with_markers_compares_and_flattens_like_other_annotations():
    circuit = sp.Circuit(sp.Circuit([sp.MarkX(0)], iterations=2))
    assert circuit.approx_equals(sp.Circuit(sp.Circuit([sp.MarkX(0)], iterations=2)))
    assert circuit.flatten() == sp.Circuit([sp.MarkX(0), sp.MarkX(0)])
    assert not circuit.approx_equals(
        sp.Circuit(sp.Circuit([sp.MarkY(0)], iterations=2))
    )
