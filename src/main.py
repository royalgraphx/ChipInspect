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
CI_vers = "0.0.1"
ffi = FFI()

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

def binary_to_char(value):
    """Converts a 32-bit integer into a 4-character string."""
    output = ""
    for i in range(4):
        output += chr((value >> (8 * i)) & 0xFF)
    return output

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
            return click.style("DEVELOPMENT", fg="yellow")
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

@click.command()
def main():
    """Main entry point for ChipInspect."""
    while True:
        click.clear()
        click.echo("Welcome to ChipInspect!")
        click.echo("Copyright (c) 2024 RoyalGraphX")
        click.echo(f"Python {get_system_architecture()} Pre-Release {CI_vers} for {host_os_pretty()}\n")
        click.echo("What would you like to do?")
        click.echo("1. Inspect a leaf and subleaf")
        click.echo("2. Exit")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            inspect_leaf_subleaf()
        elif choice == 2:
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

    subfunc = click.prompt("Enter the sub-leaf (subfunc)", default="0", type=int)

    click.echo(f"Inspecting CPUID leaf 0x{func:08X}, sub-leaf {subfunc}...\n")
    
    eax, ebx, ecx, edx = call_cpuid(func, subfunc)
    if DEBUG.upper() == "TRUE":
        print("call_cpuid function returned:")
        print(f"EAX: {eax}, EBX: {ebx}, ECX: {ecx}, EDX: {edx}\n")

    # Print registers in the requested format
    print(f"Leaf {func:X} Registers:")
    print(f"EAX: 0x{eax:08X}")
    print(f"EBX: 0x{ebx:08X}")
    print(f"ECX: 0x{ecx:08X}")
    print(f"EDX: 0x{edx:08X}\n")

    # Print raw CPUID chart
    print("Generated Leaf Table:")
    print("leaf     sub   eax       ebx       ecx       edx")
    print(f"{func:08X}.{subfunc:02X}    {eax:08X}  {ebx:08X}  {ecx:08X}  {edx:08X}\n")

    # Capture bit representations as strings
    bit_eax = print_bits(eax, 32)
    bit_ebx = print_bits(ebx, 32)
    bit_ecx = print_bits(ecx, 32)
    bit_edx = print_bits(edx, 32)

    # Print bit representations
    print("Bit representation:")
    print("EAX:", bit_eax)
    print("EBX:", bit_ebx)
    print("ECX:", bit_ecx)
    print("EDX:", bit_edx)
    print()

    # Convert to 4-character strings using binary_to_char
    char_eax = binary_to_char(eax)
    char_ebx = binary_to_char(ebx)
    char_ecx = binary_to_char(ecx)
    char_edx = binary_to_char(edx)

    # Print as 4-character strings
    print("4-Character Strings:")
    click.echo(f"EAX: {char_eax if char_eax else '<empty>'}")
    click.echo(f"EBX: {char_ebx if char_ebx else '<empty>'}")
    click.echo(f"ECX: {char_ecx if char_ecx else '<empty>'}")
    click.echo(f"EDX: {char_edx if char_edx else '<empty>'}")
    print()

    if DEBUG.upper() == "TRUE":
        # Build and print possible decoded strings
        decoded_string_1 = char_eax + char_ebx + char_ecx + char_edx
        decoded_string_2 = char_ebx + char_edx + char_ecx + char_eax

        print("Possible Decoded Strings:\n")
        print(f"{decoded_string_1}")
        print(f"{decoded_string_2}")
        print()

def exit_program():
    click.echo("Exiting ChipInspect. Goodbye!")
    raise SystemExit

if __name__ == "__main__":
    main()
