#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
for package in bash grep sed; do
    sh run.sh --package "$package" --max-depth 2 --ascii \
        --output "output/$package.png"
done
