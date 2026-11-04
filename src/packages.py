"""Read Ubuntu binary Packages data without package-manager libraries."""

import re
from dataclasses import dataclass, field

RELATION = re.compile(
    r"([a-z0-9][a-z0-9+.-]+)(?::[a-z0-9-]+)?(?:\s*\([^()]+\))?"
)


@dataclass
class Repository:
    """Named dependency edges, with virtual and unavailable nodes marked."""

    graph: dict
    external: set = field(default_factory=set)
    virtual: set = field(default_factory=set)
    relations: dict = field(default_factory=dict)


def stanzas(text):
    """Read RFC822-style fields, including folded continuation lines."""
    record = {}
    key = None
    for line in [*text.splitlines(), ""]:
        if not line.strip():
            if record:
                yield record
            record, key = {}, None
        elif line.startswith((" ", "\t")):
            if key is None:
                raise ValueError("Packages: continuation without a field")
            record[key] += " " + line.strip()
        else:
            key, separator, value = line.partition(":")
            if not separator or not key or key in record:
                raise ValueError("Packages: invalid or repeated field")
            record[key] = value.strip()


def dependency_names(value):
    """Extract all alternative names, preserving no version constraints."""
    names = set()
    if not value:
        return names
    for alternative in re.split(r"[,|]", value):
        match = RELATION.fullmatch(alternative.strip())
        if match is None:
            raise ValueError(f"Unsupported binary relation: {alternative}")
        names.add(match.group(1))
    return names


def add_record(record, repo, providers):
    """Add one binary package and collect its virtual package names."""
    name = record.get("Package", "")
    if not re.fullmatch(r"[a-z0-9][a-z0-9+.-]+", name):
        raise ValueError("Packages: missing or invalid Package field")
    if name in repo.graph:
        raise ValueError(f"Multiple versions of {name}; use one index")
    fields = (record.get("Pre-Depends", ""), record.get("Depends", ""))
    repo.relations[name] = ", ".join(value for value in fields if value)
    repo.graph[name] = dependency_names(repo.relations[name])
    for virtual in dependency_names(record.get("Provides", "")):
        providers.setdefault(virtual, set()).add(name)


def parse_packages(text):
    """Build a graph of declared dependencies from one binary index."""
    repo = Repository({})
    providers = {}
    for record in stanzas(text):
        add_record(record, repo, providers)
    if not repo.graph:
        raise ValueError("Packages: empty index")
    for name, packages in providers.items():
        if name not in repo.graph:
            repo.graph[name] = packages
            repo.virtual.add(name)
    targets = {child for names in repo.graph.values() for child in names}
    repo.external = targets - repo.graph.keys()
    repo.graph.update({name: set() for name in repo.external})
    return repo
