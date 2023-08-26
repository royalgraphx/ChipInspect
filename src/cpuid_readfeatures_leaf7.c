/*
 * ChipInspect - CPU Identification and Inspection Tool
 * cpuid_readfeatures_leaf7.c -  Reads the Extended CPU Feature flags, commonly found in leaf 7.
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

    printf("Showing Extended CPU Feature flags:");
    printf("\n");
    printf("\n");

    // Setup the Bit Table
    char bit_1 = cpuid_binary_str[0];
    char bit_2 = cpuid_binary_str[1];
    char bit_3 = cpuid_binary_str[2];
    char bit_4 = cpuid_binary_str[3];
    char bit_5 = cpuid_binary_str[4];
    char bit_6 = cpuid_binary_str[5];
    char bit_7 = cpuid_binary_str[6];
    char bit_8 = cpuid_binary_str[7];
    char bit_9 = cpuid_binary_str[8];
    char bit_10 = cpuid_binary_str[9];
    char bit_11 = cpuid_binary_str[10];
    char bit_12 = cpuid_binary_str[11];
    char bit_13 = cpuid_binary_str[12];
    char bit_14 = cpuid_binary_str[13];
    char bit_15 = cpuid_binary_str[14];
    char bit_16 = cpuid_binary_str[15];
    char bit_17 = cpuid_binary_str[16];
    char bit_18 = cpuid_binary_str[17];
    char bit_19 = cpuid_binary_str[18];
    char bit_20 = cpuid_binary_str[19];
    char bit_21 = cpuid_binary_str[20];
    char bit_22 = cpuid_binary_str[21];
    char bit_23 = cpuid_binary_str[22];
    char bit_24 = cpuid_binary_str[23];
    char bit_25 = cpuid_binary_str[24];
    char bit_26 = cpuid_binary_str[25];
    char bit_27 = cpuid_binary_str[26];
    char bit_28 = cpuid_binary_str[27];
    char bit_29 = cpuid_binary_str[28];
    char bit_30 = cpuid_binary_str[29];
    char bit_31 = cpuid_binary_str[30];
    char bit_32 = cpuid_binary_str[31];

    if (bit_1 == '1') {
        printf("AVX512 vector length extensions (AVX512VL) is supported!\n");
    } else {
        printf("AVX512 vector length extensions (AVX512VL) is not supported.\n");
    }

    if (bit_2 == '1') {
        printf("AVX512 byte/word instructions (AVX512BW) is supported!\n");
    } else {
        printf("AVX512 byte/word instructions (AVX512BW) is not supported.\n");
    }

    if (bit_3 == '1') {
        printf("SHA extensions is supported!\n");
    } else {
        printf("SHA extensions is not supported.\n");
    }

    if (bit_4 == '1') {
        printf("AVX512 conflict detection extensions (AVX512CD) is supported!\n");
    } else {
        printf("AVX512 conflict detection extensions (AVX512CD) is not supported.\n");
    }

    if (bit_5 == '1') {
        printf("AVX512 exponent/reciprocal instructions (AVX512ER) is supported!\n");
    } else {
        printf("AVX512 exponent/reciprocal instructions (AVX512ER) is not supported.\n");
    }

    if (bit_6 == '1') {
        printf("AVX512 prefetch instructions (AVX512PF) is supported!\n");
    } else {
        printf("AVX512 prefetch instructions (AVX512PF) is not supported.\n");
    }

    if (bit_7 == '1') {
        printf("Intel Processor Trace is supported!\n");
    } else {
        printf("Intel Processor Trace is not supported.\n");
    }

    if (bit_8 == '1') {
        printf("Cache line write back (CLWB) is supported!\n");
    } else {
        printf("Cache line write back (CLWB) is not supported.\n");
    }

    if (bit_9 == '1') {
        printf("CLFLUSHOPT is supported!\n");
    } else {
        printf("CLFLUSHOPT is not supported.\n");
    }

    if (bit_10 == '1') {
        printf("Persistent commit instruction (PCOMMIT) is supported!\n");
    } else {
        printf("Persistent commit instruction (PCOMMIT) is not supported.\n");
    }

    if (bit_11 == '1') {
        printf("AVX512 integer FMA instructions (AVBX512IFMA) is supported!\n");
    } else {
        printf("AVX512 integer FMA instructions (AVBX512IFMA) is not supported.\n");
    }

    if (bit_12 == '1') {
        printf("Supervisor-mode access prevention (SMAP) is supported!\n");
    } else {
        printf("Supervisor-mode access prevention (SMAP) is not supported.\n");
    }

    if (bit_13 == '1') {
        printf("Arbitrary precision add-carry instructions (ADX) is supported!\n");
    } else {
        printf("Arbitrary precision add-carry instructions (ADX) is not supported.\n");
    }

    if (bit_14 == '1') {
        printf("RDSEED is supported!\n");
    } else {
        printf("RDSEED is not supported.\n");
    }

    if (bit_15 == '1') {
        printf("AVX512 dword/qword instructions (AVX512DQ) is supported!\n");
    } else {
        printf("AVX512 dword/qword instructions (AVX512DQ) is not supported.\n");
    }

    if (bit_16 == '1') {
        printf("AVX512 foundation (AVX512F) is supported!\n");
    } else {
        printf("AVX512 foundation (AVX512F) is not supported.\n");
    }
    
    if (bit_17 == '1') {
        printf("PQE / Resource director technology allocation (RDT-A) capability is supported!\n");
    } else {
        printf("PQE / Resource director technology allocation (RDT-A) capability is not supported.\n");
    }

    if (bit_18 == '1') {
        printf("Memory protection extensions (MPX) is supported!\n");
    } else {
        printf("Memory protection extensions (MPX) is not supported.\n");
    }

    if (bit_19 == '1') {
        printf("FPU CS and FPU DS values are supported!\n");
    } else {
        printf("FPU CS and FPU DS values are not supported.\n");
    }

    if (bit_20 == '1') {
        printf("PQM / Resource director technology monitoring (RDT-M) capability is supported!\n");
    } else {
        printf("PQM / Resource director technology monitoring (RDT-M) capability is not supported.\n");
    }

    if (bit_21 == '1') {
        printf("Restricted transactional memory (RTM) is supported!\n");
    } else {
        printf("Restricted transactional memory (RTM) is not supported.\n");
    }

    if (bit_22 == '1') {
        printf("INVPCID is supported!\n");
    } else {
        printf("INVPCID is not supported.\n");
    }

    if (bit_23 == '1') {
        printf("REP MOVSB/STOSB is supported!\n");
    } else {
        printf("REP MOVSB/STOSB is not supported.\n");
    }

    if (bit_24 == '1') {
        printf("BMI2 is supported!\n");
    } else {
        printf("BMI2 is not supported.\n");
    }

    if (bit_25 == '1') {
        printf("Supervisor-mode execution prevention (SMEP) is supported!\n");
    } else {
        printf("Supervisor-mode execution prevention (SMEP) is not supported.\n");
    }

    if (bit_26 == '1') {
        printf("x87 FPU data pointer is supported!\n");
    } else {
        printf("x87 FPU data pointer is not supported.\n");
    }

    if (bit_27 == '1') {
        printf("AVX2 is supported!\n");
    } else {
        printf("AVX2 is not supported.\n");
    }

    if (bit_28 == '1') {
        printf("Hardware lock elision (HLE) is supported!\n");
    } else {
        printf("Hardware lock elision (HLE) is not supported.\n");
    }

    if (bit_29 == '1') {
        printf("BMI1 is supported!\n");
    } else {
        printf("BMI1 is not supported.\n");
    }

    if (bit_30 == '1') {
        printf("Software guard extensions (SGX) is supported!\n");
    } else {
        printf("Software guard extensions (SGX) is not supported.\n");
    }

    if (bit_31 == '1') {
        printf("IA32_TSC_ADJUST MSR is supported!\n");
    } else {
        printf("IA32_TSC_ADJUST MSR is not supported.\n");
    }

    printf("\n");

    return 0;
}