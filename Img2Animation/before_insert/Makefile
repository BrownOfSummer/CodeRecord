CPP=g++
CC=gcc
INCLUDE=$(shell pkg-config --cflags opencv)
LIBS=$(shell pkg-config --libs opencv)
OBJS=utils.o
all:
	make test_salient
	make Smoothing
	make rect_smooth
	make edge_smooth
	make smooth_around
	make test_mask
	make smooth_around_video
test_salient:test_salient.o
	$(CPP) -O3 -o test_salient test_salient.o $(LIBS)
Smoothing: Smoothing.o
	$(CPP) -O3 -o Smoothing Smoothing.o $(LIBS)
rect_smooth: rect_smooth.o $(OBJS)
	$(CPP) -O3 -o rect_smooth rect_smooth.o $(OBJS) $(LIBS)
edge_smooth: edge_smooth.o $(OBJS)
	$(CPP) -O3 -o edge_smooth edge_smooth.o $(OBJS) $(LIBS)
smooth_around: smooth_around.o $(OBJS)
	$(CPP) -O3 -o smooth_around smooth_around.o $(OBJS) $(LIBS)
test_mask: test_mask.o $(OBJS)
	$(CPP) -O3 -o test_mask test_mask.o $(OBJS) $(LIBS)
smooth_around_video: smooth_around_video.o $(OBJS)
	$(CPP) -O3 -o smooth_around_video smooth_around_video.o $(OBJS) $(LIBS)
smooth_around_video-d: smooth_around_video-d.o $(OBJS)
	$(CPP) -O3 -o smooth_around_video-d smooth_around_video-d.o $(OBJS) $(LIBS)
.cpp.o:
	$(CPP) $(INCLUDE) -c $< -o $@
.c.o:
	$(CC) $(INCLUDE) -c $< -o $@

clean:
	rm *.o
	rm test_salient
	rm rect_smooth
	rm edge_smooth
	rm smooth_around
	rm smooth_around_video-d
	rm smooth_around_video
