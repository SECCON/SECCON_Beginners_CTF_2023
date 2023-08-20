#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <err.h>

#define LIST_SIZE 5
#define MEMO_SIZE 0x80


char *memos[LIST_SIZE] = {NULL};

int ask_index() {
    int idx = 0;
    char buf[0x100];
    printf("index: ");
    fgets(buf, 0xff, stdin);
    idx = atoi(buf);

    return idx;
}

void create_memo() {
    int idx;
    char *memo;
    idx = ask_index();

    if (idx < 0 || LIST_SIZE <= idx) {
        puts("Invalid index. now choose unused one.");
        for (idx = 0; idx < LIST_SIZE; idx++) {
            if (memos[idx] == NULL) {
                break;
            }
        }
    }

    if (LIST_SIZE <= idx) {
        puts("Can't find unused memo");
        return;
    }

    memo = malloc(MEMO_SIZE);
    memos[idx] = memo;

    return;
}

void read_memo() {
    int idx;
    char *memo;
    idx = ask_index();

    if (idx < 0 || LIST_SIZE <= idx) {
        puts("Invalid index");
        return;
    }

    memo = memos[idx];
    puts(memo);
    
    return;
}

void update_memo() {
    int idx;
    char *memo;
    idx = ask_index();

    if (idx < 0 || LIST_SIZE <= idx) {
        puts("Invalid index");
    } else if (memos[idx] == NULL) {
        puts("that memo is empty");
    } else {
        memo = memos[idx];
    }

    if (memo == NULL) {
        puts("something wrong");
    } else {
        printf("content: ");
        read(STDIN_FILENO, memo, MEMO_SIZE);
    }
    return;
}

void delete_memo() {
    int idx;
    char *memo;
    idx = ask_index();

    if (idx < 0 || LIST_SIZE <= idx) {
        puts("Invalid index");
        return;
    }

    memo = memos[idx];
    if (memo == NULL)
        return;
    free(memo);
    memos[idx] = NULL;

    return;

}

int main() {
    int idx;
    while(1) {
        printf("1. create\n"
               "2. read\n"
               "3. update\n"
               "4. delete\n"
               "5. exit\n"
               "> ");
        if (scanf("%d%*c", &idx) != 1) {
            puts("I/O Error");
            return 1;
        }

        switch (idx) {
            case 1:
                create_memo();
                break;
            case 2:
                read_memo();
                break;
            case 3:
                update_memo();
                break;
            case 4:
                delete_memo();
                break;
            case 5:
                puts("Bye");
                return 0;
            default:
                puts("Invalid index");

        }
    }

}

__attribute__((constructor))
void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(60);
}
