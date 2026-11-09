"""Run the final CLI in separate processes, including a local HTTP index."""

import functools
import gzip
import http.server
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


def execute(args, environment=None):
    """Invoke the actual CLI with a timeout and captured UTF-8 output."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    env.update(environment or {})
    return subprocess.run(
        [sys.executable, "-m", "src", *args], cwd=PROJECT, env=env,
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )


class CliTests(unittest.TestCase):
    """Test public behavior rather than internal call structure."""

    def test_file_mode_and_input_preservation(self):
        """UTF-8 BOM and paths with spaces work; the source is unchanged."""
        with tempfile.TemporaryDirectory(prefix="graph test ") as folder:
            source = Path(folder) / "input.json"
            original = '\ufeff{"A": ["B"], "B": ["A"]}'.encode("utf-8")
            source.write_bytes(original)
            image = Path(folder) / "result.png"
            result = execute([
                "--package", "A", "--test-repo", "--repo", str(source),
                "--output", str(image), "--ascii",
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("[cycle]", result.stdout)
            self.assertTrue(image.is_file())
            self.assertEqual(source.read_bytes(), original)

    def test_missing_package(self):
        """An absent root has exit code one and no traceback."""
        result = execute(["--package", "Z", "--test-repo",
                          "--repo", "examples/tree.json"])
        self.assertEqual(result.returncode, 1)
        self.assertIn("Package not found", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_argument_error(self):
        """Invalid command-line options have exit code two."""
        result = execute(["--package", "bash", "--max-depth", "-1"])
        self.assertEqual(result.returncode, 2)

    def test_bad_json(self):
        """Malformed JSON produces a readable failure."""
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "bad.json"
            source.write_text("not JSON", encoding="utf-8")
            result = execute(["--package", "A", "--test-repo",
                              "--repo", str(source)])
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stderr)

    def test_no_renderer(self):
        """A missing external renderer is reported without losing DOT."""
        with tempfile.TemporaryDirectory() as folder:
            image = Path(folder) / "result.png"
            result = execute([
                "--package", "A", "--test-repo",
                "--repo", "examples/tree.json", "--output", str(image),
            ], {"GRAPHVIZ_DOT": "definitely-missing-dot"})
            self.assertEqual(result.returncode, 1)
            self.assertTrue(image.with_suffix(".dot").exists())
            self.assertFalse(image.exists())

    def test_http_download(self):
        """Fetch compressed metadata through HTTP and generate a real PNG."""
        with tempfile.TemporaryDirectory() as folder:
            data = b"Package: aa\nDepends: bb\n\nPackage: bb\n"
            Path(folder, "Packages.gz").write_bytes(gzip.compress(data))
            handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                        directory=folder)
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
            with server:
                thread = threading.Thread(target=server.serve_forever)
                thread.start()
                try:
                    self.check_http_result(server.server_port, folder)
                finally:
                    server.shutdown()
                    thread.join()

    def check_http_result(self, port, folder):
        """Exercise both successful download and an HTTP error."""
        url = f"http://127.0.0.1:{port}/Packages.gz"
        image = str(Path(folder) / "remote.png")
        result = execute(["--package", "aa", "--repo", url,
                          "--output", image, "--ascii"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("`-- bb", result.stdout)
        missing = f"http://127.0.0.1:{port}/missing/Packages"
        result = execute(["--package", "aa", "--repo", missing])
        self.assertEqual(result.returncode, 1)
        self.assertIn("404", result.stderr)
