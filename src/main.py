# -----------------------------------------------------------------------------
# 
# ChipInspect - A collection of advanced CPUID tools designed to provide developers with in-depth hardware insight.
# 
# Copyright (c) 2024 RoyalGraphX - BSD 3-Clause License
# See LICENSE file for more detailed information.
# 
# -----------------------------------------------------------------------------

import os
import re
import sys
import time
import json
import click
import shutil
import string
import getpass
import platform
import subprocess
from cffi import FFI

# Define various variables
DEBUG = "FALSE"
CI_vers = "0.0.9"
ffi = FFI()

# Define the list of leaf values with comments explaining their purpose
# Note: The actual availability and use of these leaves can depend on the specific CPU and vendor.
leaf_list = [
    0x00000000,  # Basic CPUID Information
    0x00000001,  # Processor Info and Feature Bits
    0x00000002,  # Cache and TLB Descriptor Information
    0x00000003,  # Processor Serial Number (reserved)
    0x00000004,  # Deterministic Cache Parameters
    0x00000005,  # MONITOR/MWAIT Parameters
    0x00000006,  # Thermal and Power Management Features
    0x00000007,  # Structured Extended Feature Flags Enumeration
    0x00000008,  # Architectural Performance Monitoring (Intel-specific)
    0x00000009,  # Direct Cache Access Information (Intel-specific)
    0x0000000A,  # Architectural Performance Monitoring
    0x0000000B,  # Extended Topology Enumeration
    0x0000000C,  # Intel Processor Trace Enumeration
    0x0000000D,  # Processor Extended State Enumeration (including XSAVE)
    0x0000000E,  # Intel Processor Trace Core-Specific Enumeration
    0x0000000F,  # QoS Enforcement Information (Intel-specific)
    0x00000010,  # QoS Enforcement Monitoring (Intel-specific)
    0x00000011,  # SGX Capabilities (Intel-specific)
    0x00000012,  # SGX Attributes (Intel-specific)
    0x00000013,  # SGX EPC Enumeration (Intel-specific)
    0x00000014,  # Reserved for future use
    0x00000015,  # Time Stamp Counter and Nominal Core Crystal Clock Information
    0x00000016,  # Processor Frequency Information
    0x00000017,  # System-On-Chip Vendor Attribute Enumeration
    0x00000018,  # Reserved for future use
    0x00000019,  # Reserved for future use
    0x0000001A,  # Reserved for future use
    0x0000001B,  # Reserved for future use
    0x0000001C,  # Reserved for future use
    0x0000001D,  # Reserved for future use
    0x0000001E,  # Reserved for future use
    0x0000001F,  # Reserved for future use
    0x00000020,  # Reserved for future use
    0x00000021,  # Reserved for future use
    0x00000022,  # Reserved for future use
    0x00000023,  # Reserved for future use
    0x00000024,  # Reserved for future use
    0x00000025,  # Reserved for future use
    0x00000026,  # Reserved for future use
    0x00000027,  # Reserved for future use
    0x00000028,  # Reserved for future use
    0x00000029,  # Reserved for future use
    0x0000002A,  # Reserved for future use
    0x0000002B,  # Reserved for future use
    0x0000002C,  # Reserved for future use
    0x0000002D,  # Reserved for future use
    0x0000002E,  # Reserved for future use
    0x0000002F,  # Reserved for future use
    0x00000030,  # Reserved for future use
    0x00000031,  # Reserved for future use
    0x00000032,  # Reserved for future use
    0x00000033,  # Reserved for future use
    0x00000034,  # Reserved for future use
    0x00000035,  # Reserved for future use
    0x00000036,  # Reserved for future use
    0x00000037,  # Reserved for future use
    0x00000038,  # Reserved for future use
    0x00000039,  # Reserved for future use
    0x0000003A,  # Reserved for future use
    0x0000003B,  # Reserved for future use
    0x0000003C,  # Reserved for future use
    0x0000003D,  # Reserved for future use
    0x0000003E,  # Reserved for future use
    0x0000003F,  # Reserved for future use
    0x40000000,  # Hypervisor Vendor Leaf
    0x40000001,  # Hypervisor Version Information
    0x40000002,  # Hypervisor Specific Leaf
    0x40000003,  # Hypervisor Specific Leaf
    0x40000004,  # Hypervisor Specific Leaf
    0x40000005,  # Hypervisor Specific Leaf
    0x40000006,  # Hypervisor Specific Leaf
    0x40000007,  # Hypervisor Specific Leaf
    0x40000008,  # Hypervisor Specific Leaf
    0x40000009,  # Hypervisor Specific Leaf
    0x4000000A,  # Hypervisor Specific Leaf
    0x4000000B,  # Hypervisor Specific Leaf
    0x4000000C,  # Hypervisor Specific Leaf
    0x4000000D,  # Hypervisor Specific Leaf
    0x4000000E,  # Hypervisor Specific Leaf
    0x4000000F,  # Hypervisor Specific Leaf
    0x80000000,  # Extended CPUID Information
    0x80000001,  # Extended Processor Info and Feature Bits
    0x80000002,  # Processor Brand String
    0x80000003,  # Processor Brand String Continued
    0x80000004,  # Processor Brand String Continued
    0x80000005,  # L1 Cache and TLB Information
    0x80000006,  # Extended L2 Cache Features
    0x80000007,  # Advanced Power Management Information
    0x80000008,  # Virtual and Physical Address Sizes
    0x80000009,  # SVM Revision and Feature Identifiers (AMD-specific)
    0x8000000A,  # SVM Features (AMD-specific)
    0x8000000B,  # Reserved for future use
    0x8000000C,  # Reserved for future use
    0x8000000D,  # Reserved for future use
    0x8000000E,  # Reserved for future use
    0x8000000F,  # Reserved for future use
    0x80000010,  # Reserved for future use
    0x80000011,  # Reserved for future use
    0x80000012,  # Reserved for future use
    0x80000013,  # Reserved for future use
    0x80000014,  # Reserved for future use
    0x80000015,  # Reserved for future use
    0x80000016,  # Reserved for future use
    0x80000017,  # Reserved for future use
    0x80000018,  # Reserved for future use
    0x80000019,  # Reserved for future use
    0x8000001A,  # Reserved for future use
    0x8000001B,  # Reserved for future use
    0x8000001C,  # Reserved for future use
    0x8000001D,  # Reserved for future use
    0x8000001E,  # Reserved for future use
    0x8000001F,  # Reserved for future use
    0x80000020,  # Reserved for future use
    0x80000021,  # Reserved for future use
    0x80000022,  # Reserved for future use
    0x80000023,  # Reserved for future use
    0x80000024,  # Reserved for future use
    0x80000025,  # Reserved for future use
    0x80000026,  # Reserved for future use
    0x80000027,  # Reserved for future use
    0x80000028,  # Reserved for future use
]

