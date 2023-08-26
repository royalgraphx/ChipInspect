/*
 * ChipInspect - CPU Identification and Inspection Tool
 * cpuid_avx2_check.c - Checks Leaf 7 specifically for AVX2 Support.
 * BSD 4-Clause "Original" or "Old" License
 * Copyright (c) 2023 RoyalGraphX
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 * 
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 * 
 * 3. Neither the name of the copyright holder nor the names of its
 *    contributors may be used to endorse or promote products derived from
 *    this software without specific prior written permission.
 * 
 * 4. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 *    THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 *    PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
 *    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 *    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 *    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 *    OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 *    OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 *    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <stdio.h>
#include <stdint.h>

void cpuid(uint32_t func, uint32_t subfunc, uint32_t *eax, uint32_t *ebx, uint32_t *ecx, uint32_t *edx) {
    asm volatile (
        "mov %0, %%eax\n"
        "mov %1, %%ecx\n"
        "cpuid\n"
        "mov %%eax, %0\n"
        "mov %%ebx, %1\n"
        "mov %%ecx, %2\n"
        "mov %%edx, %3\n"
        : "=r" (*eax), "=r" (*ebx), "=r" (*ecx), "=r" (*edx)
        : "0" (func), "1" (subfunc)
        : "eax", "ebx", "ecx", "edx"
    );
}

void print_bits(uint32_t value, int num_bits, char *binary_str) {
    for (int i = num_bits - 1; i >= 0; i--) {
        binary_str[num_bits - 1 - i] = ((value >> i) & 1) + '0';
    }
    binary_str[num_bits] = '\0'; // Null-terminate the string
}

int main() {
    uint32_t eax, ebx, ecx, edx;

    // Call CPUID with EAX=7
    cpuid(7, 0, &eax, &ebx, &ecx, &edx);

    printf("\n");
    printf("CPUID leaf 7 Registers:");
    printf("\n");

    printf("EAX: 0x%08X\n", eax);
    printf("EBX: 0x%08X\n", ebx);
    printf("ECX: 0x%08X\n", ecx);
    printf("EDX: 0x%08X\n", edx);
    printf("\n");

    char cpuid_binary_str[33];  // +1 for the null terminator
    print_bits(ebx, 32, cpuid_binary_str);

    printf("[EBX] (Bits): %s\n", cpuid_binary_str);
    printf("\n");

    // Check the 27th character
    char bit_27 = cpuid_binary_str[26];

    if (bit_27 == '1') {
        printf("AVX2 is supported!\n");
    } else {
        printf("AVX2 is not supported.\n");
    }

    return 0;
}