# (c) Copyright Riverlane 2020-2026. All rights reserved.
"""Crumble Pauli marker annotations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar, Generic

import deltakit_stim as stim

from deltakit_circuit._qubit_identifiers import Qubit, T, U
from deltakit_circuit._qubit_mapping import default_qubit_mapping
from deltakit_circuit.gates import PauliBasis


class Pragma(Generic[T]):
    """A Crumble Pauli marker at a qubit and an indexed Pauli product.

    Parameters
    ----------
    qubit : Qubit[T] | T
        The qubit on which to place the marker.
    index : int
        The Crumble Pauli product index, from 0 to 9.
    """

    basis: ClassVar[PauliBasis]
    stim_string: ClassVar[str]

    def __init__(self, qubit: Qubit[T] | T, index: int = 0):
        if (
            isinstance(index, bool)
            or not isinstance(index, int)
            or index not in range(10)
        ):
            msg = "Crumble marker index must be an integer from 0 to 9."
            raise ValueError(msg)
        self._qubit = qubit if isinstance(qubit, Qubit) else Qubit(qubit)
        self._index = index

    @property
    def qubit(self) -> Qubit[T]:
        """The qubit marked by this annotation."""
        return self._qubit

    @property
    def qubits(self) -> tuple[Qubit[T]]:
        """The qubits referenced by this annotation."""
        return (self._qubit,)

    @property
    def index(self) -> int:
        """The index of the marked Pauli product."""
        return self._index

    def transform_qubits(self, id_mapping: Mapping[T, U]):
        """Apply an identifier mapping to the marked qubit."""
        if (new_id := id_mapping.get(self._qubit.unique_identifier)) is not None:
            self._qubit = Qubit(new_id)

    def as_crumble_string(
        self, qubit_mapping: Mapping[Qubit[T], int] | None = None
    ) -> str:
        """Render a marker using Crumble's Stim comment syntax."""
        if qubit_mapping is None:
            qubit_mapping = default_qubit_mapping(self.qubits)
        return f"#!pragma {self.stim_string}({self.index}) {qubit_mapping[self.qubit]}"

    def permute_stim_circuit(
        self,
        _stim_circuit: stim.Circuit,
        _qubit_mapping: Mapping[Qubit[T], int] | None = None,
    ):
        """Omit the Crumble-only annotation from a pure Stim circuit."""

    def __str__(self) -> str:
        return self.as_crumble_string()

    def __repr__(self) -> str:
        return f"{self.stim_string}({self.qubit}, index={self.index})"

    def __eq__(self, other: object) -> bool:
        return (
            type(self) is type(other)
            and isinstance(other, Pragma)
            and self.qubit == other.qubit
            and self.index == other.index
        )

    def __hash__(self) -> int:
        return hash((type(self), self.qubit, self.index))


class MarkX(Pragma[T]):
    """Mark an X Pauli for propagation in Crumble."""

    basis: ClassVar[PauliBasis] = PauliBasis.X
    stim_string: ClassVar[str] = f"MARK{basis.value}"


class MarkY(Pragma[T]):
    """Mark a Y Pauli for propagation in Crumble."""

    basis: ClassVar[PauliBasis] = PauliBasis.Y
    stim_string: ClassVar[str] = f"MARK{basis.value}"


class MarkZ(Pragma[T]):
    """Mark a Z Pauli for propagation in Crumble."""

    basis: ClassVar[PauliBasis] = PauliBasis.Z
    stim_string: ClassVar[str] = f"MARK{basis.value}"
