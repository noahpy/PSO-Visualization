.PHONY: all clean functions
all: functions

functions:
	gcc -fPIC -lm -shared -o functions.so functions.c


clean:
	rm -f functions.so