# Define the list of specific AMD Ryzen CPUID leaf values that are of interest
ryzen_leaf_list = [
    0x00000000,  # Basic CPUID Information
    0x00000001,  # Processor Info and Feature Bits
    0x00000002,  # Cache and TLB Descriptor Information
    0x00000004,  # Deterministic Cache Parameters
    0x00000006,  # Thermal and Power Management Features
    0x00000007,  # Structured Extended Feature Flags Enumeration
    0x0000000A,  # Architectural Performance Monitoring
    0x0000000B,  # Extended Topology Enumeration
    0x0000000D,  # Processor Extended State Enumeration (including XSAVE)
    0x00000014,  # Reserved for future use
    0x00000015,  # Time Stamp Counter and Nominal Core Crystal Clock Information
    0x0000001E,  # Reserved for future use
    0x0000001F,  # Reserved for future use
    0x00000020,  # Reserved for future use
    0x00000021,  # Reserved for future use
    0x00000022,  # Reserved for future use
    0x00000023,  # Reserved for future use
    0x00000024,  # Reserved for future use
    0x00000025,  # Reserved for future use
    0x00000026,  # Reserved for future use
    0x00000027,  # Reserved for future use
    0x00000028,  # Reserved for future use
    0x00000029,  # Reserved for future use
    0x0000002A,  # Reserved for future use
    0x0000002B,  # Reserved for future use
    0x0000002C,  # Reserved for future use
    0x0000002D,  # Reserved for future use
    0x0000002E,  # Reserved for future use
    0x0000002F,  # Reserved for future use
    0x00000030,  # Reserved for future use
    0x00000031,  # Reserved for future use
    0x00000032,  # Reserved for future use
    0x00000033,  # Reserved for future use
    0x00000034,  # Reserved for future use
    0x00000035,  # Reserved for future use
    0x00000036,  # Reserved for future use
    0x00000037,  # Reserved for future use
    0x00000038,  # Reserved for future use
    0x00000039,  # Reserved for future use
    0x0000003A,  # Reserved for future use
    0x0000003B,  # Reserved for future use
    0x0000003C,  # Reserved for future use
    0x0000003D,  # Reserved for future use
    0x0000003E,  # Reserved for future use
    0x0000003F,  # Reserved for future use
    0x80000000,  # Extended CPUID Information
    0x80000001,  # Extended Processor Info and Feature Bits
    0x80000002,  # Processor Brand String
    0x80000003,  # Processor Brand String Continued
    0x80000004,  # Processor Brand String Continued
    0x80000005,  # L1 Cache and TLB Information
    0x80000006,  # Extended L2 Cache Features
    0x80000007,  # Advanced Power Management Information
    0x80000008,  # Virtual and Physical Address Sizes
    0x80000009,  # SVM Revision and Feature Identifiers (AMD-specific)
    0x8000000A,  # SVM Features (AMD-specific)
]

# Ensure GCC is used
os.environ['CC'] = 'gcc'

