/*
 * ChipInspect - CPU Identification and Inspection Tool
 * intel_validity_check.c - Prints out current CPUID Vendor ID Information and compares it to GenuineIntel.
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
#include <inttypes.h>

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

    // Call CPUID with EAX=0 to get vendor ID
    cpuid(0, 0, &eax, &ebx, &ecx, &edx);

    // Display Vendor ID as characters
    printf("Vendor ID: %c%c%c%c%c%c%c%c%c%c%c%c\n",
        ebx & 0xFF, (ebx >> 8) & 0xFF, (ebx >> 16) & 0xFF, (ebx >> 24) & 0xFF,
        edx & 0xFF, (edx >> 8) & 0xFF, (edx >> 16) & 0xFF, (edx >> 24) & 0xFF,
        ecx & 0xFF, (ecx >> 8) & 0xFF, (ecx >> 16) & 0xFF, (ecx >> 24) & 0xFF);

    printf("Leaf 0 Registers:\n");
    printf("\n");
    printf("EAX: 0x%08X\n", eax);
    printf("EBX: 0x%08X\n", ebx);
    printf("ECX: 0x%08X\n", ecx);
    printf("EDX: 0x%08X\n", edx);
    printf("\n");

    printf("Leaf 0 (Bits) [EAX]: ");
    print_bits(eax, 32);
    printf("\n");

    printf("Leaf 0 (Bits) [EBX]: ");
    print_bits(ebx, 32);
    printf("\n");

    printf("Leaf 0 (Bits) [ECX]: ");
    print_bits(ecx, 32);
    printf("\n");

    printf("Leaf 0 (Bits) [EDX]: ");
    print_bits(edx, 32);
    printf("\n");
    printf("\n");

    printf("VMWare Leaf 0 Vendor ID Conversion:\n");

    // Convert EAX to binary string
    printf("cpuid.0.eax = \"");
    print_bits(eax, 32);
    printf("\"\n");

    // Convert EBX to binary string
    printf("cpuid.0.ebx = \"");
    print_bits(ebx, 32);
    printf("\"\n");

    // Convert ECX to binary string
    printf("cpuid.0.ecx = \"");
    print_bits(ecx, 32);
    printf("\"\n");

    // Convert EDX to binary string
    printf("cpuid.0.edx = \"");
    print_bits(edx, 32);
    printf("\"\n");

    // Convert VMWare Vendor ID information to characters
    char vmware_vendor_id_eax[5];  // 4 characters + null terminator
    char vmware_vendor_id_ebx[5];
    char vmware_vendor_id_ecx[5];
    char vmware_vendor_id_edx[5];

    binary_to_char(eax, vmware_vendor_id_eax);
    binary_to_char(ebx, vmware_vendor_id_ebx);
    binary_to_char(ecx, vmware_vendor_id_ecx);
    binary_to_char(edx, vmware_vendor_id_edx);

    printf("Returned VMWare Vendor ID [EAX]: %s\n", vmware_vendor_id_eax);
    printf("Returned VMWare Vendor ID [EBX]: %s\n", vmware_vendor_id_ebx);
    printf("Returned VMWare Vendor ID [ECX]: %s\n", vmware_vendor_id_ecx);
    printf("Returned VMWare Vendor ID [EDX]: %s\n", vmware_vendor_id_edx);
    printf("\n");

    // Check if the converted VMWare data matches the original data
    printf("Comparing returned VMWare data with Intel data:\n");
    printf("EAX: %s\n", strcmp(vmware_vendor_id_eax, "") == 0 ? "Match" : "Mismatch [Normal]");
    printf("EBX: %s\n", strcmp(vmware_vendor_id_ebx, "Genu") == 0 ? "Match" : "Mismatch");
    printf("ECX: %s\n", strcmp(vmware_vendor_id_ecx, "ntel") == 0 ? "Match" : "Mismatch");
    printf("EDX: %s\n", strcmp(vmware_vendor_id_edx, "ineI") == 0 ? "Match" : "Mismatch");

    printf("\n");

    // Concatenate the registers into a 128-bit value
    uint64_t concatenated_value = ((uint64_t)edx << 32) | eax;
    uint64_t concatenated_value_high = ((uint64_t)ebx << 32) | ecx;

    // Use PRIx64 for hexadecimal printing
    printf("Concatenated Value (Lower 64 bits): 0x%016" PRIx64 "\n", concatenated_value);
    printf("Concatenated Value (Upper 64 bits): 0x%016" PRIx64 "\n", concatenated_value_high);
    
    // Use PRIx64 for printing concatenated_value_high and PRIu64 for concatenated_value
    printf("Complete 128-bit Value: 0x%016" PRIx64 "%016" PRIu64 "\n", concatenated_value_high, concatenated_value);
    printf("\n");

    return 0;
}
