# PAQ-MAN - PAC-MAN with a quantum flavor

We have utilized the simple game of Pacman to illustrate and understand the complex concepts of Quantum Mechanics. We made this for the **IonQ + Microsoft Joint Challenge @ MIT iQuHACK 2022** [iQuHACK 2022](https://www.iquise.mit.edu/iQuHACK/2022-01-28)!

## Dependencies

* Pygame (tested with 2.0.3)
* Qiskit Aer (tested with 0.10.2)

## How to run

Just run main.py after installing dependencies! Move Pacman using the arrow keys.

## Game rules

* The objective is to score as many points as possible, while avoiding dying
* Pacman has an associated quantum state, and the ghosts perform measurements in X, Y or Z basis. If the measurement result is a 0, Pacman dies. If it's a one, Pacman starts in the post-measurement state. The measurement results and post measurement states are obtained by running the relevant code on <s>a real IonQ quantum computer, accessed via Azure!</s> on a Qiskit Aer `statevector_simulator'.
* There are gates strewn throughout the maze. If Pacman meets an X, Y or Z gate, the gate acts on the Pacman's state, and Pacman then is in the state obtained after the gate acts. 
* The gates and ghosts disappear after interacting with Pacman.
* The score is increased whenever Pacman encounters an H gate followed by a CNOT gate, which allows Pacman to create Bell pairs.

# Screenshots 

![Main gameplay window](/screenshots/gameplay_1.png)

![Score increment after Pacman swallows an H followed by CN gate](/screenshots/gameplay_2.png)

![Measurement being run on <s>an IonQ quantum computer<s> Qiskit Aer backend](/screenshots/gameplay_3.png)

![Post death :D](/screenshots/gameplay_4.png)

## Future Directions

* Since Pacman can use H and CNOT gates to generate Bell pairs, it can run a teleportation protocol between two points. This adds another quantum aspect to the game
* Currently the game has no lives counter, we can add that. 
* Other gates like rotation gates
* Multiple levels
* Multiqubit states that will add new gates and gameplay features
* Search algorithm for ghosts, currently they just move randomly.
