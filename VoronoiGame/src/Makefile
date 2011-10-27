# Makefile for Voronoi Problem
# by Uri Nieto and Eric Humphrey
# Fall 2011
#
# Type "make osx" to compile for Mac OSX
# Type "make linux" to compile for Linux

CC= gcc
CFLAGS= -g -Wall -std=c99 
LIBS_OSX= -framework OpenGL -framework GLUT -lm
LIBS_LINUX= -lX11 -lXi -lXmu -lglut -lGL -lGLU -lm  

osx: gameServerOSX client

linux: gameServerLinux client

gameServerOSX: gameServerOSX.o
	$(CC) -o gameServer gameServer.o $(LIBS_OSX) 

gameServerOSX.o: gameServer.c
	$(CC) $(CFLAGS) -D__MACOSX_CORE__ -c gameServer.c

gameServerLinux: gameServerLinux.o
	$(CC) -o gameServer gameServer.c $(LIBS_LINUX) 

gameServerLinux.o: gameServer.c
	$(CC) $(CFLAGS) -c gameServer.c

client: client.c
	$(CC) $(CFLAGS) -D_GNU_SOURCE -o client client.c

clean:
	rm -f client gameServer *.o
