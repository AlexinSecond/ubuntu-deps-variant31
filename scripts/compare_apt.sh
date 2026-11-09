#!/bin/sh
# Run in Ubuntu with python3, apt-cache and Graphviz installed.
# APT is used only as an independent reference, not by the application.
set -eu
export LC_ALL=C
cd "$(dirname "$0")/.."
command -v apt-cache >/dev/null
command -v dot >/dev/null
task_dir="$(pwd)/output/apt-comparison"
mkdir -p "$task_dir/lists/partial" "$task_dir/sourceparts"
python3 - "$task_dir" <<'PY'
import sys
from pathlib import Path
from src.config import DEFAULT_REPO
from src.download import download_index

folder = Path(sys.argv[1])
name = 'archive.ubuntu.com_ubuntu_dists_noble_main_binary-amd64_Packages'
(folder / 'lists' / name).write_text(download_index(DEFAULT_REPO),
                                   encoding='utf-8')
(folder / 'sources.list').write_text(
    'deb [trusted=yes arch=amd64] '
    'https://archive.ubuntu.com/ubuntu noble main\n', encoding='utf-8')
(folder / 'status').write_text('', encoding='utf-8')
PY
reference_apt() {
    apt-cache \
        -o "Dir::State::lists=$task_dir/lists" \
        -o "Dir::State::status=$task_dir/status" \
        -o "Dir::Etc::sourcelist=$task_dir/sources.list" \
        -o "Dir::Etc::sourceparts=$task_dir/sourceparts" \
        -o "Dir::Cache::pkgcache=" -o "Dir::Cache::srcpkgcache=" \
        -o "APT::Architecture=amd64" "$@"
}
apt-cache --version > "$task_dir/version.txt"
for package in bash grep sed; do
    reference_apt depends --important "$package" \
        > "$task_dir/$package-apt.txt"
    reference_apt -o APT::Cache::GivenOnly=true dotty "$package" \
        > "$task_dir/$package-apt.dot"
    dot -Tpng "$task_dir/$package-apt.dot" \
        -o "$task_dir/$package-apt.png"
    python3 -m src --package "$package" --max-depth 1 --ascii \
        --output "$task_dir/$package-ours.png" \
        > "$task_dir/$package-ours.txt"
done
python3 -m scripts.check_apt_result "$task_dir"
printf '%s\n' "Comparison files: $task_dir"
