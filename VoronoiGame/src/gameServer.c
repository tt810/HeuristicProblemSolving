/*
 * =====================================================================================
 *
 *       Filename:  gameServer.c
 *
 *    Description:  Server for the game Voronoi for Heuristic Problem Solvimg class
 *
 *        Version:  1.0
 *        Created:  10/17/2011 22:41:44
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Uri Nieto, uri@urinieto.com, Eric Humphrey
 *     University:  New York University
 *      Copyright:  Copyright (c) 2011, Uri Nieto, Eric Humphrey
 *
 * =====================================================================================
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>

#ifdef __MACOSX_CORE__
    #include <GLUT/glut.h>
#else
    #include <GL/glut.h>
#endif

#include "gameServer.h"

#define RED_PLAYER  0
#define BLUE_PLAYER 1
#define BOARD_SIZE  1000
#define PANEL_WIDTH 200
#define MAX_PLAYERS 10
#define MAX_STONES  50

/***** Structs *****/
typedef struct Pos {
    int x;
    int y;
} Pos;

typedef struct Player {
    float color[3];
    Pos stones[MAX_STONES];
    float score;
    int socket;
    int newsocket;
    float time;
    int port;
    int connected;
} Player;

/***** Globals *****/
int g_game_started = 0;
int g_sockets_init = 0;
int g_curr_player = 0;
int g_curr_turn = 0;
int g_num_turns;
int g_waiting = 0;
pthread_mutex_t g_mutex = PTHREAD_MUTEX_INITIALIZER;
float g_x = -1;
float g_y = -2;
Player g_players[MAX_PLAYERS];
int g_num_players;

// These variables set the dimensions of the rectanglar region we wish to view.
const double Xmin = 0.0, Xmax = BOARD_SIZE + PANEL_WIDTH;
const double Ymin = 0.0, Ymax = BOARD_SIZE;


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  myMouseFunc
 *  Description:  
 * =====================================================================================
 */
void myMouseFunc( int button, int state, int x, int y ) {
    
    double w_x, w_y, w_z;
    float margin = 20.f;
    float button_height = 60.0f;
    GLint viewport[4];
    GLdouble modelview[16],projection[16];

//    printf("Mouse: button: %d, state: %d, x: %d, y: %d\n", button, state, x, y );

    if ( button == GLUT_LEFT_BUTTON && state == GLUT_UP ) {
        /* Translate positions of the mouse */
        glGetIntegerv(GL_VIEWPORT, viewport);
        glGetDoublev(GL_MODELVIEW_MATRIX, modelview);
        glGetDoublev(GL_PROJECTION_MATRIX, projection);
        gluUnProject(x, viewport[3] - y, -0.1, modelview, projection, viewport, &w_x, &w_y, &w_z);

        /* If we're pressing on top of the start button, let's start */
        if ( !g_game_started && w_x > BOARD_SIZE + margin && 
                w_x < BOARD_SIZE + PANEL_WIDTH + margin &&
                w_y > margin && w_y < margin + button_height ) {

            /* No button anymore, just automatic start when players are ready */
//            printf("Starting Game...\n");
//            startGame();
        }
    }
}		
/* -----  end of function myMouseFunc  ----- */
/*
 * ===  FUNCTION  ======================================================================
 *         Name:  myKeyboardFunc
 *  Description:  
 * =====================================================================================
 */
void myKeyboardFunc( unsigned char key, int x, int y )
{
	switch ( key ) {

	case ' ':
        /* Space Bar */
		break;

    case 13:
        /* Enter */
        startGame( );
        break;
	case 27:
        /* Escape key */
        closeSockets();
		exit(1);

	}
}
/* -----  end of function myKeyboardFunc  ----- */


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  drawBoard
 *  Description:  
 * =====================================================================================
 */
void drawBoard (  ) {
    
    float offset = 5.0f; 

    /* Background color of the Board */
    glColor3f( .2, .2, .2 );

    /* Draw a Square */
    glBegin(GL_POLYGON);
        glVertex3f(0.0f - offset, 0.0f - offset, -0.5f);
        glVertex3f(0.0f - offset, BOARD_SIZE, -0.5f);
        glVertex3f(BOARD_SIZE + offset, BOARD_SIZE + offset, -0.5f);
        glVertex3f(BOARD_SIZE + offset, 0.0f - offset, -0.5f);
    glEnd();
}		
/* -----  end of function drawBoard  ----- */


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  drawPlayers
 *  Description:  
 * =====================================================================================
 */
