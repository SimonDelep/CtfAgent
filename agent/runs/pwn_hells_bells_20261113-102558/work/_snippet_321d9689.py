import subprocess
import sys

# Run binary with timeout
result = subprocess.run(
    ["gdb", "-batch", "-ex", "break main", "-ex", "run", "-ex", "disassemble main", "-ex", "quit", "thermite-charge"],
    capture_output=True, text=True, timeout=10
)
print(result.stdout)
print(result.stderr)