def compile_and_load_cpuid():
    ffi.cdef("""
        void cpuid(uint32_t func, uint32_t subfunc, uint32_t *eax, uint32_t *ebx, uint32_t *ecx, uint32_t *edx);
    """,override=True)

    c_code = """
#include <stdint.h>
#include <stdio.h>

#if defined(__GNUC__) || defined(__clang__)
#include <cpuid.h>

void cpuid(uint32_t func, uint32_t subfunc, uint32_t *eax, uint32_t *ebx, uint32_t *ecx, uint32_t *edx) {
    uint32_t a, b, c, d;
    __cpuid_count(func, subfunc, a, b, c, d);
    *eax = a;
    *ebx = b;
    *ecx = c;
    *edx = d;
}

#elif defined(_MSC_VER)
#include <intrin.h>

void cpuid(uint32_t func, uint32_t subfunc, uint32_t *eax, uint32_t *ebx, uint32_t *ecx, uint32_t *edx) {
    int cpuInfo[4];
    __cpuidex(cpuInfo, func, subfunc);
    *eax = cpuInfo[0];
    *ebx = cpuInfo[1];
    *ecx = cpuInfo[2];
    *edx = cpuInfo[3];
}

#else
#error "Unsupported compiler"
#endif
    """

    with open('cpuid.c', 'w') as f:
        f.write(c_code)

    # Compile the C code to a shared library
    os.system('gcc -shared -o cpuid.dylib -fPIC cpuid.c' if os.name == 'posix' else 'cl /LD cpuid.c')

    # Load the shared library using cffi
    global cpuid_lib
    cpuid_lib = ffi.dlopen('./cpuid.dylib')

    # Clean up generated files
    os.remove('cpuid.c')
    os.remove('cpuid.dylib')

# Define a function to call the cpuid function from the shared library
def call_cpuid(func, subfunc):
    """A wrapper that lets you call cpudid with a leaf and subleaf value, returns various EXX values."""
    eax = ffi.new("uint32_t *")
    ebx = ffi.new("uint32_t *")
    ecx = ffi.new("uint32_t *")
    edx = ffi.new("uint32_t *")
    cpuid_lib.cpuid(func, subfunc, eax, ebx, ecx, edx)
    return eax[0], ebx[0], ecx[0], edx[0]

def print_bits(value, num_bits):
    """Prints the bit representation of a value with colored output."""
    bit_str = ''.join(str((value >> i) & 1) for i in range(num_bits - 1, -1, -1))
    
    # Define ANSI color codes for 0 and 1
    zero_color = 'white'
    one_color = 'green'
    
    # Use click.style to apply colors based on bit values
    colored_str = ''
    for bit in bit_str:
        if bit == '0':
            colored_str += click.style(bit, fg=zero_color)
        else:
            colored_str += click.style(bit, fg=one_color)
    
    return colored_str

def print_hex_bits(hex_value):
    """Prints the bit representation of a hexadecimal value with colored output."""
    # Convert hexadecimal string to an integer
    value = int(hex_value, 16)
    
    # Determine the number of bits (32 bits for standard registers)
    num_bits = 32
    
    # Generate binary string representation with leading zeros
    bit_str = ''.join(str((value >> i) & 1) for i in range(num_bits - 1, -1, -1))
    
    # Define ANSI color codes for 0 and 1
    zero_color = 'white'
    one_color = 'green'
    
    # Use click.style to apply colors based on bit values
    colored_str = ''
    for bit in bit_str:
        if bit == '0':
            colored_str += click.style(bit, fg=zero_color)
        else:
            colored_str += click.style(bit, fg=one_color)
    
    return colored_str

def print_subleaf(subleaf):
    """Prints the subleaf number with colored output."""
    # Define ANSI color codes for subleaf numbers 0 to 5
    colors = ['white', 'bright_magenta', 'bright_green', 'bright_blue', 'bright_red', 'bright_yellow']
    
    # Ensure subleaf is within range, limit to available colors
    subleaf_index = min(subleaf, len(colors) - 1)
    
    # Get the color for the subleaf
    color = colors[subleaf_index]
    
    # Format subleaf number with color
    colored_subleaf = click.style(str(subleaf), fg=color)
    
    return colored_subleaf

def binary_to_char(value):
    """Converts a 32-bit integer into a 4-character string."""
    output = ""
    for i in range(4):
        byte = (value >> (8 * i)) & 0xFF
        output += chr(byte)
    return output

def hex_to_char(hex_value):
    """Converts a hexadecimal string to a 4-character ASCII string."""
    # Convert hexadecimal string to integer
    int_value = int(hex_value, 16)
    
    # Convert integer to bytes and decode as ASCII
    char_value = int_value.to_bytes(4, byteorder='little').decode('ascii', errors='ignore')
    
    return char_value

def is_valid_hex_input(input_str):
    """Check if input string is a valid hexadecimal format."""
    if len(input_str) == 8:
        return all(c.isdigit() or c.lower() in 'abcdef' for c in input_str)
    elif len(input_str) == 10 and input_str[:2].lower() == '0x':
        return all(c.isdigit() or c.lower() in 'abcdef' for c in input_str[2:])
    return False

# Function to probe the maximum leaf for the CPU
def max_leaf():
    max_leaf_supported = 0
    
    leaf = 0
    while True:
        eax, ebx, ecx, edx = call_cpuid(leaf, 0)
        if eax == 0:
            break
        max_leaf_supported = leaf
        leaf += 1
    
    return max_leaf_supported

# Function to probe the maximum subleaf for a given leaf
def probe_max_subleaf(leaf):
    max_subleaf = 0
    previous_eax = None
    
    while True:
        eax, ebx, ecx, edx = call_cpuid(leaf, max_subleaf)
        
        if previous_eax is not None and eax == previous_eax:
            break
        
        previous_eax = eax
        max_subleaf += 1
    
    # The loop ends when an invalid or repeated subleaf is found
    return max_subleaf - 1