void drawPlayers ( ) {
    
    int i, j, len;
    float *color;
    float margin = 20.0f;
    float player_size = 40.0f;
    char string[256];

    for ( i = 0; i < g_num_players; i++ ) {
           
        color = g_players[i].color;

        /* Draw the background */
        glBegin( GL_POLYGON );
            glColor3f( color[0], color[1], color[2] );
            glVertex3f( BOARD_SIZE + margin, BOARD_SIZE - (i + 1) * margin - (i + 1) * player_size, -0.4f );
            glVertex3f( BOARD_SIZE + margin, BOARD_SIZE - (i + 1) * margin - i * player_size, -0.4f );
            glColor3f( color[0]*0.7, color[1]*0.7, color[2] * 0.7 );
            glVertex3f( BOARD_SIZE + PANEL_WIDTH - margin, BOARD_SIZE - (i + 1) * margin - i * player_size, -0.4f );
            glVertex3f( BOARD_SIZE + PANEL_WIDTH - margin, BOARD_SIZE - (i + 1) * margin - (i + 1) * player_size, -.4f );
        glEnd();

        /* Draw the string */
        glColor3f( color[0]*1.5, color[1]*1.5, color[2]*1.5 );
        glRasterPos2f(BOARD_SIZE + margin + 33, BOARD_SIZE - (i + 1) * margin - (i + 1) * player_size + 10 );
        if ( g_players[i].connected ) {
            sprintf( string, "Player %d", i );
        }
        else {
            sprintf( string, "Waiting...");
        }
        len = (int)strlen(string);
        for (j = 0; j < len; j++) {
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, string[j]);
        }
    }
}		
/* -----  end of function drawPlayers  ----- */


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  drawStartButton
 *  Description:  
 * =====================================================================================
 */
void drawStartButton ( ) {
        
    int len, j;
    float margin = 20.f;
    float button_height = 60.f;
    char string[256];

    /* Draw the background */
    glBegin( GL_POLYGON );
        glColor3f( 0.5f, 0.6f, 0.6f );
        glVertex3f( BOARD_SIZE + margin, margin, -0.4f );
        glVertex3f( BOARD_SIZE + margin, margin + button_height, -0.4f );
        glColor3f( 0.6f, 0.6f, 0.6f );
        glVertex3f( BOARD_SIZE + PANEL_WIDTH - margin, margin + button_height, -0.4f );
        glVertex3f( BOARD_SIZE + PANEL_WIDTH - margin, margin, -0.4f);
    glEnd();

    /* Draw the string */
    glColor3f( 0.2f, 0.2f, 0.2f );
    if ( g_game_started ) {
        glRasterPos2f (BOARD_SIZE + margin + 40,  margin + 25 );
        sprintf( string, "Running" );
    }
    else if ( g_curr_turn == 0 ) {
        glRasterPos2f (BOARD_SIZE + margin + 35,  margin + 25 );
        sprintf( string, "Waiting..." );
    }
    else if ( g_curr_turn > 0 ) {
        glRasterPos2f (BOARD_SIZE + margin + 35,  margin + 25 );
        sprintf( string, "Finished!" );
        printf("End of Game!\n");
        /* TODO: Say who wins! */
    }
    len = (int)strlen(string);
    for (j = 0; j < len; j++) {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, string[j]);
    }
    
}		
/* -----  end of function drawStartButton  ----- */

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  drawPanel
 *  Description:  
 * =====================================================================================
 */
void drawPanel (  ) {
    
    /* Draw Background */
    glColor3f( .15, .15, .15 );
    glBegin( GL_POLYGON );
        glVertex3f( BOARD_SIZE, 0.0f, -0.5f );
        glVertex3f( BOARD_SIZE, BOARD_SIZE, -0.5f );
        glColor3f( .2, .2, .2 );
        glVertex3f( BOARD_SIZE + PANEL_WIDTH, BOARD_SIZE, -0.5f );
        glVertex3f( BOARD_SIZE + PANEL_WIDTH, 0.0f, -0.5f );
    glEnd();

    /* Draw Players */
    drawPlayers();

    /* Draw Start Button */
    drawStartButton( );
}		
/* -----  end of function drawPanel  ----- */

/*
 * drawScene() handles the animation and the redrawing of the
 *		graphics window contents.
 */
void drawScene(void)
{
    int i, k, x, y;
    float *color;

	// Clear the rendering window
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    /* Draw Board */
    drawBoard( );

    /* Draw Panel */
    drawPanel( );

    /* Draw the stones of all turns */
    glBegin(GL_POINTS);
    for ( i = 0; i < g_curr_turn + 1; i++ ) {
        /* For all players */
        for ( k = 0; k < g_num_players; k++ ) {
            /* Draw if the player has already played this turn */
            if ( i < g_curr_turn || (k < g_curr_player && i == g_curr_turn) ) {
                x = g_players[k].stones[i].x;
                y = g_players[k].stones[i].y;
                color = g_players[k].color;
                glColor3f( color[0], color[1], color[2] );
                glVertex2f( x, y );
            }
        }
    }
    glEnd();

	// Flush the pipeline.  (Not usually necessary.)
	glFlush();

}

