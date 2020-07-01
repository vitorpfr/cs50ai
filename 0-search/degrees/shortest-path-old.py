def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Set goal
    goal = target

    # Initialize frontier to just the starting position
    start = Node(state = source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            return None

        # Choose a node from the frontier
        node = frontier.remove()

        # If node is the goal, then we have a solution
        if node.state == goal:

            path = []
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()

            return path

        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to frontier
        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)

    return None