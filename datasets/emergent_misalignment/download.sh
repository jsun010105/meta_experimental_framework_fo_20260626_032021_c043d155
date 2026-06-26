#!/usr/bin/env bash
# Download the Emergent Misalignment training datasets (Betley et al. 2025).
# These ground the synthetic-benchmark generation for the meta-experimental
# diagnostic framework (real misalignment-training data with known outcomes).
set -e
DEST="$(dirname "$0")"
TMP="$DEST/_repo"
git clone --depth 1 https://github.com/emergent-misalignment/emergent-misalignment "$TMP"
cp "$TMP"/data/*.jsonl "$DEST"/
rm -rf "$TMP"
echo "Downloaded EM datasets to $DEST/"
ls -la "$DEST"/*.jsonl