# Function to process leaves and return registers for EXX. 
def process_leaves_registers():
    for leaf in leaf_list:
        max_subleaf = probe_max_subleaf(leaf)
        for subleaf in range(max_subleaf + 1):
            eax, ebx, ecx, edx = call_cpuid(leaf, subleaf)
            # Process the results as needed
            print(f"Leaf 0x{leaf:08X}, Subleaf {print_subleaf(subleaf)} - EAX: 0x{eax:08X}, EBX: 0x{ebx:08X}, ECX: 0x{ecx:08X}, EDX: 0x{edx:08X}")

def process_leaves_bits():
    for leaf in leaf_list:
        max_subleaf = probe_max_subleaf(leaf)
        for subleaf in range(max_subleaf + 1):
            eax, ebx, ecx, edx = call_cpuid(leaf, subleaf)
            
            if DEBUG.upper() == "TRUE":
                # Print the bit representation for each register in a debug style layout.
                print(f"Leaf 0x{leaf:08X}, Subleaf {print_subleaf(subleaf)}")
                print("call_cpuid function returned:")
                print(f"EAX: {eax}, EBX: {ebx}, ECX: {ecx}, EDX: {edx}")
                print(f"EAX bits: {print_bits(eax, 32)}")
                print(f"EBX bits: {print_bits(ebx, 32)}")
                print(f"ECX bits: {print_bits(ecx, 32)}")
                print(f"EDX bits: {print_bits(edx, 32)}")
                print()
            else:
                # Print each register's bits with the desired format for end-users
                print(f"Leaf 0x{leaf:08X}, Subleaf {print_subleaf(subleaf)} - {click.style('EAX', bold=True, fg='yellow')}: {print_bits(eax, 32)}")
                print(f"Leaf 0x{leaf:08X}, Subleaf {print_subleaf(subleaf)} - EBX: {print_bits(ebx, 32)}")
                print(f"Leaf 0x{leaf:08X}, Subleaf {print_subleaf(subleaf)} - ECX: {print_bits(ecx, 32)}")
                print(f"Leaf 0x{leaf:08X}, Subleaf {print_subleaf(subleaf)} - {click.style('EDX', bold=True, fg='yellow')}: {print_bits(edx, 32)}")

def generate_raw_table():
    print("CPUID Raw Table:")
    print("leaf     sub   eax       ebx       ecx       edx")

    # Iterate over your CPUID data to fill in the table
    for leaf in leaf_list:
        max_subleaf = probe_max_subleaf(leaf)
        for subleaf in range(max_subleaf + 1):
            eax, ebx, ecx, edx = call_cpuid(leaf, subleaf)

            # Format output according to your specified style
            print(f"{leaf:08X}.0{print_subleaf(subleaf)}    "
                  f"{eax:08X}  {ebx:08X}  {ecx:08X}  {edx:08X}")

def get_host_os():
    """
    Determine the host operating system.

    Returns:
        str: The name of the host operating system ('Linux', 'Windows', 'Darwin' for macOS, etc.).
    """
    return platform.system()

def host_os_pretty():
    """
    Get a pretty-printed version of the host OS with detailed information.

    Returns:
        str: A detailed string describing the host OS.
    """
    os_type = get_host_os()
    
    if os_type == "Linux":
        # Read the os-release file to get distribution information
        try:
            with open('/etc/os-release') as f:
                lines = f.readlines()
                os_info = {}
                for line in lines:
                    key, value = line.strip().split('=', 1)
                    os_info[key] = value.strip('"')
                pretty_name = os_info.get('PRETTY_NAME', 'Linux')
                return pretty_name
        except Exception:
            return "Linux"
    
    elif os_type == "Darwin":
        try:
            # Use sw_vers to get macOS version details
            sw_vers_output = subprocess.check_output(["sw_vers"], text=True).strip().split("\n")
            version_info = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in sw_vers_output}
            kernel_version = get_darwin_kernel_version()
            kernel_type = get_darwin_kernel_type()
            kernel_integrity = get_darwin_kernel_integrity_status()
            kernel_build_string = get_darwin_build_string()
            return f"Darwin {version_info.get('ProductVersion', '')} ({version_info.get('BuildVersion', '')})\n{kernel_integrity}\nDarwin Kernel {kernel_version} ({kernel_type}) - {kernel_build_string}"
        except Exception:
            return "Darwin"
    
    return os_type

def get_darwin_kernel_version():
    """
    Get the kernel version and type for Darwin (macOS) systems.

    Returns:
        str: The kernel version and type.
    """
    try:
        uname_output = subprocess.check_output(["uname", "-r"], text=True).strip()
        return uname_output
    except subprocess.CalledProcessError:
        return "Unknown Kernel Version"

def get_darwin_kernel_type():
    """
    Detect whether the Darwin (macOS) kernel in use is RELEASE or DEVELOPMENT.

    Returns:
        str: 'RELEASE' or 'DEVELOPMENT', or 'Unknown Kernel Type' if detection fails.
    """
    try:
        uname_output = subprocess.check_output(["uname", "-v"], text=True).strip()
        if "RELEASE" in uname_output:
            return click.style("RELEASE", fg="green")
        elif "DEVELOPMENT" in uname_output:
            return click.style("DEVELOPMENT", fg="bright_red")
        else:
            return "Unknown Kernel Type"
    except subprocess.CalledProcessError:
        return "Unknown Kernel Type"