// Initialize OpenGL's rendering modes
void initRendering() {
	glEnable ( GL_DEPTH_TEST );

	// The following commands should cause points and line to be drawn larger
	//	than a single pixel width.
	glPointSize(8);
	glLineWidth(3);

	// The following commands should induce OpenGL to create round points and 
	//	antialias points and lines.  (This is implementation dependent unfortunately).
	glEnable(GL_POINT_SMOOTH);
	glEnable(GL_LINE_SMOOTH);
	glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);	// Make round points, not square points
	glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);		// Antialias the lines
	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

}

// Called when the window is resized
//		w, h - width and height of the window in pixels.
void resizeWindow(int w, int h)
{
	double scale, center;
	double windowXmin, windowXmax, windowYmin, windowYmax;

	// Define the portion of the window used for OpenGL rendering.
	glViewport( 0, 0, w, h );	// View port uses whole window

	// Set up the projection view matrix: orthographic projection
	// Determine the min and max values for x and y that should appear in the window.
	// The complication is that the aspect ratio of the window may not match the
	//		aspect ratio of the scene we want to view.
	w = (w==0) ? 1 : w;
	h = (h==0) ? 1 : h;
	if ( (Xmax-Xmin)/w < (Ymax-Ymin)/h ) {
		scale = ((Ymax-Ymin)/h)/((Xmax-Xmin)/w);
		center = (Xmax+Xmin)/2;
		windowXmin = center - (center-Xmin)*scale;
		windowXmax = center + (Xmax-center)*scale;
		windowYmin = Ymin;
		windowYmax = Ymax;
	}
	else {
		scale = ((Xmax-Xmin)/w)/((Ymax-Ymin)/h);
		center = (Ymax+Ymin)/2;
		windowYmin = center - (center-Ymin)*scale;
		windowYmax = center + (Ymax-center)*scale;
		windowXmin = Xmin;
		windowXmax = Xmax;
	}
	
	// Now that we know the max & min values for x & y that should be visible in the window,
	//		we set up the orthographic projection.
	glMatrixMode( GL_PROJECTION );
	glLoadIdentity();
	glOrtho( windowXmin, windowXmax, windowYmin, windowYmax, -1, 1 );
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  error
 *  Description:  
 * =====================================================================================
 */
void error ( const char *msg ) {
    perror(msg);
    exit(1);
}		
/* -----  end of function error  ----- */


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  openPort
 *  Description:  
 * =====================================================================================
 */
void openPort ( int portno, int *sockfd, int *newsockfd ) {
    
     struct sockaddr_in serv_addr;
     socklen_t clilen;
     struct sockaddr_in cli_addr;

     *sockfd = socket(AF_INET, SOCK_STREAM, 0);
     if (sockfd < 0) 
        error("ERROR opening socket");
     memset((char *) &serv_addr, 0, sizeof(char) * sizeof(serv_addr));
     serv_addr.sin_family = AF_INET;
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     serv_addr.sin_port = htons(portno);
     if (bind(*sockfd, (struct sockaddr *) &serv_addr,
              sizeof(serv_addr)) < 0) 
              error("ERROR on binding");


     /* Listen and wait for the client to connect */
     listen(*sockfd,5);
     
     clilen = sizeof(cli_addr);
     *newsockfd = accept(*sockfd, 
                 (struct sockaddr *) &cli_addr, 
                 &clilen);
     if (*newsockfd < 0) 
          error("ERROR on accept");

}		
/* -----  end of function openPort  ----- */


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  closeSockets
 *  Description:  
 * =====================================================================================
 */
void closeSockets (  ) {
    
    int i;

    for ( i = 0; i < g_num_players; i++ ) {
        close( g_players[i].newsocket );
        close( g_players[i].socket );
    }
}		
/* -----  end of function closeSockets  ----- */


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  storePoint
 *  Description:  
 * =====================================================================================
 */
void storePoint ( Pos p ) {
    g_players[g_curr_player].stones[g_curr_turn].x = p.x;
    g_players[g_curr_player].stones[g_curr_turn].y = p.y;
}		
/* -----  end of function storePoint  ----- */


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  printGlobals
 *  Description:  
 * =====================================================================================
 */
void printGlobals ( char buffer[1024] ) {

    char tmp[64];
    int i;

    strcpy( buffer, "GLOBALS\n" );
    sprintf( tmp, "Total Turns: %d\n", g_num_turns );
    strcat( buffer, tmp );
    sprintf( tmp, "Total Players: %d\n", g_num_players );
    strcat( buffer, tmp );
    sprintf( tmp, "You are Player: %d\n", g_curr_player );
    strcat( buffer, tmp );

    /* Player Scores */
    strcat( buffer, "\nPLAYER SCORES\n" );
    for ( i = 0; i < g_num_players; i++ ) {
        sprintf( tmp, "%d: %g\n", i, g_players[i].score );
        strcat( buffer, tmp );
    }

}		
/* -----  end of function printGlobals  ----- */

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  printCurrentBoard
 *  Description:  
 * =====================================================================================
 */
void printCurrentBoard ( char buffer[1024] ) {  
    
    char tmp[64];
    int i, k;

    strcat( buffer, "\nBOARD STATE\n");
    for ( i = 0; i < g_curr_turn + 1; i++ ) {
        /* For all players */
        for ( k = 0; k < g_num_players; k++ ) {
        /* Get the positions */
            if ( i < g_curr_turn || (k < g_curr_player && i == g_curr_turn) ) {
                sprintf( tmp, "%d: %d %d\n", k, 
                        g_players[k].stones[i].x, 
                        g_players[k].stones[i].y );
                strcat( buffer, tmp );
            }
        }
    }

    strcat( buffer, "\nEnter new position \"X Y\":" );
}		
/* -----  end of function printCurrentBoard  ----- */

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  nextPlayer
 *  Description:  
 * =====================================================================================
 */
void nextPlayer ( ) {
    g_curr_player = ( g_curr_player + 1 ) % g_num_players;
    if ( g_curr_player == 0 ) {
        g_curr_turn++;
    }
}		
/* -----  end of function nextPlayer  ----- */

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  parseMessage
 *  Description:  
 * =====================================================================================
 */
void parseMessage ( char buffer[1024] ) {
    
    Pos p;

    sscanf( buffer, "%d %d", &p.x, &p.y );
    printf("New point: (%d, %d)\n", p.x, p.y);
    if ( p.x < 0 || p.x >= BOARD_SIZE ||
        p.y < 0 || p.y >= BOARD_SIZE ) {
        printf("Error: Incorrect coordenates! (must be two integers from 0 to 999 separated by a space)\n");
        exit(1);
    }

    /* Store point */
    storePoint( p );

    /* Next player */
    nextPlayer( );
}		
/* -----  end of function parseMessage  ----- */

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  listenToSocket
 *  Description:  
 * =====================================================================================
 */
void *listenToSocket ( void *arg ) {

     int newsockfd, n, sockfd;
     char buffer[1024];

     sockfd = g_players[g_curr_player].socket;
     newsockfd = g_players[g_curr_player].newsocket;

     /* Send Globals and Board State */
     memset( buffer, 0,  sizeof(char) * 1024);
     printGlobals( buffer );
     printCurrentBoard( buffer );
     n = write(newsockfd,buffer,strlen(buffer));
     printf("Sent: %d\n", n);
     if (n < 0) error("ERROR writing to socket");
     
     /* Lock */
     pthread_mutex_lock(&g_mutex);

     /* Receive new message */
     memset( buffer, 0, sizeof(char) * 1024);
     n = read(newsockfd,buffer,1023);
     if (n < 0) error("ERROR reading from socket");

     /* Parse message and manage turn */
     parseMessage( buffer );

     /* Redraw */
     glutPostRedisplay();

     g_waiting = 0;

     /* Unlock */
     pthread_mutex_unlock(&g_mutex);

     return NULL;
}	
/* -----  end of function listenToPort1  ----- */


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  initSockets
 *  Description:  This function blocks the system until all connections are established
 * =====================================================================================
 */
void *initSockets(  ) {
    int i;

    for ( i = 0; i < g_num_players; i++ ) {
        openPort( g_players[i].port, &g_players[i].socket, &g_players[i].newsocket );
        g_players[i].connected = 1;
        glutPostRedisplay( );
    }

    /* Uncoment this if you want to start right away after all players are connected */
    startGame( );

    return NULL;
}
/* -----  end of function ,nitSockets  ----- */

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  idleCallback
 *  Description:  This callback gets called repeatedly. Check for new inputs and update
 *                the graphics, and listen to the other socket
 * =====================================================================================
 */
void idleCallback (  ) {
    
    pthread_t pth;
    Player p;

    if ( !g_sockets_init ) {
        g_sockets_init = 1;
        pthread_create( &pth, NULL, initSockets, NULL );
    }

    if ( g_game_started ) {
        if ( g_curr_turn == g_num_turns ) {
            /* Game Ended! */
            closeSockets( );
            g_game_started = 0;
        }
        else if ( !g_waiting ) {
            /* Next Player */
            g_waiting = 1;
            pthread_mutex_lock(&g_mutex);
            p = g_players[g_curr_player];
            printf("Listening to player %d port...\n", g_curr_player);
            pthread_create( &pth, NULL, listenToSocket, NULL );
            pthread_mutex_unlock(&g_mutex);
        }
    }
}		
/* -----  end of function idleCallback  ----- */

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  startGame
 *  Description:  
 * =====================================================================================
 */
void startGame ( ) {
    
    /* Start the game */
    g_game_started = 1;

    /* Redraw */
    glutPostRedisplay();

    printf("Game Started!\n");
}		
/* -----  end of function startGame  ----- */

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  initGraphics
 *  Description:  
 * =====================================================================================
 */
void initGraphics ( int argc, char **argv ) {
    
	glutInit( &argc, argv );

	// The image is not animated so single buffering is OK. 
	glutInitDisplayMode( GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH );

	// Window position (from top corner), and size (width and hieght)
	glutInitWindowPosition( 40, 60 );
	glutInitWindowSize( (BOARD_SIZE + PANEL_WIDTH ) / 2, BOARD_SIZE / 2 );
	glutCreateWindow( "Voronoi Game" );

	// Initialize OpenGL as we like it..
	initRendering();

	// Set up callback functions for key presses
	glutKeyboardFunc( myKeyboardFunc );			// Handles "normal" ascii symbols
	// glutSpecialFunc( mySpecialKeyFunc );		// Handles "special" keyboard keys
    
    /* Set up mouse callback */
    glutMouseFunc( myMouseFunc );

	// Set up the callback function for resizing windows
	glutReshapeFunc( resizeWindow );

	// Call this for background processing
	glutIdleFunc( idleCallback );

	// call this whenever window needs redrawing
	glutDisplayFunc( drawScene );
}		
/* -----  end of function initGraphics  ----- */


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  initPlayers
 *  Description:  
 * =====================================================================================
 */
void initPlayers ( int n_players, char *argv[] ) {
    
    int i;
    float r, brightness = 1.2;

    g_num_players = n_players;
    g_curr_player = 0;
    g_curr_turn = 0;
    g_num_turns = atoi( argv[1] );

    for ( i = 0; i < n_players; i++ ) {
        g_players[i].score = 0.0;
        g_players[i].time = 0.0;
        g_players[i].port = atoi( argv[i+2] );
        g_players[i].connected = 0;
        if ( i == 0 ) {
            /* Red */
            g_players[i].color[0] = .8;
            g_players[i].color[1] = .3;
            g_players[i].color[2] = .3;
        }
        else if ( i == 1 ) {
            /* Blue */
            g_players[i].color[0] = .3;
            g_players[i].color[1] = .3;
            g_players[i].color[2] = .8;
        }
        else {
            /* Random with a minimum brightness*/
            do {
                g_players[i].color[0] = (float)rand()/(float)RAND_MAX;
                g_players[i].color[1] = (float)rand()/(float)RAND_MAX;
                g_players[i].color[2] = (float)rand()/(float)RAND_MAX;
                r = g_players[i].color[0] + g_players[i].color[1] + g_players[i].color[2];
            } while ( r < brightness );
        }
    }
}		
/* -----  end of function initPlayers  ----- */

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  main
 *  Description:  
 * =====================================================================================
 */
int main ( int argc, char *argv[] ) {
    
    int port1, port2;

    /* Check for error in input */
    if ( argc < 4 || argc > MAX_PLAYERS + 2 ) {
        printf("Usage: %s N port1 port2 [port3 ... port%d] \n", argv[0], MAX_PLAYERS);
        printf("  N: Number of turns\n");
        printf("  portn: Port for player\n");
        exit(1);
    }

    /* Seed the random */
    srand( (unsigned)time(0) );

    /* Read ports */
    port1 = atoi( argv[1] );
    port2 = atoi( argv[2] );

    /* Init Players */
    initPlayers( argc - 2, argv );

    /* Init Graphics */
    initGraphics( argc, argv );

    /* Print Message */
    printf("Run all the players with their specific ports and press Enter or click Start.");

	/* Start the main loop.  glutMainLoop never returns */
	glutMainLoop( );

    /* We should never get here */
    return EXIT_SUCCESS;
}				
