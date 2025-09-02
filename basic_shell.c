#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
    char line[1024];

    while (1) {
        printf("AcidopShell$ ");   
        fflush(stdout);

        if (!fgets(line, sizeof(line), stdin)) {
            printf("\n");
            break;
        }

        line[strcspn(line, "\n")] = 0;

        if (strcmp(line, "exit") == 0) {
            break;
        }

        pid_t pid = fork();
        if (pid == 0) {
            execlp(line, line, (char *)NULL);  
            perror("execlp"); 
            exit(1);
        } else if (pid > 0) {
            wait(NULL);
        } else {
            perror("fork");
        }
    }
    return 0;
} 
