#include <stdio.h>
#include <unistd.h>

static char silent_buf[80];
static int saved_stdout;

void stdout_off() {
    saved_stdout = dup(1);
    if(!freopen("/dev/null", "w", stdout)) {
        printf("Error!!redirect to null fail\n"); 
    }
}

void stdout_on() {
    sprintf(silent_buf, "/dev/fd/%d", saved_stdout);
    if(!freopen(silent_buf, "w", stdout)) {
        printf("Error!!redirect to stdout fail\n"); 
    }
}
