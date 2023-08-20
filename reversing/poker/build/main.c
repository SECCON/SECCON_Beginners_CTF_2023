#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUM_CARDS 52
#define NUM_SUITS 4
#define NUM_RANKS 13

typedef enum { CLUBS, DIAMONDS, HEARTS, SPADES } Suit;

typedef enum {
  ACE = 1,
  TWO,
  THREE,
  FOUR,
  FIVE,
  SIX,
  SEVEN,
  EIGHT,
  NINE,
  TEN,
  JACK,
  QUEEN,
  KING
} Rank;

typedef struct {
  Suit suit;
  Rank rank;
} Card;

int play_poker(int score, int choice) {
  Card deck[NUM_CARDS];
  Card player1, player2;

  int i, j, k;
  k = 0;
  for (i = 0; i < NUM_SUITS; i++) {
    for (j = 1; j <= NUM_RANKS; j++) {
      deck[k].suit = i;
      deck[k].rank = j;
      k++;
    }
  }

  srand(time(NULL));
  for (i = 0; i < NUM_CARDS; i++) {
    int r = rand() % NUM_CARDS;
    Card temp = deck[i];
    deck[i] = deck[r];
    deck[r] = temp;
  }

  player1 = deck[0];
  player2 = deck[1];

  if (player1.rank > player2.rank) {
    if (choice == 1) {
      printf("[+] Player 1 wins! You got score!\n");
      score += 1;
    } else {
      printf("[-] Player 1 wins! Your score is reseted...\n");
      score = 0;
    }
  } else if (player1.rank < player2.rank) {
    if (choice == 2) {
      printf("[+] Player 2 wins! You got score!\n");
      score += 1;
    } else {
      printf("[-] Player 2 wins! Your score is reseted...\n");
      score = 0;
    }
  } else {
    printf("[+] It's a tie! Your score is reseted...\n");
    score = 0;
  }
  return score;
}

int get_choice() {
  int choice;
  do {
    printf("[?] Enter 1 or 2: ");
    scanf("%d", &choice);
  } while (choice != 1 && choice != 2);
  return choice;
}

void print_welcome() {
  puts("");
  puts("██╗███╗   ██╗██████╗ ██╗ █████╗ ███╗   ██╗    ██████╗  ██████╗ ██╗  "
       "██╗███████╗██████╗");
  puts("██║████╗  ██║██╔══██╗██║██╔══██╗████╗  ██║    ██╔══██╗██╔═══██╗██║ "
       "██╔╝██╔════╝██╔══██╗");
  puts("██║██╔██╗ ██║██║  ██║██║███████║██╔██╗ ██║    ██████╔╝██║   ██║█████╔╝ "
       "█████╗  ██████╔╝");
  puts("██║██║╚██╗██║██║  ██║██║██╔══██║██║╚██╗██║    ██╔═══╝ ██║   ██║██╔═██╗ "
       "██╔══╝  ██╔══██╗");
  puts("██║██║ ╚████║██████╔╝██║██║  ██║██║ ╚████║    ██║     ╚██████╔╝██║  "
       "██╗███████╗██║  ██║");
  puts("╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝      ╚═════╝ ╚═╝  "
       "╚═╝╚══════╝╚═╝  ╚═");
}

void print_score(int score) {
  printf("\n================\n");
  printf("| Score : %3d  |\n", score);
  printf("================\n\n");
}

int print_flag(void);

int main() {
  int choice;
  int score = 0;

  print_welcome();

  for (int i = 0; i < 99; i++) {
    print_score(score);
    choice = get_choice();
    score = play_poker(score, choice);
    if (score > 99) {
      print_flag();
      return 0;
    }
  }

  return 0;
}
