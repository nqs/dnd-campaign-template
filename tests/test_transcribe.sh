#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TRANSCRIBE="$SCRIPT_DIR/../transcribe.sh"

pass=0
fail=0

run_test() {
    local name="$1"
    local got="$2"
    local expected="$3"
    if [ "$got" = "$expected" ]; then
        echo "PASS: $name"
        pass=$((pass + 1))
    else
        echo "FAIL: $name"
        echo "  expected: $expected"
        echo "  got:      $got"
        fail=$((fail + 1))
    fi
}

# No args → usage + non-zero exit
output=$(bash "$TRANSCRIBE" 2>&1 || true)
run_test "no args prints usage" "$(echo "$output" | grep -c "Usage")" "1"
exit_code=0; bash "$TRANSCRIBE" 2>/dev/null || exit_code=$?
run_test "no args exits non-zero" "$([ "$exit_code" -ne 0 ] && echo yes || echo no)" "yes"

# Too many args → usage
output=$(bash "$TRANSCRIBE" a b c 2>&1 || true)
run_test "too many args prints usage" "$(echo "$output" | grep -c "Usage")" "1"

# Missing input file → error message
output=$(bash "$TRANSCRIBE" nonexistent_file.mp3 2>&1 || true)
run_test "missing input file prints error" "$(echo "$output" | grep -c "not found")" "1"
exit_code=0; bash "$TRANSCRIBE" nonexistent_file.mp3 2>/dev/null || exit_code=$?
run_test "missing input file exits non-zero" "$([ "$exit_code" -ne 0 ] && echo yes || echo no)" "yes"

# Default output extension is .md
run_test "default output uses .md extension" \
    "$(grep -c 'OUTPUT.*\.md' "$TRANSCRIBE")" "1"

echo ""
if [ "$fail" -gt 0 ]; then
    echo "$fail test(s) failed (${pass} passed)."
    exit 1
fi
echo "All $pass tests passed."
