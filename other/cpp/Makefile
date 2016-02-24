CC=g++
CC_OPTS=--std=c++14 -Wall -O2
LIBS=-lpugixml
INC_PATH=
TARGET=count
RM=rm -f
OBJS=main.o graph.o graphGen.o svg.o layout.o

all: $(TARGET)


%.o : %.cpp
	$(CC) -c $(CC_OPTS) $(INC_PATH) $(LIBS) $<

$(TARGET): $(OBJS)
	$(CC) $(CC_OPTS) -o $(TARGET) $(INCLUDE) $(OBJS) $(LIBS)

.PHONY: clean

clean:
	$(RM) *.o
	$(RM) $(TARGET)

