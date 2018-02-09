CC=g++
INCLUDE=$(shell pkg-config --cflags opencv)
LIBS=$(shell pkg-config --libs opencv)
BINS=smooth_around_video image_align align_image_list smooth_around align_image_list_masks
OBJS= utils.o
all:
	make smooth_around_video
	make image_align
	make align_image_list
	make smooth_around
	make align_image_list_masks
smooth_around_video: smooth_around_video.o $(OBJS)
	$(CC) -O3 -o smooth_around_video smooth_around_video.o $(OBJS) $(LIBS)
image_align: image_align.o
	$(CC) -O3 -o image_align image_align.o $(LIBS)
align_image_list: align_image_list.o
	$(CC) -O3 -o align_image_list align_image_list.o $(LIBS)
smooth_around: smooth_around.o
	$(CC) -O3 -o smooth_around smooth_around.o $(OBJS) $(LIBS)
align_image_list_masks: align_image_list_masks.o $(OBJS)
	$(CC) -O3 -o align_image_list_masks align_image_list_masks.o $(OBJS) $(LIBS)
.cpp.o:
	$(CC) $(INCLUDE) -c $< -o $@
.c.o:
	gcc $(INCLUDE) -c $< -o $@
clean:
	rm smooth_around_video.o image_align.o align_image_list.o smooth_around.o align_image_list_masks.o $(OBJS)
	rm $(BINS)
