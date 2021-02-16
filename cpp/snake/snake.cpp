#include "SDL2.h"
#include <iostream>

using namespace std;
int screenWidth = 720;
int screenHeight = 480;
main(){
	SDL_Window* window = NULL;
	SDL_Surface* screenSurface = NULL;
	if( SDL_Init( SDL_INIT_VIDEO ) < 0 )
    {
        printf( "SDL could not initialize! SDL_Error: %s\n", SDL_GetError() );
		return 0;
    }
	window = SDL_CreateWindow("Snake", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, screenWidth, screenHeight, SDL_WINDOW_SHOW);
	if(!window){
		printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() );
		return 0;
	}
	while(1){
		screenSurface = SDL_GetWindowSurface( window );
		SDL_FillRect( screenSurface, NULL, SDL_MapRGB( screenSurface->format, 0xFF, 0xFF, 0xFF ) );
		SDL_UpdateWindowSurface( window );
		SDL_Delay( 2000 );
	}
	SDL_DestroyWindow( window );
	SDL_Quit();
	return 0;
}