import qiskit
import numpy as np
from qiskit.providers.aer import QasmSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit import Aer
import time

listaTeste = ["Hadamard", "PauliZ", "RX"]


def initialize(level):
    #Connections for the Azure Quantum simulator
    provider = AzureQuantumProvider(
    resource_id="/subscriptions/b1d7f7f8-743f-458e-b3a0-3e09734d716d/resourceGroups/aq-hackathons/providers/Microsoft.Quantum/Workspaces/aq-hackathon-01", 
    location="East US"
    )
    #print([backend.name() for backend in provider.backends()])
    simulator = provider.get_backend("ionq.simulator")
    # simulator = Aer.get_backend('statevector_simulator')
    
    #Game circuit generations, both for the player circuit and the score circuit
    scoreCircuit = QuantumCircuit(level+2, level+2)
    playerCircuit = QuantumCircuit(1,1)
    
    #Dictionary with the relation of gates present in game and the command, used for verification of which have been collected at execute measurement
    quantumGateDict= {"Hadamard": playerCircuit.h , "PauliX": playerCircuit.x,
                "PauliY": playerCircuit.y, "PauliZ": playerCircuit.z,}

    quantumRotDict= {"RX": playerCircuit.rx, "RY":playerCircuit.ry, "RZ":playerCircuit.rz}

    return scoreCircuit, playerCircuit, quantumGateDict, quantumRotDict, simulator

def execute_measurement(qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, measurement):
    #Reset the circuit so we can update it fresh in case of a second encounter.
    playerCircuit.reset(0)
    
    #Verification of each of the collected gates to be applied to the circuit
    for gate in qGates:
        if gate in quantumGateDict:
            quantumGateDict[gate](0)
        if gate in quantumRotDict:
            quantumRotDict[gate](np.pi/2, 0)
            
    #Verify which measurement basis will we use according to the parameter sent (type of enemy)
    if measurement == "Z":
        playerCircuit.measure(0, 0)
    elif measurement == "Y":
        playerCircuit.h(0)
        playerCircuit.sdg(0)
        playerCircuit.h(0)
        playerCircuit.measure(0,0)
    else:
        playerCircuit.h(0)
        playerCircuit.h(0)
        playerCircuit.measure(0, 0)
    
    #Compilation and optimization of the circuit
    compiled_circuit = transpile(playerCircuit, simulator)
    job = simulator.run(compiled_circuit, shots = 1)
    result = job.result()
    counts = result.get_counts(playerCircuit)
    if '0' in counts:
        return 0
    else:
        return 1
    if counts["0"] >= counts["1"]:
        return 0
    else:
        return 1

#Function for the score circuit. If you generate a maximally entalgled state, you win.
def Score_circuit(gate, scoreCircuit, score, scorelist):
    cnot_count = 0
    for i in range(2):
        scoreCircuit.reset(i)
    if gate == "H":
        score += 1
    else:
        if "H" in scorelist:
            score += 1
    for gates in scorelist:
        if gates == "H":
            scoreCircuit.h(0)
        else:
            scoreCircuit.cnot(cnot_count, cnot_count+ 1)
            cnot_count += 1
    return score, scoreCircuit                         

#scoreCircuit, playerCircuit, quantumGateDict, quantumRotDict, simulator = initialize()

#execute_measurement(listaTeste)
#playerCircuit.draw(output = 'mpl')
