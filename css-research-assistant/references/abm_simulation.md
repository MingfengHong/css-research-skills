# ABM and Simulation Reference

## Table of Contents
1. [Intent Routing](#1-intent-routing)
2. [Phase 1: Model Architecture](#2-phase-1-model-architecture)
3. [Phase 2: OOP Strictness](#3-phase-2-oop-strictness)
4. [Phase 3: Execution Constraints](#4-phase-3-execution-constraints)
5. [Phase 4: Validation Protocol](#5-phase-4-validation-protocol)
6. [Phase 5: Output and Diagnostics](#6-phase-5-output-and-diagnostics)

---

## 1. Intent Routing

Classify the simulation type before writing code:

| Route | Condition | Space Type |
|---|---|---|
| **Spatial-Grid Dynamics** | Segregation, cellular automata, resource foraging, urban location choice | `SingleGrid` or `MultiGrid` (Mesa) |
| **Topological-Network Dynamics** | Opinion dynamics, epidemic spreading, innovation diffusion, alliance formation | `NetworkGrid` (Mesa) + `NetworkX` |
| **Policy Optimization** | Finding optimal parameters under constraints; ABM as fitness evaluator | `BatchRunner` + `scipy.optimize` or GA |

---

## 2. Phase 1: Model Architecture

Before coding, sketch the micro-macro linkage:
- **Micro**: What is the agent's state space? What rules govern individual behavior?
- **Meso**: How do agents interact? (Local neighborhood? Network ties? Global broadcast?)
- **Macro**: What emergent phenomenon should the `DataCollector` track?

Write this as a comment block at the top of the model file.

---

## 3. Phase 2: OOP Strictness

All ABM code MUST use Mesa's class hierarchy:

```python
from mesa import Agent, Model
from mesa.space import SingleGrid, NetworkGrid
from mesa.time import RandomActivation, SimultaneousActivation
from mesa.datacollection import DataCollector
```

### 3.1 Model Class (`class MyModel(Model)`)

`__init__` MUST initialize in this exact order:
1. `self.schedule` — e.g., `RandomActivation(self)` or `SimultaneousActivation(self)`
2. `self.space` — Grid or Network
3. `self.datacollector` — `DataCollector(model_reporters={...}, agent_reporters={...})`

### 3.2 Agent Class (`class MyAgent(Agent)`)

`step()` MUST follow the sequence:
1. **Perception**: Read local environment or neighbors.
2. **Decision**: Update internal state based on rules.
3. **Action**: Modify the environment or communicate with other agents.

---

## 4. Phase 3: Execution Constraints

### 4.1 Randomness and Reproducibility

- **Never** use Python's built-in `random` module directly inside agents.
- Use Mesa's internal RNG: `self.random.random()`, `self.random.choice()`, etc.
- Pass `seed=SEED` to `Model.__init__` and log the seed value.

### 4.2 Spatial Lookup Performance

- **Forbidden**: Looping through all agents to find spatial proximity. This is O(N^2).
- **Required**: Use Mesa's built-in spatial lookups:
  - `self.grid.get_neighbors(self.pos, moore=True, radius=1)`
  - `self.grid.get_cell_list_contents(self.pos)`
- For network dynamics, use `self.grid.get_neighbors(node_id)` via `NetworkGrid`.

### 4.3 Defensive Assertions

Inject domain assertions inside agent logic:
```python
assert 0 <= self.wealth <= max_wealth, "Wealth out of bounds"
assert 0 <= probability <= 1.0, "Probability must be in [0, 1]"
```

Handle empty cells gracefully:
```python
if self.model.grid.exists_empty_cells():
    self.model.grid.move_to_empty(self)
```

### 4.4 Complexity Annotation

Annotate the time complexity of `Model.step()`:
```python
def step(self):
    """Execute one model step.
    Time Complexity: O(N * k) where k = max neighbors (<= 8 for Moore grid).
    """
    self.datacollector.collect(self)
    self.schedule.step()
```

---

## 5. Phase 4: Validation Protocol

### 5.1 Dry Run Test

Every ABM script MUST include a minimal test block:
```python
if __name__ == "__main__":
    model = MyModel(seed=42)
    for _ in range(10):
        model.step()
    print("Dry run passed: 10 steps executed without errors")
```

### 5.2 Invariant Checks

After a full run, verify:
- State variables remain within valid ranges.
- Total system quantities are conserved (if applicable).
- Awareness / adoption rates are monotonic (if the model assumes irreversible transitions).

### 5.3 Reproducibility Check

Run the model twice with the same seed. Compare `DataCollector` outputs row-by-row. They must be identical.

---

## 6. Phase 5: Output and Diagnostics

### 6.1 Time-Series Output

Export `DataCollector` results to `output/model_data.csv`. Include:
- Step number
- All model-level reporters (e.g., awareness_rate, gini_coefficient)
- All agent-level reporters (if requested)

### 6.2 Visualization

- Plot time-series of macro variables with `seaborn` or `matplotlib`.
- Use `sns.despine()`, Okabe-Ito colors, and `dpi=300`.
- For spatial models, render agent positions as a grid heatmap or scatter plot.

### 6.3 Validation Checklist

1. [ ] Micro-Meso-Macro linkage explicitly tagged in code comments
2. [ ] Randomness controlled via Mesa's `self.random`, not Python `random`
3. [ ] Spatial lookup uses Mesa native methods (no O(N^2) neighbor search)
4. [ ] Dry run test block included and passes
5. [ ] Reproducibility: same seed produces identical trajectories
6. [ ] Time-series data exported to `output/model_data.csv`