def get_darwin_kernel_integrity_status():
    """
    Check the integrity status of the Darwin (macOS) kernel to determine its type.

    Returns:
        str: Integrity status message indicating the type of kernel.
    """
    try:
        uname_output = subprocess.check_output(["uname", "-v"], text=True).strip()

        if "RELEASE_ARM64" in uname_output or "RELEASE_X86_64" in uname_output:
            if "root:xnu-" in uname_output:
                return "Kernel integrity: Official RELEASE kernel."
            else:
                return "Kernel integrity: Non-official kernel (custom or modified)."
        
        elif "DEVELOPMENT_ARM64" in uname_output or "DEVELOPMENT_X86_64" in uname_output:
            if "root:xnu-" in uname_output:
                return "Kernel integrity: AppleInternal DEVELOPMENT kernel."
            else:
                return "Kernel integrity: Non-official kernel (custom or modified)."
        
        else:
            return "Kernel integrity: Non-standard kernel version (not RELEASE or DEVELOPMENT)."

    except subprocess.CalledProcessError:
        return "Kernel integrity: Unknown"

def get_darwin_build_string():
    """
    Extracts the build string from the uname output for Darwin (macOS) systems.

    Returns:
        str: The build string extracted from the uname output.
    """
    try:
        uname_output = subprocess.check_output(["uname", "-v"], text=True).strip()
        # Find the position of the first ';' after the date
        semicolon_index = uname_output.find(';')
        if semicolon_index != -1:
            return uname_output[semicolon_index + 1:].strip()  # Skip ';' and trim any leading/trailing whitespace
        else:
            return uname_output  # Return the whole string if ';' is not found

    except subprocess.CalledProcessError:
        return "Error: Unable to retrieve build string"


def get_system_architecture():
    return platform.machine()

def get_current_user():
    """
    Get the username of the currently active user running the Python script.

    This function uses the getpass module to retrieve the login name of the user.
    It checks the environment variables LOGNAME, USER, LNAME, and USERNAME in order,
    and returns the value of the first non-empty string.

    Returns:
        str: The username of the currently active user.
    """
    username = getpass.getuser()
    return username

def get_current_directory():
    """Gets the current working directory and returns it"""
    return os.getcwd()

def get_last_directory_name(path):
    """
    Get the last directory name from a given path.
    
    Parameters:
        path (str): The path from which to extract the last directory name.
    
    Returns:
        str: The last directory name in the path.
    """
    return os.path.basename(os.path.normpath(path))

def clear_console_deeply():
    """Clears the console deeply by using ANSI escape sequences."""
    # ANSI escape sequence to clear the screen and move cursor to the top left
    os.system('cls' if os.name == 'nt' else 'clear')

@click.command()
def main():
    """Main entry point for ChipInspect."""
    while True:
        clear_console_deeply()
        click.echo("Welcome to ChipInspect!")
        click.echo("Copyright (c) 2024 RoyalGraphX")
        click.echo(f"Python {get_system_architecture()} Pre-Release {CI_vers} for {host_os_pretty()}\n")
        click.echo("What would you like to do?")
        click.echo("1. Inspect a Leaf and Subleaf")
        click.echo("2. Inspect a Register or 32-Bit Value")
        click.echo("3. Inspect a 4 Value Register based Leaf")
        click.echo("4. Inspect a 4 Value 32-Bit based Leaf")
        click.echo("5. Dump CPU Registers")
        click.echo("6. Dump CPU Leafs in Bits")
        click.echo("7. Dump CPU Register Table")
        click.echo("8. Check AVX2 Support")
        click.echo("9. Exit")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            inspect_leaf_subleaf()
        elif choice == 2:
            inspect_reg_bit_data()
        elif choice == 3:
            inspect_register_leaf()
        elif choice == 4:
            inspect_bit_leaf()
        elif choice == 5:
            dump_cpu_registers()
        elif choice == 6:
            dump_cpu_bits()
        elif choice == 7:
            dump_cpu_register_table()
        elif choice == 8:
            check_avx2_support()
        elif choice == 9:
            exit_program()
        else:
            click.echo("Invalid choice. Please enter a valid option.")

        # Pause to show the result before clearing the screen again
        click.pause()

