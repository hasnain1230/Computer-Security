#define _GNU_SOURCE
#include <dirent.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// Name: Hasnain Ali
// netID: ha430
// RUID: 200006372
// your code for readdir goes here


typedef struct dirent *(*original_readdir)(DIR *dirp);

struct dirent *readdir(DIR *dirp) {
    original_readdir originalReaddir = (original_readdir) dlsym(RTLD_NEXT, "readdir");
    struct dirent *entry;
    const char *hidden_files = getenv("HIDDEN");

    while ((entry = originalReaddir(dirp)) != NULL) {
        if (hidden_files == NULL) {
            return entry;
        }

        int hidden = false;
        char *file_list = strdup(hidden_files);
        char *file = strtok(file_list, ":");

        while (file != NULL) {
            if (strcmp(entry->d_name, file) == 0) {
                hidden = true;
                break;
            }

            file = strtok(NULL, ":"); // NULL to continue from the last token
        }

        free(file_list);

        if (!hidden) {
            return entry;
        }
    }

    return NULL;
}