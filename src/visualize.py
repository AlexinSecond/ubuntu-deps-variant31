"""Convert a graph to DOT, PNG and an ASCII spanning tree."""

import json
import os
import shutil
import subprocess
import tempfile
from collections import deque
from pathlib import Path

RENDER_TIMEOUT = 60
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def to_dot(graph, repo, root):
    """Describe dependency and provider edges with quoted identifiers."""
    lines = ['digraph dependencies {', '  rankdir=LR;']
    lines.append('  node [shape=box, fontname="Arial"];')
    for name in sorted(graph):
        attributes = []
        if name == root:
            attributes += ['style=filled', 'fillcolor="lightblue"']
        if name in repo.external:
            attributes += ['style=dashed', 'color="red"']
        if name in repo.virtual:
            attributes += ['shape=diamond']
        lines.append(f"  {json.dumps(name)} [{', '.join(attributes)}];")
    for parent, children in sorted(graph.items()):
        for child in sorted(children):
            label = ' [label="provider", style=dashed]'
            label = label if parent in repo.virtual else ""
            source, target = json.dumps(parent), json.dumps(child)
            lines.append(f"  {source} -> {target}{label};")
    return "\n".join([*lines, "}", ""])


def find_dot():
    """Find Graphviz via an explicit path, PATH, or the delivery folder."""
    explicit = os.environ.get("GRAPHVIZ_DOT")
    if explicit:
        return explicit
    executable = shutil.which("dot")
    if executable:
        return executable
    for parent in list(Path(__file__).resolve().parents)[1:4]:
        matches = parent.glob("tools/graphviz/Graphviz*/bin/dot.exe")
        for match in matches:
            return str(match)
    raise ValueError("Graphviz not found. Install it or set GRAPHVIZ_DOT")


def render_png(dot_text, output):
    """Write DOT and render PNG atomically; preserve an older PNG on error."""
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    dot_path = output.with_suffix(".dot")
    dot_path.write_text(dot_text, encoding="utf-8")
    executable = find_dot()
    with tempfile.TemporaryDirectory(dir=output.parent) as folder:
        temporary = Path(folder) / "render.png"
        result = subprocess.run(
            [executable, "-Tpng", str(dot_path), "-o", str(temporary)],
            capture_output=True, timeout=RENDER_TIMEOUT, check=False,
        )
        if result.returncode:
            detail = result.stderr.decode("utf-8", errors="replace")
            raise ValueError(f"Graphviz failed: {detail.strip()}")
        if not temporary.is_file():
            raise ValueError("Graphviz did not create a PNG")
        with temporary.open("rb") as stream:
            if stream.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
                raise ValueError("Graphviz returned an invalid PNG")
        temporary.replace(output)
    return dot_path


def tree_levels(graph, root):
    """Find shortest levels so the displayed tree respects the depth limit."""
    levels = {root: 0}
    pending = deque([root])
    while pending:
        parent = pending.popleft()
        for child in sorted(graph.get(parent, set())):
            if child not in levels:
                levels[child] = levels[parent] + 1
                pending.append(child)
    return levels


def ascii_tree(graph, root):
    """Render each subtree once and annotate cycles and shared nodes."""
    lines = [root]
    expanded = {root}
    levels = tree_levels(graph, root)

    def walk(name, prefix, ancestors):
        """Recursively draw a finite spanning tree of the selected graph."""
        children = sorted(graph.get(name, set()))
        for child in children:
            last = child == children[-1]
            branch = "`-- " if last else "|-- "
            marker = ""
            if child in ancestors:
                marker = " [cycle]"
            elif child in expanded:
                marker = " [shown above]"
            elif levels[child] != levels[name] + 1:
                marker = " [link]"
            lines.append(prefix + branch + child + marker)
            if not marker:
                expanded.add(child)
                indent = "    " if last else "|   "
                walk(child, prefix + indent, ancestors | {child})

    walk(root, "", {root})
    return "\n".join(lines)
