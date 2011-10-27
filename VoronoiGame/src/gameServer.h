/*
 * =====================================================================================
 *
 *       Filename:  gameServer.h
 *
 *    Description:  Header file for the game server of Voronoi
 *
 *        Version:  1.0
 *        Created:  10/17/2011 22:42:59
 *       Revision:  none
 *       Compiler:  gcc
 *
 *        Authors:  Uri Nieto, Eric Humphrey
 *
 * =====================================================================================
 */

void myKeyboardFunc( unsigned char key, int x, int y );
void myMouseFunc( int button, int state, int x, int y );

void startGame ( );
void drawScene(void);

void initRendering();
void resizeWindow(int w, int h);
void closeSockets ( );
