CPP=g++
CC=gcc
INCLUDE=$(shell pkg-config --cflags opencv)
LIBS=$(shell pkg-config --libs opencv)
all:
	make test_salient
	make Smoothing
	make rect_smooth
test_salient:test_salient.o
	$(CPP) -O3 -o test_salient test_salient.o $(LIBS)
Smoothing: Smoothing.o
	$(CPP) -O3 -o Smoothing Smoothing.o $(LIBS)
rect_smooth: rect_smooth.o
	$(CPP) -O3 -o rect_smooth rect_smooth.o $(LIBS)

.cpp.o:
	$(CPP) $(INCLUDE) -c $< -o $@
.c.o:
	$(CC) $(INCLUDE) -c $< -o $@

clean:
	rm *.o
	rm test_salient
	rm Smoothing
	rm rect_smooth
