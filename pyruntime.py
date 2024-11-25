import struct
import sys

# Define offsets and a signature based on the `_PyRuntimeState` structure
PYRUNTIME_SIGNATURE_OFFSETS = {
    "preinitialized": 0,  # offset for preinitialized (int)
    "core_initialized": 4,  # offset for core_initialized (int)
    "initialized": 8,      # offset for initialized (int)
}

EXPECTED_VALUES = {
    "preinitialized": 0,
    "core_initialized": 0,
    "initialized": 1,  # Python runtime fully initialized
}

def validate_pyruntime(data, offset):
    """Validate a potential _PyRuntimeState structure at the given offset."""
    try:
        # Unpack the three initialization flags (int32 each)
        preinitialized, core_initialized, initialized = struct.unpack_from('3i', data, offset)

        # Check if these fields match the expected values
        return (preinitialized == EXPECTED_VALUES["preinitialized"] and
                core_initialized == EXPECTED_VALUES["core_initialized"] and
                initialized == EXPECTED_VALUES["initialized"])
    except struct.error:
        return False

def find_pyruntime(memory_dump):
    """Search for _PyRuntime in a memory dump."""
    print("[*] Searching for `_PyRuntime` in memory dump...")

    with open(memory_dump, 'rb') as f:
        data = f.read()

    for offset in range(0, len(data) - 12, 4):  # Scan 4-byte aligned
        if validate_pyruntime(data, offset):
            print(f"[+] Potential _PyRuntime found at offset: 0x{offset:x}")
            return offset

    print("[-] `_PyRuntime` not found in the memory dump.")
    return None

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <memory_dump>")
        sys.exit(1)

    memory_dump = sys.argv[1]
    offset = find_pyruntime(memory_dump)
    if offset is not None:
        print(f"[+] `_PyRuntime` confirmed at offset: 0x{offset:x}")

if __name__ == "__main__":
    main()

