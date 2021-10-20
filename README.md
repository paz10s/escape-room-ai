My own implementation of Depth First Search and Breadth First Search in Python using OOP. The `Pygame` library was used for the visuals.

# Goal
- The goal of the agent is to reach state `s29`. This is the state where both keys are picked up, the door is unlocked, and the agent is in cell `ex`.
- To unlock the door, the agent must obtain both keys and enter cell `c1`. When this is done, the door will be automatically unlocked and the agent’s only next step will be to move to cell `ex`, transitioning into state `s29`.


# Search Algorithms
- Each search algorithm in this program is modified to **avoid traversing a node twice**. This is to optimize the algorithm since traversing a node more than once is unnecessary. This also prevents the tree traversal from having infinite depth, avoiding infinite loops in the **DFS** algorithm as it tries to reach the deepest node of the tree.
- A folder named Diagrams is provided, containing the State Space, State Transition, and the Graphs of the AI. The Graphs is used to visualize how each algorithm works, as presented in the provided video presentation.
- The number of ***steps*** is equal to the number of times a goal check has occurred.
    - For DFS, a goal check occurs every time a node is traversed.
    - For BFS, a goal check occurs every time before a node is queued.

## Depth First Search (DFS)
- Due to the environment, the deepest node of the tree traversal is always the goal, given that a node can only be traversed at most once.
- The program implements this algorithm by choosing which child to traverse next whenever a node with more than one child is expanded.
- This algorithm follows this behavior:
    1. The initial node is goal checked. If it is not a goal, then it is expanded.
    2. The program then randomly selects one of the node’s children, goal checks it, and expands it if it is not a goal.
    3. This repeats until a goal is reached.
- The console outputs three things: the added node, whether or not the added node has more than one child, and the path.
    - The added node is the most recently traversed or expanded node.
    - Whenever the added node has more than one child, the algorithm randomly chooses which to expand next. Whatever node was added next is the child that was chosen.
    - The path is the set of traversed or expanded nodes.
- Once a goal has been found, the program outputs the solution. The state transition is the path that the agent has taken, and the actions are the actions executed to transition from state to state.

## Breadth First Search (BFS)
- This algorithm uses a queue (first in, first out) to determine which nodes to check and expand. The behavior is as follows:
    - The initial node is enqueued*. The algorithm then expands the first node in the queue and enqueues* each and every one of its children. Once all children have been enqueued, the parent node is removed from the queue. This process repeats until a goal is found.
        **Before a node is enqueued, it is first goal checked.*
    - When a goal is found, a path is traced. This is done by determining the set of traversed nodes that connect the initial node to the goal node. Afterwards, the set of actions required to follow this path is determined. The solution is then outputted.
- The console outputs three things: the queued nodes, the dequeued nodes, and the queue.
- Once a goal has been found, the program outputs the solution, similar to that of the DFS solution output.
