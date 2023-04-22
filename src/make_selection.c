#include <windows.h>
#include <stdio.h>

#define BLUE_FG "\033[34m"
#define YELLOW_FG "\033[33m"
#define WHITE_BG "\033[30;47m"
#define RESET "\033[0m"

static HANDLE stdin_handle;
static int initialized = 0;
static int max_window_size = 5;

typedef struct {
	int top;
	int bottom;
} DisplayWindow;

static void PrintOptions(char** options, int selection, DisplayWindow window, char* label) {
	printf(BLUE_FG "%s>" RESET "\n", label);

	for(int i = window.top; i < window.bottom; ++i) {
		if(i == selection) {
			printf(WHITE_BG "%s" RESET "\n", options[i]);
		}
		else {
			printf("%s\n", options[i]);
		}
	}

	printf(YELLOW_FG "Enter: Select, Ctl+C: Cancel" RESET "\n");
}

static void ResetWindow(DisplayWindow window) {
	int lines_to_clear = window.bottom - window.top + 2;
	printf("\033[%dF\r", lines_to_clear);
	printf("\033[%dM\r", lines_to_clear);
}

static void ClearWindow(DisplayWindow window) {
	int lines_to_clear = window.bottom - window.top + 2;
	printf("\033[%dF\r", lines_to_clear);
	printf("\033[%dM\r", lines_to_clear);
}

int MakeSelection(char** options, int num_options, char* label) {
    // Initialize on first run
    if(!initialized) {
        SetConsoleOutputCP(CP_UTF8);
	    stdin_handle = GetStdHandle(STD_INPUT_HANDLE);	
	
	    // Allow ctl+c to be handled by us
	    DWORD cm;
	    GetConsoleMode(stdin_handle, &cm);
	    cm &= ~ENABLE_PROCESSED_INPUT;
	    SetConsoleMode(stdin_handle, cm);

        initialized = 1;
    }

	DisplayWindow window;
	window.top = 0;
	window.bottom = (num_options > max_window_size) ? max_window_size : num_options;

	int selection = 0;
	while(1) {
		PrintOptions(options, selection, window, label);

		INPUT_RECORD ipr;
		DWORD events_read;
		if(!ReadConsoleInputA(stdin_handle, &ipr, 1, &events_read)) {
			printf("Error reading input...\n");
			return 0;
		}

		if(ipr.EventType == KEY_EVENT && ipr.Event.KeyEvent.bKeyDown) {
			if(ipr.Event.KeyEvent.wVirtualKeyCode == VK_RETURN) {
				ClearWindow(window);
				printf("%s> %s\n", label, options[selection]);
				return selection;
			}
			else {
				if(ipr.Event.KeyEvent.wVirtualKeyCode == VK_DOWN) {
					if((selection + 1) < num_options) {
						selection++;
					}

					if(selection == window.bottom) {
						window.top++;
						window.bottom++;
					}
				}
				else if(ipr.Event.KeyEvent.wVirtualKeyCode == VK_UP) {
					if((selection - 1) >= 0) {
						selection--;
					}

					if(selection < window.top) {
						window.top--;
						window.bottom--;
					}
				}
				else if(
					(ipr.Event.KeyEvent.dwControlKeyState == LEFT_CTRL_PRESSED || ipr.Event.KeyEvent.dwControlKeyState == RIGHT_CTRL_PRESSED) && 
					 ipr.Event.KeyEvent.wVirtualKeyCode == 0x43
				) {
					ClearWindow(window);
					printf("cancelled");
					return -1;
				}
			}
		}

		ResetWindow(window);
	}
	return 0;
}
