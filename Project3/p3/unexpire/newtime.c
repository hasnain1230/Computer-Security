#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <time.h>
#include <stdbool.h>

// Name: Hasnain Ali
// netID: ha430
// RUID: 200006372

typedef time_t (*orig_time_t)(time_t *);

static orig_time_t orig_time = NULL;
static int first_call = true;

time_t time(time_t *t) {
    if (orig_time == NULL) {
        orig_time = (orig_time_t) dlsym(RTLD_NEXT, "time");
        if (orig_time == NULL) {
            return 0;
        }
    }

    if (first_call) {
        first_call = false;

        // Set the current time to January 2, 2023
        struct tm new_time = {
                .tm_sec = 0,
                .tm_min = 0,
                .tm_hour = 0,
                .tm_mday = 2,
                .tm_mon = 0,
                .tm_year = 122,
                .tm_wday = 0,
                .tm_yday = 1,
                .tm_isdst = 0
        };

        // Convert the new time to a time_t value
        time_t new_time_t = mktime(&new_time);

        if (t != NULL) {
            *t = new_time_t;
        }

        return new_time_t;
    }

    return orig_time(t);
}
