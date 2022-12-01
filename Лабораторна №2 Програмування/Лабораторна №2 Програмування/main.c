#define _CRT_SECURE_NO_WARNINGS
#include <SDL.h>
#include <stdio.h>

const int width = 960;
const int height = 540;
const int lines_in_file = 48802;

void poll_DS7();

int SDL_main(int argc, char* argv[])
{
	if (SDL_Init(SDL_INIT_VIDEO) != 0)
	{
		printf("Error: %s", SDL_GetError());
		SDL_Quit();
		return 0;
	}
	SDL_Window* main_window = SDL_CreateWindow("DS7",
		SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
		width, height, SDL_WINDOW_SHOWN);
	if (main_window == NULL)
	{
		printf("Error: %s", SDL_GetError());
		return 0;
	}
	SDL_Renderer* main_renderer = SDL_CreateRenderer(main_window, -1, 0);
	if (main_renderer == NULL)
	{
		printf("Error: %s", SDL_GetError());
		return 0;
	}
	SDL_SetRenderDrawColor(main_renderer, 255, 255, 255, 0);
	SDL_RenderClear(main_renderer);
	SDL_SetRenderDrawColor(main_renderer, 0, 0, 0, 255);
	FILE* ds7 = fopen("DS7.txt", "r");
	int x, y, temp;
	while (1)
	{
		fscanf(ds7, "%d %d", &x, &y);
		if (feof(ds7))
		{
			break;
		}
		temp = x;
		x = y;
		y = height - temp;
		SDL_RenderDrawPoint(main_renderer, x, y);
	}
	fclose(ds7);
	SDL_RenderPresent(main_renderer);
	poll_DS7();
	SDL_DestroyRenderer(main_renderer);
	SDL_DestroyWindow(main_window);
	SDL_Quit();
	return 0;
}

void poll_DS7()
{
	SDL_Event event;
	do
	{
		SDL_PollEvent(&event);
	} while (event.type != SDL_QUIT);
}