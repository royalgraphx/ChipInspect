#!/bin/bash

: '
ChipInspect - CPU Identification and Inspection Tool
build_all.sh - Compile all C files in the src directory and output to the build folder.
BSD 4-Clause "Original" or "Old" License
Copyright (c) 2023 RoyalGraphX
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

4. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
   OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
   OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
   EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'

# Assumes you are on a macOS host/guest. May work on Linux.

BUILD_DIR="build"

# Clear the console to begin compilation

clear

# Remove the build folder if it exists
if [ -d "$BUILD_DIR" ]; then
    echo "Removing existing $BUILD_DIR folder..."
    rm -rf "$BUILD_DIR"
fi

# Create the build folder
mkdir "$BUILD_DIR"

# Find all .c files in the src directory
c_files=$(find src -name "*.c")

# Compile each .c file
for c_file in $c_files; do
    output_name="build/${c_file#src/}"
    output_name="${output_name%.c}"  # Remove .c extension
    gcc -o "$output_name" "$c_file"
done

echo "Compilation completed!"

# Clear the console to end compilation, modify sleep timer to see errors or to increase speed.

sleep 2
clear