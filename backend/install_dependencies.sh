#!/bin/sh
# Install Python dependencies from local wheels bundled in ./vendor
DIR="$(cd "$(dirname "$0")" && pwd)"

pip install --no-index --find-links="$DIR/vendor" -r "$DIR/requirements.txt"
