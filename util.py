import random
from config import *

# Gate Table (QSG)
QSG_TABLE = {
    '+0': [0, 1, 2, 3], '+1': [1, 0, 3, 2], '+2': [2, 3, 0, 1], '+3': [3, 2, 1, 0],
    '123': [0, 2, 3, 1], '013': [1, 3, 2, 0], '021': [2, 0, 1, 3], '032': [3, 1, 0, 2],
    '132': [0, 3, 1, 2], '012': [1, 2, 0, 3], '023': [2, 1, 3, 0], '031': [3, 0, 2, 1],
    '23': [0, 1, 3, 2], '01': [1, 0, 2, 3], '0213': [2, 3, 1, 0], '0312': [3, 2, 0, 1],
    '12': [0, 2, 1, 3], '0132': [1, 3, 0, 2], '0231': [2, 0, 3, 1], '03': [3, 1, 2, 0],
    '13': [0, 3, 2, 1], '0123': [1, 2, 3, 0], '02': [2, 1, 0, 3], '0321': [3, 0, 1, 2]
}

# All possible gate types
GATE_TYPES = []
for shift in QSG_TABLE:
    GATE_TYPES.append(f"Z{shift}")
    GATE_TYPES.append(f"C3Z{shift}")

# Generate a random gate
def random_gate():
    gtype = random.choice(GATE_TYPES)
    if gtype.startswith("C"):
        ctrl = random.randint(0, NUM_QULINES - 1)
        tgt = random.choice([i for i in range(NUM_QULINES) if i != ctrl])
    else:
        ctrl = tgt = random.randint(0, NUM_QULINES - 1)
    return (ctrl, tgt, gtype)

# Truth table for LOWER: f = 1 if a < b
def generate_lower_truth_table():
    table = {}
    for a in range(QUBASE):
        for b in range(QUBASE):
            f = 1 if a < b else 0
            table[(a, b, 0)] = (a, b, f)
    return table

def generate_equal_truth_table():
    table = {}
    for a in range(QUBASE):
        for b in range(QUBASE):
            f = 3 if a == b else 0
            table[(a, b, 0)] = (a, b, f)
    return table

def generate_greater_truth_table():
    table = {}
    for a in range(QUBASE):
        for b in range(QUBASE):
            f = 2 if a > b else 0
            table[(a, b, 0)] = (a, b, f)
    return table

def generate_ququart_truth_table():
    table = {}
    for a in range(QUBASE):
        for b in range(QUBASE):
            if a == b:
                f = 3
            elif a > b:
                f = 2
            else:
                f = 1
            table[(a, b, 0)] = (a, b, f)
    return table

# Apply a single gate to a state
def apply_gate(state, gate):
    ctrl, tgt, gtype = gate
    lines = list(state)
    if gtype.startswith("Z") and not gtype.startswith("C"):
        lines[tgt] = QSG_TABLE[gtype[1:]][lines[tgt]]
    elif gtype.startswith("C"):
        perm_key = gtype[3:]
        if lines[ctrl] == 3:
            lines[tgt] = QSG_TABLE[perm_key][lines[tgt]]
    return tuple(lines)

# Simulate full circuit
def simulate_circuit(circuit, input_state):
    state = input_state
    for gate in circuit:
        state = apply_gate(state, gate)
    return state

# Fitness: how many outputs match truth table
def fitness(circuit, truth_table):
    correct = 0
    for inp, expected in truth_table.items():
        output = simulate_circuit(circuit, inp)
        if output[2] == expected[2]:
            correct += 1
    if correct / len(truth_table) < 1.0:
        return correct / len(truth_table)
    else:
        return 1 + (1/len(circuit))

def normalize_gate(g):
    ctrl, tgt, typ = g
    if typ.startswith("Z") and not typ.startswith("C"):
        return (tgt, tgt, typ)  # single-wire Z: ctrl == tgt
    return g

def normalize_circuit(circ):
    return [normalize_gate(g) for g in circ]
