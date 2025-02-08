import pygame

import math

pygame.init()

width = 1280
height = 720

vertical_offset = 100

vs_box_width = 350
vs_box_height = 450

#Maximum size of posters
max_poster_width = 300
max_poster_height = 400

border_offset = 25

screen = pygame.display.set_mode((width, height+20))
clock = pygame.time.Clock()
running = True
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
vsfont_size = 100
vsfont = pygame.font.SysFont("monospace", vsfont_size,  pygame.font.Font.bold)
versus = vsfont.render("VS", 1, (255,255,255))

vs_left = width/2 - versus.get_width()/2
vs_right = vs_left + versus.get_width()
vs_top = height/2 - versus.get_height()/2
vs_bottom = vs_top + versus.get_height()

# Initialize font for the Movie Titles found below the posters
moviefont_size = 50
moviefont = pygame.font.SysFont("monospace", moviefont_size)

titlefont_size = 75
titlefont = pygame.font.SysFont("monospace", titlefont_size,  pygame.font.Font.bold)
title = titlefont.render("Which movie is better?", 1, (255, 255, 255))

percentfont_size = 20
percentfont = pygame.font.SysFont("monospace", percentfont_size)

sortprogressfont_size = 50
sortprogressfont = pygame.font.SysFont("monospace", sortprogressfont_size)

skipfont_size = 30
skipfont = pygame.font.SysFont("monospace", skipfont_size,  pygame.font.Font.bold)

deletefont_size = 25
deletefont = pygame.font.SysFont("monospace", deletefont_size)

#Initialize the undo button image, size, and transparency
undo_image = pygame.image.load("C:\\Users\\jonah\\Desktop\\Aidan_Ranking_Project\\Updated_Ranking\\undo_button.png").convert_alpha()
undo_image = pygame.transform.scale(undo_image, (100, 50))
undo_image.set_alpha(75)

# Describe Undo Button location
undo_left = 0
undo_right = undo_left + undo_image.get_width()

undo_top = 0
undo_bottom = undo_top + undo_image.get_height()

def poster_rect(movie, is_left):
    filename = movie.replace(":", " -")
    poster = pygame.image.load("C:\\Users\\jonah\\Desktop\\Aidan_Ranking_Project\\Updated_Ranking\\poster_images\\" + filename + ".jpg").convert()
    poster_width, poster_height = poster.get_size()
    scale_factor = min(max_poster_width / poster_width, max_poster_height / poster_height)
    new_poster_width = int(poster_width * scale_factor)
    new_poster_height = int(poster_height * scale_factor)
    poster = pygame.transform.scale(poster, (new_poster_width, new_poster_height))

    poster_left = width/2 - new_poster_width/2 + (-1 if is_left else 1)*vs_box_width
    poster_top = height/2 - new_poster_height/2

    border_left = poster_left - border_offset
    border_right = poster_left + new_poster_width + border_offset

    border_top = poster_top - border_offset
    border_bottom = poster_top + new_poster_height + border_offset

    return poster, poster_left, poster_top, border_left, border_right, border_top, border_bottom

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left + (rect.width/2-image.get_width()/2), y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

# Read in unsorted movies
try:
    with open("unsorted.txt", "r") as f:
        unsorted_movies = [line.strip() for line in f.readlines()]

except FileNotFoundError:
    print("unsorted.txt not found. Using a default movie list.")
    unsorted_movies = ["Inception", "Men In Tights", "Pulp Fiction", "Shawshank", "Dark Knight"]

# Read in sorted movies
try:
    with open("jonah_sorted.txt", "r") as f:
        sorted_movies = [line.strip() for line in f.readlines()]
        sorted_movies.reverse()

except FileNotFoundError:
    print("jonah_sorted.txt not found. Using a default movie list.")
    sorted_movies = []

total_movies = len(unsorted_movies) + len(sorted_movies)

# Initial Values for movies to rank
movie = unsorted_movies.pop(0)
undo_stack = []
if len(sorted_movies) == 0: # Put first movie from unsorted into sorted
    sorted_movies.append(movie)
    movie = unsorted_movies.pop(0)
upper,lower = len(sorted_movies),0
mid = (upper+lower)//2

def num_compare_undos():
    num_compares = 0
    for undo_record in reversed(undo_stack):
        if undo_record[0] == "compare":
            num_compares += 1
        else:
            break
    return num_compares

