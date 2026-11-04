"""Verify real metadata syntax without a network dependency."""

import gzip
import lzma
import unittest

from src.download import decode_index, index_url
from src.packages import dependency_names, parse_packages, stanzas

SAMPLE = """Package: app
Version: 1
Pre-Depends: base (>= 1)
Depends: lib:any (>= 2) | other,
 virtual
Recommends: ignored

Package: base
Version: 1

Package: lib
Provides: virtual (= 1)
"""


class PackagesTests(unittest.TestCase):
    """Dependency extraction follows binary Packages field syntax."""

    def test_alternatives_versions_and_architecture(self):
        """Keep both alternatives but remove versions and qualifiers."""
        self.assertEqual(dependency_names("aa:any (>= 1) | bb, cc:native"),
                         {"aa", "bb", "cc"})

    def test_folded_and_pre_dependencies(self):
        """Folded fields and Pre-Depends contribute to the graph."""
        repo = parse_packages(SAMPLE)
        self.assertEqual(repo.graph["app"],
                         {"base", "lib", "other", "virtual"})
        self.assertNotIn("ignored", repo.graph)

    def test_virtual_and_external(self):
        """Virtual nodes point to providers; absent targets are leaves."""
        repo = parse_packages(SAMPLE)
        self.assertEqual(repo.graph["virtual"], {"lib"})
        self.assertEqual(repo.virtual, {"virtual"})
        self.assertEqual(repo.external, {"other"})

    def test_invalid_metadata(self):
        """Malformed, empty and duplicate package records are rejected."""
        samples = ["", "broken", " abc", "Version: 1", "Package: Bad"]
        samples += ["Package: aa\n\nPackage: aa", "Package: aa\nDepends: ???"]
        for sample in samples:
            with self.subTest(sample=sample), self.assertRaises(ValueError):
                parse_packages(sample)

    def test_compression(self):
        """Plain, gzip and xz representations give the same Unicode text."""
        data = SAMPLE.encode("utf-8")
        cases = [(data, "Packages"), (gzip.compress(data), "Packages.gz"),
                 (lzma.compress(data), "Packages.xz")]
        for value, name in cases:
            self.assertEqual(decode_index(value, name), SAMPLE)

    def test_directory_url(self):
        """Directory URLs expand without losing query parameters."""
        self.assertEqual(index_url("https://example.com/amd64/?x=1"),
                         "https://example.com/amd64/Packages.xz?x=1")

    def test_crlf_and_final_record(self):
        """Windows newlines and a missing trailing blank are supported."""
        self.assertEqual(list(stanzas("Package: aa\r\nVersion: 1")),
                         [{"Package": "aa", "Version": "1"}])
