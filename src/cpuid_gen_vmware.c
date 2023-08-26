/*
 * ChipInspect - CPU Identification and Inspection Tool
 * cpuid_gen_vmware.c - Dumps CPUID leafs in Binary/VMWare format.
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

struct Leaf {
    uint32_t leaf;
};

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

int main() {
    struct Leaf leaf[] = {
        {0x00000000},
        {0x00000001},
        {0x00000002},
        {0x00000003},
        {0x00000004},
        {0x00000005},
        {0x00000006},
        {0x00000007},
        {0x00000009},
        {0x0000000A},
        {0x0000000B},
        {0x0000000D},
        {0x0000000F},
        {0x00000010},
        {0x00000012},
        {0x00000014},
        {0x00000015},
        {0x00000016},
        {0x00000017},
        {0x40000000},
        {0x40000001},
        {0x40000002},
        {0x40000003},
        {0x40000004},
        {0x40000005},
        {0x40000006},
        {0x40000007},
        {0x4000000B},
        {0x80000000},
        {0x80000001},
        {0x80000002},
        {0x80000003},
        {0x80000004},
        {0x80000006},
        {0x80000007},
        {0x80000008}
        
    };

    for (int i = 0; i < sizeof(leaf) / sizeof(leaf[0]); i++) {
        uint32_t eax, ebx, ecx, edx;
        cpuid(leaf[i].leaf, 0, &eax, &ebx, &ecx, &edx);

        printf("cpuid.%X.eax = \"", leaf[i].leaf);
        print_bits(eax, 32);
        printf("\"\n");

        printf("cpuid.%X.ebx = \"", leaf[i].leaf);
        print_bits(ebx, 32);
        printf("\"\n");

        printf("cpuid.%X.ecx = \"", leaf[i].leaf);
        print_bits(ecx, 32);
        printf("\"\n");

        printf("cpuid.%X.edx = \"", leaf[i].leaf);
        print_bits(edx, 32);
        printf("\"\n");
    }

    return 0;
}