def inspect_leaf_subleaf():
    click.clear()

    if DEBUG.upper() == "TRUE":
        click.echo("If you see this message, you're in DEBUG mode...")

    compile_and_load_cpuid()

    while True:
        # Prompt the user for func and subfunc values
        func_input = click.prompt("Enter the CPUID leaf (func)", default="0x0", type=str)

        # Remove '0x' prefix if present and ensure it's a valid hex string
        func_input = func_input.lstrip('0x')
        if func_input == "":
            func_input = "0"  # Handle empty input as '0'

        try:
            func = int(func_input, 16)
            break
        except ValueError:
            click.echo(f"Error: '{func_input}' is not a valid hexadecimal integer.")

    while True:
        # Prompt the user for subleaf value, accepting both integer and letter inputs
        subfunc_input = click.prompt("Enter the sub-leaf (subfunc)", default="0", type=str)

        if subfunc_input.isdigit():
            subfunc = int(subfunc_input)
        elif len(subfunc_input) == 1 and subfunc_input.isalpha():
            subfunc = ord(subfunc_input.upper()) - ord('A') + 10
        else:
            click.echo(f"Error: '{subfunc_input}' is not a valid sub-leaf value.")
            continue
        
        click.echo(f"Inspecting CPUID leaf 0x{func:08X}, sub-leaf {subfunc}...\n")
        break

    eax, ebx, ecx, edx = call_cpuid(func, subfunc)
    if DEBUG.upper() == "TRUE":
        click.echo("call_cpuid function returned:")
        click.echo(f"EAX: {eax}, EBX: {ebx}, ECX: {ecx}, EDX: {edx}")
        click.echo()

    # Print registers in the requested format
    click.echo(f"Leaf {func:X} Registers:")
    click.echo(f"EAX: 0x{eax:08X}")
    click.echo(f"EBX: 0x{ebx:08X}")
    click.echo(f"ECX: 0x{ecx:08X}")
    click.echo(f"EDX: 0x{edx:08X}\n")

    # Print raw CPUID chart
    click.echo("Generated Leaf Table:")
    click.echo("leaf     sub   eax       ebx       ecx       edx")
    click.echo(f"{func:08X}.{subfunc:02X}    {eax:08X}  {ebx:08X}  {ecx:08X}  {edx:08X}\n")

    # Capture bit representations as strings
    bit_eax = print_bits(eax, 32)
    bit_ebx = print_bits(ebx, 32)
    bit_ecx = print_bits(ecx, 32)
    bit_edx = print_bits(edx, 32)

    # Print bit representations
    click.echo("Bit representation:")
    click.echo(f"EAX: {bit_eax}")
    click.echo(f"EBX: {bit_ebx}")
    click.echo(f"ECX: {bit_ecx}")
    click.echo(f"EDX: {bit_edx}")
    click.echo()

    # Convert to 4-character strings using binary_to_char
    char_eax = binary_to_char(eax)
    char_ebx = binary_to_char(ebx)
    char_ecx = binary_to_char(ecx)
    char_edx = binary_to_char(edx)

    # Print as 4-character strings
    click.echo("ASCII Representation:")
    click.echo(f"EAX: {char_eax if char_eax else '<empty>'}")
    click.echo(f"EBX: {char_ebx if char_ebx else '<empty>'}")
    click.echo(f"ECX: {char_ecx if char_ecx else '<empty>'}")
    click.echo(f"EDX: {char_edx if char_edx else '<empty>'}")
    click.echo()

    if DEBUG.upper() == "TRUE":
        # Build and print possible decoded strings
        decoded_string_1 = char_eax + char_ebx + char_ecx + char_edx
        decoded_string_2 = char_ebx + char_edx + char_ecx + char_eax

        click.echo("Possible Decoded Strings:\n")
        click.echo(f"{decoded_string_1}")
        click.echo(f"{decoded_string_2}")
        click.echo()

def inspect_reg_bit_data():
    click.clear()

    if DEBUG.upper() == "TRUE":
        click.echo("If you see this message, you're in DEBUG mode...")

    # compile_and_load_cpuid()

    while True:
        input_value = input("Enter a register value or binary bit data: ").strip()

        if not input_value:
            print("No input entered. Please enter a valid value.")
            continue

        # Remove any leading "0x" if present
        if input_value.startswith("0x") or input_value.startswith("0X"):
            input_value = input_value[2:]

        # Check if it's a register value (hexadecimal) or bit data (binary)
        if len(input_value) <= 8 and all(char in "0123456789ABCDEFabcdef" for char in input_value):
            # Assume it's a register value (hexadecimal)
            register_value = int(input_value, 16)
            print(f"Integer Value: {register_value}")
            print(f"Register Value (Hex): 0x{register_value:X}")
            print(f"Binary Representation: {register_value:032b}")
        elif len(input_value) == 32 and all(char in "01" for char in input_value):
            # Assume it's bit data (binary)
            bit_data = int(input_value, 2)
            print(f"Integer Value: {bit_data}")
            print(f"Bit Data (Binary): {input_value}")
            print(f"Hexadecimal Representation: 0x{bit_data:X}")
        else:
            print("Invalid input format. Please enter either a hexadecimal register value or binary bit data.")
            continue

        # Validate the user's response for another inspection
        while True:
            another_inspection = input("Do you want to perform another inspection? (yes/[no]): ").strip().lower()
            if another_inspection in ('yes', 'y', ''):
                break
            elif another_inspection in ('no', 'n'):
                return
            else:
                print("Invalid response. Please enter response.")

