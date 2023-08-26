/*
 * ChipInspect - CPU Identification and Inspection Tool
 * cpuid_dump_registers.c - Dumps all CPUID registers possible.
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
#include <string.h>

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

void print_bits(uint32_t value, int num_bits) {
    for (int i = num_bits - 1; i >= 0; i--) {
        printf("%d", (value >> i) & 1);
    }
}

void binary_to_char(uint32_t value, char *output) {
    for (int i = 0; i < 4; i++) {
        output[i] = (char)((value >> (8 * i)) & 0xFF);
    }
    output[4] = '\0';
}

int main() {
    uint32_t eax, ebx, ecx, edx;

    // Find the maximum supported EAX value
    cpuid(0, 0, &eax, &ebx, &ecx, &edx);
    uint32_t maxEAX = eax;

    printf("Maximum supported EAX value: 0x%08X\n", maxEAX);

    // Iterate through each EAX value and print the registers
    for (uint32_t currentEAX = 0; currentEAX <= maxEAX; ++currentEAX) {
        cpuid(currentEAX, 0, &eax, &ebx, &ecx, &edx);
        
        printf("CPUID Registers for EAX 0x%08X:\n", currentEAX);
        printf("EAX: 0x%08X\n", eax);
        printf("EBX: 0x%08X\n", ebx);
        printf("ECX: 0x%08X\n", ecx);
        printf("EDX: 0x%08X\n", edx);
        printf("\n");

        printf("[EAX] (Bits): ");
        print_bits(eax, 32);
        printf("\n");

        printf("[EBX] (Bits): ");
        print_bits(ebx, 32);
        printf("\n");

        printf("[ECX] (Bits): ");
        print_bits(ecx, 32);
        printf("\n");

        printf("[EDX] (Bits): ");
        print_bits(edx, 32);
        printf("\n");
        printf("\n");

        printf("Converted EAX to Chars: ");
        char eax_chars[5];
        binary_to_char(eax, eax_chars);
        printf("%s\n", eax_chars);

        printf("Converted EBX to Chars: ");
        char ebx_chars[5];
        binary_to_char(ebx, ebx_chars);
        printf("%s\n", ebx_chars);

        printf("Converted ECX to Chars: ");
        char ecx_chars[5];
        binary_to_char(ecx, ecx_chars);
        printf("%s\n", ecx_chars);

        printf("Converted EDX to Chars: ");
        char edx_chars[5];
        binary_to_char(edx, edx_chars);
        printf("%s\n", edx_chars);

        printf("\n");
    }

    return 0;
}