movie_1 = poster_rect(movie, True)
movie_2 = poster_rect(sorted_movies[mid], False)

poster_1, poster_1_left, poster_1_top, movie_1_border_left, movie_1_border_right, movie_1_border_top, movie_1_border_bottom = movie_1
poster_2, poster_2_left, poster_2_top, movie_2_border_left, movie_2_border_right, movie_2_border_top, movie_2_border_bottom = movie_2

skip_rect = (width/2 - ((movie_2_border_left-75) - (movie_1_border_right+75))/2, vs_bottom + 50, ((movie_2_border_left-75) - (movie_1_border_right+75)), 100)

delete_rect = (movie_1_border_left - 5, movie_1_border_top - 65, movie_1_border_right - movie_1_border_left + 10, 60)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # print("lower: ", lower)
            # print("upper: ", upper)
            # print("mid: ", mid)
            # print(sorted_movies)
            x,y = pygame.mouse.get_pos()
            if x >= movie_1_border_left and x <= movie_1_border_right and y <= movie_1_border_bottom and y >= movie_1_border_top:
                print(movie + " better than " + sorted_movies[mid])
                undo_stack.append(("compare",upper,lower))
                lower = mid+1
            elif x >= movie_2_border_left and x <= movie_2_border_right and y <= movie_2_border_bottom and y >= movie_2_border_top:
                print(sorted_movies[mid] + " better than " + movie)
                undo_stack.append(("compare",upper,lower))
                upper = mid
            elif x >= undo_left and x <= undo_right and y >= undo_top and y <= undo_bottom:
                if len(undo_stack) == 0:
                    continue
                else:
                    print("undo")
                undo_record = undo_stack.pop()

                if undo_record[0] == "compare":
                    print(undo_record[1])
                    print(undo_record[2])
                    upper,lower = undo_record[1],undo_record[2]
                elif undo_record[0] == "skip":
                    movie = undo_record[1]
                    unsorted_movies.insert(0,movie)
                    unsorted_movies.pop()
                    with open("unsorted.txt", "w") as f:
                        for movie in unsorted_movies:
                            f.write(movie + "\n")
                    movie = unsorted_movies.pop(0)
                    upper,lower = len(sorted_movies),0
                elif undo_record[0] == "delete":
                    movie = undo_record[1]
                    unsorted_movies.insert(0,movie)
                    with open("unsorted.txt", "w") as f:
                        for movie in unsorted_movies:
                            f.write(movie + "\n")
                    movie = unsorted_movies.pop(0)
                    upper,lower = len(sorted_movies),0
                    continue
                elif undo_record[0] == "sort":
                    unsorted_movies.insert(0, movie)
                    movie = undo_record[1]
                    sorted_movies.remove(movie)
                    unsorted_movies.insert(0,movie)
                    with open("jonah_sorted.txt", "w") as f:
                        for movie in reversed(sorted_movies):
                            f.write(movie + "\n")
                    with open("unsorted.txt", "w") as f:
                        for movie in unsorted_movies:
                            f.write(movie + "\n")
                    movie = unsorted_movies.pop(0)
                    compare_undo_sort = undo_stack.pop()
                    upper,lower = compare_undo_sort[1], compare_undo_sort[2]

            elif x >= skip_rect[0] and x <= (skip_rect[0]+skip_rect[2]) and y >= skip_rect[1] and y <= (skip_rect[1] + skip_rect[3]):
                print("Skipped " + movie)
                unsorted_movies.append(movie)
                undo_stack.append(("skip", movie))
                with open("unsorted.txt", "w") as f:
                    for movie in unsorted_movies:
                        f.write(movie + "\n")
                movie = unsorted_movies.pop(0)
                upper,lower = len(sorted_movies),0
                continue
            elif x >= delete_rect[0] and x <= (delete_rect[0]+delete_rect[2]) and y >= delete_rect[1] and y <= (delete_rect[1] + delete_rect[3]):
                print("Deleted " + movie)
                undo_stack.append(("delete", movie))
                with open("unsorted.txt", "w") as f:
                    for movie in unsorted_movies:
                        f.write(movie + "\n")
                movie = unsorted_movies.pop(0)
                upper,lower = len(sorted_movies),0
                continue
            if lower >= upper:
                sorted_movies.insert(lower, movie)
                print("Sorted " + movie)
                undo_stack.append(("sort", movie))
                with open("jonah_sorted.txt", "w") as f:
                    for movie in reversed(sorted_movies):
                        f.write(movie + "\n")
                with open("unsorted.txt", "w") as f:
                    for movie in unsorted_movies:
                        f.write(movie + "\n")
                if len(unsorted_movies) == 0:
                    running = False
                    print("All Done!")
                    continue
                movie = unsorted_movies.pop(0)
                upper,lower = len(sorted_movies),0
            mid = (upper+lower)//2

    movie_1 = poster_rect(movie, True)
    movie_2 = poster_rect(sorted_movies[mid], False)

    poster_1, poster_1_left, poster_1_top, movie_1_border_left, movie_1_border_right, movie_1_border_top, movie_1_border_bottom = movie_1
    poster_2, poster_2_left, poster_2_top, movie_2_border_left, movie_2_border_right, movie_2_border_top, movie_2_border_bottom = movie_2
    
    screen.fill("black")

    #movie_1_text = moviefont.render(movie, 1, (255,255,255))
    movie_1_text_rect = (0, movie_1_border_bottom, vs_left, height - movie_1_border_bottom)
    fontsize = moviefont_size
    font = moviefont
    while drawText(screen, movie, (255,255,255), movie_1_text_rect, font) != "":
        drawText(screen, movie, (0,0,0), movie_1_text_rect, font)
        fontsize = fontsize - 5
        font = pygame.font.SysFont("monospace", fontsize)

    movie_2_text_rect = (vs_right, movie_2_border_bottom, width-vs_right, height - movie_2_border_bottom)
    fontsize = moviefont_size
    font = moviefont
    while drawText(screen, sorted_movies[mid], (255,255,255), movie_2_text_rect, font) != "":
        drawText(screen, sorted_movies[mid], (0,0,0), movie_2_text_rect, font)
        fontsize = fontsize - 5
        font = pygame.font.SysFont("monospace", fontsize)

    pygame.draw.rect(screen, "white", [movie_1_border_left, movie_1_border_top, poster_1.get_width() + (border_offset*2), poster_1.get_height() + (border_offset*2)])
    pygame.draw.rect(screen, "white", [movie_2_border_left, movie_2_border_top, poster_2.get_width() + (border_offset*2), poster_2.get_height() + (border_offset*2)])

    if len(undo_stack) != 0:
        undo_image.set_alpha(255)
    else:
        undo_image.set_alpha(75)
    screen.blit(undo_image, (0,0))

    screen.blit(versus, (width/2 - versus.get_width()/2, height/2 - versus.get_height()/2))

    screen.blit(title, (width/2 - title.get_width()/2, 0))

    screen.blit(poster_1, (poster_1_left, poster_1_top))
    screen.blit(poster_2, (poster_2_left, poster_2_top))

    percent = (total_movies - len(unsorted_movies))/total_movies

    pygame.draw.rect(screen, "white", [0, 720, (percent)*width, 20])
    percent_text = percentfont.render(str(math.floor(percent*100)) + "%", 1, (255,0,0))
    screen.blit(percent_text, (width/2 - percent_text.get_width()/2, 720))

    max_height = movie_1_border_bottom - movie_1_border_top

    pygame.draw.rect(screen, (128,128,128), [movie_1_border_left/2 - 50, movie_1_border_top, 100, max_height])
    pygame.draw.rect(screen, (255,0,0), [movie_1_border_left/2 - 25, movie_1_border_top+25, 50, max_height-25])

    num_compares = num_compare_undos()

    denominator = num_compares + math.floor(1+math.log2(upper-lower))

    sorted_progress = num_compares/denominator
    sorted_progress_y = sorted_progress*max_height
    pygame.draw.rect(screen, (0,255,0), [movie_1_border_left/2 - 25, max_height + movie_1_border_top - sorted_progress_y, 50, sorted_progress_y])

    sortprogress = sortprogressfont.render(str(num_compares) + "/" + str(denominator), 1, (255,255,255))
    screen.blit(sortprogress, (25, movie_1_border_top - sortprogress.get_height()))

    pygame.draw.rect(screen, (255,0,0), pygame.Rect(skip_rect), 0, -1, 10, 10, 10, 10)
    drawText(screen, "Skip This Comparison For Now", (255,255,255), skip_rect, skipfont)

    pygame.draw.rect(screen, (0,0,255), pygame.Rect(delete_rect))
    drawText(screen, "Don't Remember/ Haven't Seen", (255, 255, 255), delete_rect, deletefont)

    pygame.display.flip()