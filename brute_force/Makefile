CC=g++
CC_OPTS=-Wall -O3 --std=c++11
LIBS=-lpthread
INC_PATH=
TARGET=brute
RM=rm -f
OBJS=main.o problem.o

all: $(TARGET)


%.o : %.cpp
	$(CC) -c $(CC_OPTS) $(INC_PATH) $(LIBS) $<

$(TARGET): $(OBJS)
	$(CC) $(CC_OPTS) -o $(TARGET) $(INCLUDE) $(OBJS) $(LIBS)

.PHONY: clean

clean:
	$(RM) *.o
	$(RM) $(TARGET)

