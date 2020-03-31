import math
from qiskit import IBMQ, BasicAer, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

#define variables
pi = math.pi
qr = QuantumRegister(4)
cr = ClassicalRegister(4)
qc = QuantumCircuit(qr, cr)

######## init 4 qubits #########
qc.h(qr[0])
qc.h(qr[1])
qc.h(qr[2])
qc.h(qr[3])

### Oracle for 0010 ###
qc.x(qr[0])
qc.x(qr[2])
qc.x(qr[3])

qc.cu1(pi/4, qr[0], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(-pi/4, qr[1], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(pi/4, qr[1], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])

qc.x(qr[0])
qc.x(qr[2])
qc.x(qr[3])


#### Amplification ####
qc.h(qr[0])
qc.h(qr[1])
qc.h(qr[2])
qc.h(qr[3])
qc.x(qr[0])
qc.x(qr[1])
qc.x(qr[2])
qc.x(qr[3])

####### cccZ #########
qc.cu1(pi/4, qr[0], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(-pi/4, qr[1], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(pi/4, qr[1], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])

####### end cccZ #######
qc.x(qr[0])
qc.x(qr[1])
qc.x(qr[2])
qc.x(qr[3])
qc.h(qr[0])
qc.h(qr[1])
qc.h(qr[2])
qc.h(qr[3])

####### Barrier & Measures ########
qc.barrier(qr)
qc.measure(qr[0], cr[0])
qc.measure(qr[1], cr[1])
qc.measure(qr[2], cr[2])
qc.measure(qr[3], cr[3])

#draw circuit
print (qc.draw())

# Execute job
backend_sim = Aer.get_backend('statevector_simulator')
job_sim = execute(qc, backend_sim)
statevec = job_sim.result().get_statevector()
print(statevec)

# Results
qc.measure(qr,cr)
backend = BasicAer.get_backend('qasm_simulator')
shots = 1000
results = execute(qc, backend=backend, shots=shots).result()
answer = results.get_counts()

#Display data
plot_histogram(answer)
plt.show()
