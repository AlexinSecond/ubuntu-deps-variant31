"""Recursive DFS with a depth limit, filtering and cycle protection."""


def dependency_graph(source, root, max_depth, exclude=""):
    """Collect edges, revisiting nodes reached by a shorter path."""
    if root not in source:
        raise ValueError(f"Package not found: {root}")
    if exclude and exclude in root:
        raise ValueError("The exclusion filter removes the root package")
    result = {}
    best_depth = {}

    def visit(name, depth):
        """Visit recursively only when a larger depth budget is available."""
        if name in best_depth and best_depth[name] <= depth:
            return
        best_depth[name] = depth
        result.setdefault(name, set())
        if depth >= max_depth:
            return
        for child in sorted(source.get(name, set())):
            if exclude and exclude in child:
                continue
            result[name].add(child)
            visit(child, depth + 1)

    visit(root, 0)
    return result


def edge_list(graph):
    """Represent every included node, including leaves and isolated roots."""
    return "\n".join(
        f"{name}: {', '.join(sorted(children)) or '(none)'}"
        for name, children in sorted(graph.items())
    )
