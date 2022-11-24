.PHONY: all clean functions
all: functions

functions:
	gcc -fPIC -lm -shared -O3 -o pso.so pso.c


clean:
	rm -f pso.so
