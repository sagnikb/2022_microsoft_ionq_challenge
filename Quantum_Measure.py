from qiskit import QuantumCircuit, transpile
from qiskit import Aer


class QuantumBackend():
    def __init__(self, level: int) -> None:
        """Initiates the quantum backend

        Args:
            level (int): level (currently unused, set to 0)
        """
        self.simulator = Aer.get_backend('statevector_simulator')
        self.playerCircuit = QuantumCircuit(1, 1)
        self.scoreCircuit = QuantumCircuit(level+2, level+2)
        self.quantumGateDict = {
            'H': self.playerCircuit.h,
            'X': self.playerCircuit.x,
            'Y': self.playerCircuit.y,
            'Z': self.playerCircuit.z,
            'S': self.playerCircuit.s
        }

    def execute_measurement(self, qGates: list[str], measurement: str) -> int:
        """Given a list of gates and a measurement basis, starts a qubit from
        state zero, acts the gates on it, measures it in the given basis and
        returns the result

        Args:
            qGates (list(str)): list of gates, consisting of ['X', 'Y', 'Z',
            'H', 'S']
            measurement (str): measurement basis, one of ['X', 'Y', 'Z']

        Raises:
            NotImplementedError: if given gate or measurement is not
            implemented

        Returns:
            int: measurement result
        """
        # Reset the circuit so we can update it fresh in case of a second
        # encounter
        self.playerCircuit.reset(0)

        for gate in qGates:
            if gate in self.quantumGateDict:
                self.quantumGateDict[gate](0)
            else:
                raise NotImplementedError
        # Verify which measurement basis will we use according to the parameter
        # sent (type of enemy)
        if measurement == "Z":
            self.playerCircuit.measure(0, 0)
        elif measurement == "Y":
            self.playerCircuit.sdg(0)
            self.playerCircuit.h(0)
            self.playerCircuit.measure(0, 0)
        elif measurement == 'X':
            self.playerCircuit.h(0)
            self.playerCircuit.measure(0, 0)
        else:
            raise NotImplementedError

        # Compilation and optimization of the circuit
        compiled_circuit = transpile(self.playerCircuit, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=1)
        result = job.result()
        counts = result.get_counts(self.playerCircuit)
        if '0' in counts:
            return 0
        else:
            return 1

    # Function for the score circuit. If you generate a maximally entalgled
    # state, you win.
    def Score_circuit(self, gate, score, scorelist):
        cnot_count = 0
        for i in range(2):
            self.scoreCircuit.reset(i)
        if gate == 'H':
            score += 1
        else:
            if 'H' in scorelist:
                score += 1
        for gates in scorelist:
            if gates == 'H':
                self.scoreCircuit.h(0)
            else:
                self.scoreCircuit.cnot(cnot_count, cnot_count + 1)  # BUG
                cnot_count += 1
        return score, self.scoreCircuit
