#include <windows.h>
#include <stdio.h>

#define BLUE_FG "\033[34m"
#define YELLOW_FG "\033[33m"
#define WHITE_BG "\033[30;47m"
#define RESET "\033[0m"

static HANDLE stdin_handle;
static int initialized = 0;

static void PrintOptions(char** options, int selection, char* label) {
	printf(BLUE_FG "%s>" RESET "\n", label);

	int i = 0;
	while(options[i])	{
		if(i == selection) {
			printf(WHITE_BG "%s" RESET "\n", options[i]);
		}
		else {
			printf("%s\n", options[i]);
		}
		++i;
	}

	printf(YELLOW_FG "Enter: Select, Ctl+C: Cancel" RESET "\n");
}

static void ResetCursor(int num_options) {
	printf("\033[%dF\r", num_options + 2);
}

static void ClearOptions(int num_options) {
	printf("\033[%dF\r", num_options + 2);
	printf("\033[%dM\r", num_options + 2);
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

	int selection = 0;
	while(1) {
		PrintOptions(options, selection, label);

		INPUT_RECORD ipr;
		DWORD events_read;
		if(!ReadConsoleInputA(stdin_handle, &ipr, 1, &events_read)) {
			printf("Error reading input...\n");
			return 0;
		}

		if(ipr.EventType == KEY_EVENT && ipr.Event.KeyEvent.bKeyDown) {
			if(ipr.Event.KeyEvent.wVirtualKeyCode == VK_RETURN) {
				ClearOptions(num_options);
				printf("%s> %s\n", label, options[selection]);
				return selection;
			}
			else {
				if(ipr.Event.KeyEvent.wVirtualKeyCode == VK_DOWN) {
					selection++;
					selection = selection >= num_options ? num_options - 1 : selection;
				}
				else if(ipr.Event.KeyEvent.wVirtualKeyCode == VK_UP) {
					selection--;
					selection = selection < 0 ? 0 : selection;
				}
				else if(
					(ipr.Event.KeyEvent.dwControlKeyState == LEFT_CTRL_PRESSED || ipr.Event.KeyEvent.dwControlKeyState == RIGHT_CTRL_PRESSED) && 
					 ipr.Event.KeyEvent.wVirtualKeyCode == 0x43
				) {
					ClearOptions(num_options);
					printf("cancelled");
					return -1;
				}
			}
		}

		ResetCursor(num_options);
	}
}
