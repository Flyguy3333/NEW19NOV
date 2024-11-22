#include <ta_libc.h>
#include <stdio.h>

int main() {
    TA_RetCode retCode = TA_Initialize();
    if (retCode == TA_SUCCESS) {
        printf("TA-Lib initialized successfully!\n");
        TA_Shutdown();
    } else {
        printf("Failed to initialize TA-Lib.\n");
    }
    return 0;
}

