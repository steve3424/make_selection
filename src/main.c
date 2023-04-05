#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "make_selection.h"

int main() {

	char* options[] = {
		"option 1",
		"option 2",
		"option 3",
		"option 4",
		"option 5",
		0
	};

	int num_options = 0;
	char** p = options;
	while(*p++) {
		++num_options;
	}
	int selected_index = MakeSelection(options, num_options, "options");
	if(selected_index == -1) {
		return 0;
	}

	char* things[] = {
		"thing 1",
		"thing 2",
		"thing 3",
		"thing 4",
		"thing 5",
		0
	};
	int num_things = 0;
	p = things;
	while(*p++) {
		++num_things;
	}
	selected_index = MakeSelection(things, num_things, "things");
	if(selected_index == -1) {
		return 0;
	}

	return 0;
}