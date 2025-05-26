import pygame
import sys
import math

from controller import Controller

con = Controller()

# Read in unsorted movies
try:
    with open("unsorted.txt", "r") as f:
        con.unsorted_movies = [line.strip() for line in f.readlines()]

except FileNotFoundError:
    print("unsorted.txt not found. Using a default movie list.")
    con.unsorted_movies = ["Inception", "Men In Tights", "Pulp Fiction", "Shawshank", "Dark Knight"]

def draw_input_box():
    con.screen.fill((30, 30, 30))
    txt_surface = con.text_box_font.render(con.user_text, True, con.color)
    width = max(240, txt_surface.get_width()+10)
    con.input_box.w = width
    con.screen.blit(txt_surface, (con.input_box.x+5, con.input_box.y+5))
    pygame.draw.rect(con.screen, con.color, con.input_box, 2)
    pygame.display.flip()

movie = ""
upper = 0
lower = 0

while con.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            con.running = False
        elif event.type == pygame.KEYDOWN:
            if con.need_user_input and con.typing_in_box:
                if event.key == pygame.K_RETURN:
                    print(f"Username entered: {con.user_text}")
                    # You can now use user_text as the identifier for this session
                    # Break the loop to go to the next phase of your app
                    con.need_user_input = False
                    # pygame.quit()
                    # sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    print("Pressed backspace")
                    con.user_text = con.user_text[:-1]
                    print(con.user_text)
                else:
                    con.user_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:

            movie, upper, lower = con.handle_click(movie,event,upper,lower)

    if(not con.need_user_input):
        if(con.need_get_user_data):
            movie, upper, lower = con.get_user_data(con.user_text)
            movie_1 = con.poster_rect(movie, True)
            mid = (upper+lower)//2
            movie_2 = con.poster_rect(con.sorted_movies[mid], False)

            poster_1, poster_1_left, poster_1_top, con.movie_1_border_left, con.movie_1_border_right, con.movie_1_border_top, con.movie_1_border_bottom = movie_1
            poster_2, poster_2_left, poster_2_top, con.movie_2_border_left, con.movie_2_border_right, con.movie_2_border_top, con.movie_2_border_bottom = movie_2

            con.need_get_user_data = False
        con.drawMovies(movie, upper, lower)
    else:
        draw_input_box()