def inspect_register_leaf():
    click.clear()

    def hex_to_binary(hex_value):
        # Remove "0x" prefix if present and convert to binary string
        if hex_value.startswith("0x"):
            hex_value = hex_value[2:]
        return bin(int(hex_value, 16))[2:].zfill(32)

    def hex_to_char(hex_value):
        """Converts a hexadecimal string to a 4-character ASCII string."""
        if hex_value.startswith("0x"):
            hex_value = hex_value[2:]
        # Ensure the length is even
        hex_value = hex_value.zfill((len(hex_value) + 1) // 2 * 2)
        
        # Convert pairs of hex digits to characters and reverse the order
        chars = [chr(int(hex_value[i:i+2], 16)) for i in range(0, len(hex_value), 2)]
        return ''.join(reversed(chars))

    if DEBUG.upper() == "TRUE":
        click.echo("If you see this message, you're in DEBUG mode...")

    eax = input("Enter EAX (hexadecimal register format): ").strip()
    if not is_valid_hex_input(eax):
        click.echo(
            "Invalid input for EAX. Please enter a valid hexadecimal register value."
        )
        return
    if eax.startswith("0x"):
        eax = eax[2:].upper()

    ebx = input("Enter EBX (hexadecimal register format): ").strip()
    if not is_valid_hex_input(ebx):
        click.echo(
            "Invalid input for EBX. Please enter a valid hexadecimal register value."
        )
        return
    if ebx.startswith("0x"):
        ebx = ebx[2:].upper()

    ecx = input("Enter ECX (hexadecimal register format): ").strip()
    if not is_valid_hex_input(ecx):
        click.echo(
            "Invalid input for ECX. Please enter a valid hexadecimal register value."
        )
        return
    if ecx.startswith("0x"):
        ecx = ecx[2:].upper()

    edx = input("Enter EDX (hexadecimal register format): ").strip()
    if not is_valid_hex_input(edx):
        click.echo(
            "Invalid input for EDX. Please enter a valid hexadecimal register value."
        )
        return
    if edx.startswith("0x"):
        edx = edx[2:].upper()

    # For debugging, print out the formatted inputs
    if DEBUG.upper() == "TRUE":
        print(f"\ninspect_register_leaf returned: - EAX: 0x{eax}, EBX: 0x{ebx}, ECX: 0x{ecx}, EDX: 0x{edx}")

    # Print formatted output
    click.echo("\nUser Defined Registers:")
    click.echo(f"EAX: 0x{eax}")
    click.echo(f"EBX: 0x{ebx}")
    click.echo(f"ECX: 0x{ecx}")
    click.echo(f"EDX: 0x{edx}")
    print()

    # Generate and print dummy leaf table for user defined registers
    click.echo("Generated Leaf Table:")
    click.echo(f"leaf     sub   eax       ebx       ecx       edx")
    click.echo(f"00000000.00    {eax}  {ebx}  {ecx}  {edx}")
    print()

    # Convert hexadecimal values to binary
    eax_binary = hex_to_binary(eax)
    ebx_binary = hex_to_binary(ebx)
    ecx_binary = hex_to_binary(ecx)
    edx_binary = hex_to_binary(edx)

    # Print bit representations
    print("Bit representation:")
    print(f"EAX: {print_hex_bits(eax)}")
    print(f"EBX: {print_hex_bits(ebx)}")
    print(f"ECX: {print_hex_bits(ecx)}")
    print(f"EDX: {print_hex_bits(edx)}")
    print()

    # Convert hexadecimal values to acsii
    char_eax = hex_to_char(eax)
    char_ebx = hex_to_char(ebx)
    char_ecx = hex_to_char(ecx)
    char_edx = hex_to_char(edx)

    print("ASCII Representation:")
    print(f"EAX: {char_eax if char_eax else '<empty>'}")
    print(f"EBX: {char_ebx if char_ebx else '<empty>'}")
    print(f"ECX: {char_ecx if char_ecx else '<empty>'}")
    print(f"EDX: {char_edx if char_edx else '<empty>'}")
    print()

def inspect_bit_leaf():
    click.clear()

    def print_bits(value):
        """Prints the bit representation of a value."""
        return ''.join(str((value >> i) & 1) for i in range(31, -1, -1))

    def print_bits_colored(value):
        """Prints the bit representation of a value with colored output."""
        colored_bits = []
        for bit in value:
            if bit == '0':
                colored_bits.append(click.style(bit, fg='white'))
            else:
                colored_bits.append(click.style(bit, fg='green'))
        
        return ''.join(colored_bits)

    def binary_to_hex(binary_value):
        """Converts a 32-bit binary string to hexadecimal."""
        hex_value = hex(int(binary_value, 2))
        return hex_value[2:].upper().zfill(8)  # Remove '0x' prefix and zero-pad to 8 characters

    def hex_to_char(hex_value):
        """Converts a hexadecimal string to a 4-character ASCII string."""
        if hex_value.startswith("0x"):
            hex_value = hex_value[2:]
        # Ensure the length is even
        hex_value = hex_value.zfill((len(hex_value) + 1) // 2 * 2)
        
        # Convert pairs of hex digits to characters and reverse the order
        chars = [chr(int(hex_value[i:i+2], 16)) for i in range(0, len(hex_value), 2)]
        return ''.join(reversed(chars))

    if DEBUG.upper() == "TRUE":
        click.echo("If you see this message, you're in DEBUG mode...")

    eax_bits = input("Enter EAX (32-bit binary format): ").strip()
    if len(eax_bits) != 32 or not all(bit in '01' for bit in eax_bits):
        click.echo("Invalid input for EAX. Please enter a valid 32-bit binary value.")
        return

    ebx_bits = input("Enter EBX (32-bit binary format): ").strip()
    if len(ebx_bits) != 32 or not all(bit in '01' for bit in ebx_bits):
        click.echo("Invalid input for EBX. Please enter a valid 32-bit binary value.")
        return

    ecx_bits = input("Enter ECX (32-bit binary format): ").strip()
    if len(ecx_bits) != 32 or not all(bit in '01' for bit in ecx_bits):
        click.echo("Invalid input for ECX. Please enter a valid 32-bit binary value.")
        return

    edx_bits = input("Enter EDX (32-bit binary format): ").strip()
    if len(edx_bits) != 32 or not all(bit in '01' for bit in edx_bits):
        click.echo("Invalid input for EDX. Please enter a valid 32-bit binary value.")
        return

    # Convert binary values to hexadecimal
    eax_hex = binary_to_hex(eax_bits)
    ebx_hex = binary_to_hex(ebx_bits)
    ecx_hex = binary_to_hex(ecx_bits)
    edx_hex = binary_to_hex(edx_bits)

    # For debugging, print out the formatted hexadecimal registers
    if DEBUG.upper() == "TRUE":
        print("\nbinary_to_hex returned registers:")
        print(f"EAX: 0x{eax_hex}")
        print(f"EBX: 0x{ebx_hex}")
        print(f"ECX: 0x{ecx_hex}")
        print(f"EDX: 0x{edx_hex}")

    # Print formatted output
    click.echo("\nUser Defined Registers:")
    click.echo(f"EAX: 0x{eax_hex}")
    click.echo(f"EBX: 0x{ebx_hex}")
    click.echo(f"ECX: 0x{ecx_hex}")
    click.echo(f"EDX: 0x{edx_hex}")
    print()

    # Generate and print dummy leaf table for user defined registers
    click.echo("Generated Leaf Table:")
    click.echo("leaf     sub   eax       ebx       ecx       edx")
    click.echo(f"00000000.00    0x{eax_hex}  0x{ebx_hex}  0x{ecx_hex}  0x{edx_hex}")
    print()

    # Print bit representations
    print("Bit representation:")
    print(f"EAX: {print_bits_colored(eax_bits)}")
    print(f"EBX: {print_bits_colored(ebx_bits)}")
    print(f"ECX: {print_bits_colored(ecx_bits)}")
    print(f"EDX: {print_bits_colored(edx_bits)}")
    print()

    # Convert hexadecimal values to ASCII characters
    char_eax = hex_to_char(eax_hex)
    char_ebx = hex_to_char(ebx_hex)
    char_ecx = hex_to_char(ecx_hex)
    char_edx = hex_to_char(edx_hex)

    print("ASCII Representation:")
    print(f"EAX: {char_eax if char_eax else '<empty>'}")
    print(f"EBX: {char_ebx if char_ebx else '<empty>'}")
    print(f"ECX: {char_ecx if char_ecx else '<empty>'}")
    print(f"EDX: {char_edx if char_edx else '<empty>'}")
    print()

def dump_cpu_registers():
    click.clear()

    if DEBUG.upper() == "TRUE":
        click.echo("If you see this message, you're in DEBUG mode...")

    compile_and_load_cpuid()

    process_leaves_registers()

def dump_cpu_bits():
    click.clear()

    if DEBUG.upper() == "TRUE":
        click.echo("If you see this message, you're in DEBUG mode...")

    compile_and_load_cpuid()

    process_leaves_bits()

def dump_cpu_register_table():
    click.clear()

    if DEBUG.upper() == "TRUE":
        click.echo("If you see this message, you're in DEBUG mode...")

    compile_and_load_cpuid()

    generate_raw_table()

def check_avx2_support():
    click.clear()

    if DEBUG.upper() == "TRUE":
        click.echo("If you see this message, you're in DEBUG mode...")

    compile_and_load_cpuid()

    click.echo("This is a proof of concept entry.")
    print()

    # Query CPUID leaf 7, subleaf 0 to check AVX2 support
    eax, ebx, ecx, edx = call_cpuid(7, 0)
    if DEBUG.upper() == "TRUE":
        print("call_cpuid function returned:")
        print(f"EAX: {eax}, EBX: {ebx}, ECX: {ecx}, EDX: {edx}\n")

    # Print EBX in hexadecimal format
    if DEBUG.upper() == "TRUE":
        print(f"Leaf 7 sub-leaf 0 Registers...")
        print(f"EAX: 0x{eax:08X}")
        print(f"EBX: 0x{ebx:08X}")
        print(f"ECX: 0x{ecx:08X}")
        print(f"EDX: 0x{edx:08X}")
        print()
        
    avx2_bit = ebx & (1 << 5)  # AVX2 bit is 5th bit in EBX (zero-indexed)

    # Print EBX in 32-bit binary format with AVX2 bit highlighted
    ebx_binary = f"{ebx:032b}"
    avx2_bit_index = 31 - 5  # AVX2 bit is 5th from the right (zero-indexed)
    colored_ebx_binary = (
        ebx_binary[:avx2_bit_index]
        + click.style(ebx_binary[avx2_bit_index], fg='green', bold=True)
        + ebx_binary[avx2_bit_index + 1:]
    )
    click.echo(f"EBX in binary: {colored_ebx_binary}")
    print()

    if avx2_bit:
        click.echo("AVX2 is supported on this CPU.")
    else:
        click.echo("AVX2 is not supported on this CPU.")
    
    print()

def exit_program():
    click.echo("Exiting ChipInspect. Goodbye!")
    raise SystemExit

if __name__ == "__main__":
    main()