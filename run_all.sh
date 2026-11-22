#!/bin/bash
# Rebuild everything locally from raw/. Publishes nothing.
set -e
cd /workspace/florida
rm -f VERIFY_LOG.txt
python3 scripts/make_manifest.py
python3 scripts/pass1_compute.py
python3 scripts/pass2_verify.py
python3 scripts/compare_passes.py          # exits non-zero unless both passes match exactly and state totals check
python3 scripts/build_outputs.py >/dev/null
python3 scripts/build_pdf.py
python3 scripts/build_wiki.py
python3 scripts/verify_outputs.py
