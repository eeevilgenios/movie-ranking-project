import pygame
import math

class Controller:
    def __init__(self):
        pygame.init()

        #Set width and height of pygame screen
        self.width = 1280
        self.height = 720

        # Input box setup
        self.input_box_width = 240
        self.input_box_height = 50
        self.input_box_left = self.width/2 - self.input_box_width/2
        self.input_box_top = self.height/2 - self.input_box_height/2
        self.input_box = pygame.Rect(self.input_box_left, self.input_box_top, self.input_box_width, self.input_box_height)
        self.text_box_font = pygame.font.Font(None, 48)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.need_user_input = True
        self.typing_in_box = False
        self.user_text = ''

        self.need_get_user_data = True

        #This allows for the total completeion bar at the bottom of the screen by movieng everything up to make room
        self.vertical_offset = 100

        #Height an width of "vs" text
        self.vs_box_width = 350
        self.vs_box_height = 450

        #Maximum size of posters
        self.max_poster_width = 300
        self.max_poster_height = 400

        #Size of the border around the movie posters
        self.border_offset = 25

        #Initialize screen
        self.screen = pygame.display.set_mode((self.width, self.height+20))
        self.clock = pygame.time.Clock()
        self.running = True

        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        self.vsfont_size = 100
        self.vsfont = pygame.font.SysFont("monospace", self.vsfont_size,  pygame.font.Font.bold)
        self.versus = self.vsfont.render("VS", 1, (255,255,255))

        #Set location of the "vs" on the screen
        self.vs_left = self.width/2 - self.versus.get_width()/2
        self.vs_right = self.vs_left + self.versus.get_width()
        self.vs_top = self.height/2 - self.versus.get_height()/2
        self.vs_bottom = self.vs_top + self.versus.get_height()

        # Initialize font for the Movie Titles found below the posters
        self.moviefont_size = 50
        self.moviefont = pygame.font.SysFont("monospace", self.moviefont_size)

        #Initialize font for the top text
        self.titlefont_size = 75
        self.titlefont = pygame.font.SysFont("monospace", self.titlefont_size,  pygame.font.Font.bold)
        self.title = self.titlefont.render("Which movie is better?", 1, (255, 255, 255))

        #Initialize fonts for various texts on the screen
        self.percentfont_size = 20
        self.percentfont = pygame.font.SysFont("monospace", self.percentfont_size)

        self.sortprogressfont_size = 50
        self.sortprogressfont = pygame.font.SysFont("monospace", self.sortprogressfont_size)

        self.skipfont_size = 30
        self.skipfont = pygame.font.SysFont("monospace", self.skipfont_size,  pygame.font.Font.bold)

        self.deletefont_size = 25
        self.deletefont = pygame.font.SysFont("monospace", self.deletefont_size)

        #Initialize the undo button image, size, and transparency
        self.undo_image = pygame.image.load("C:\\Users\\jonah\\Desktop\\Aidan_Ranking_Project\\Updated_Ranking\\undo_button.png").convert_alpha()
        self.undo_image = pygame.transform.scale(self.undo_image, (100, 50))
        self.undo_image.set_alpha(75)

        # Describe Undo Button location
        self.undo_left = 0
        self.undo_right = self.undo_left + self.undo_image.get_width()

        self.undo_top = 0
        self.undo_bottom = self.undo_top + self.undo_image.get_height()

        self.undo_stack = []

        self.movie_1_border_bottom = 0
        self.movie_1_border_left = 0
        self.movie_1_border_right = 0
        self.movie_1_border_top = 0

        self.movie_2_border_bottom = 0
        self.movie_2_border_left = 0
        self.movie_2_border_right = 0
        self.movie_2_border_top = 0

        self.sorted_movies = []
        self.unsorted_movies = []

        self.txt_file = ""
        self.total_movies = 0

    #this function finds and creates the movie posters on the screen and places them in the right place
    def poster_rect(self, movie, is_left):
        filename = movie.replace(":", " -")
        poster = pygame.image.load("C:\\Users\\jonah\\Desktop\\Aidan_Ranking_Project\\Updated_Ranking\\poster_images\\" + filename + ".jpg").convert()
        poster_width, poster_height = poster.get_size()
        scale_factor = min(self.max_poster_width / poster_width, self.max_poster_height / poster_height)
        new_poster_width = int(poster_width * scale_factor)
        new_poster_height = int(poster_height * scale_factor)
        poster = pygame.transform.scale(poster, (new_poster_width, new_poster_height))

        poster_left = self.width/2 - new_poster_width/2 + (-1 if is_left else 1)*self.vs_box_width
        poster_top = self.height/2 - new_poster_height/2

        border_left = poster_left - self.border_offset
        border_right = poster_left + new_poster_width + self.border_offset

        border_top = poster_top - self.border_offset
        border_bottom = poster_top + new_poster_height + self.border_offset

        return poster, poster_left, poster_top, border_left, border_right, border_top, border_bottom

    #This function defines how to draw the font and ho to wrap it in a specified area
    def drawText(self, surface, text, color, rect, font, aa=False, bkg=None):
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
    
    def num_compare_undos(self):
        num_compares = 0
        for undo_record in reversed(self.undo_stack):
            if undo_record[0] == "compare":
                num_compares += 1
            else:
                break
        return num_compares

    def drawMovies(self, movie, upper, lower):
        mid = (upper+lower)//2
        #assigns variables to images and sizes of movie posters
        poster_1, poster_1_left, poster_1_top, self.movie_1_border_left, self.movie_1_border_right, self.movie_1_border_top, self.movie_1_border_bottom = self.poster_rect(movie, True)
        poster_2, poster_2_left, poster_2_top, self.movie_2_border_left, self.movie_2_border_right, self.movie_2_border_top, self.movie_2_border_bottom = self.poster_rect(self.sorted_movies[mid], False)
        
        self.screen.fill("black")

        #write the names of the movies below the movies
        movie_1_text_rect = (0, self.movie_1_border_bottom, self.vs_left, self.height - self.movie_1_border_bottom)
        fontsize = self.moviefont_size
        font = self.moviefont
        while self.drawText(self.screen, movie, (255,255,255), movie_1_text_rect, font) != "":
            self.drawText(self.screen, movie, (0,0,0), movie_1_text_rect, font)
            fontsize = fontsize - 5
            font = pygame.font.SysFont("monospace", fontsize)

        movie_2_text_rect = (self.vs_right, self.movie_2_border_bottom, self.width-self.vs_right, self.height - self.movie_2_border_bottom)
        fontsize = self.moviefont_size
        font = self.moviefont
        while self.drawText(self.screen, self.sorted_movies[mid], (255,255,255), movie_2_text_rect, font) != "":
            self.drawText(self.screen, self.sorted_movies[mid], (0,0,0), movie_2_text_rect, font)
            fontsize = fontsize - 5
            font = pygame.font.SysFont("monospace", fontsize)

        #draw poster borders
        pygame.draw.rect(self.screen, "white", [self.movie_1_border_left, self.movie_1_border_top, poster_1.get_width() + (self.border_offset*2), poster_1.get_height() + (self.border_offset*2)])
        pygame.draw.rect(self.screen, "white", [self.movie_2_border_left, self.movie_2_border_top, poster_2.get_width() + (self.border_offset*2), poster_2.get_height() + (self.border_offset*2)])

        #draw undo button
        if len(self.undo_stack) != 0:
            self.undo_image.set_alpha(255)
        else:
            self.undo_image.set_alpha(75)
        self.screen.blit(self.undo_image, (0,0))

        #draw versus
        self.screen.blit(self.versus, (self.width/2 - self.versus.get_width()/2, self.height/2 - self.versus.get_height()/2))

        #draw title
        self.screen.blit(self.title, (self.width/2 - self.title.get_width()/2, 0))

        #draw posters
        self.screen.blit(poster_1, (poster_1_left, poster_1_top))
        self.screen.blit(poster_2, (poster_2_left, poster_2_top))


        percent = (self.total_movies - len(self.unsorted_movies))/self.total_movies

        pygame.draw.rect(self.screen, "white", [0, 720, (percent)*self.width, 20])
        percent_text = self.percentfont.render(str(math.floor(percent*100)) + "%", 1, (255,0,0))
        self.screen.blit(percent_text, (self.width/2 - percent_text.get_width()/2, 720))

        max_height = self.movie_1_border_bottom - self.movie_1_border_top

        pygame.draw.rect(self.screen, (128,128,128), [self.movie_1_border_left/2 - 50, self.movie_1_border_top, 100, max_height])
        pygame.draw.rect(self.screen, (255,0,0), [self.movie_1_border_left/2 - 25, self.movie_1_border_top+25, 50, max_height-25])

        num_compares = self.num_compare_undos()

        denominator = num_compares + math.floor(1+math.log2(upper-lower))

        sorted_progress = num_compares/denominator
        sorted_progress_y = sorted_progress*max_height
        pygame.draw.rect(self.screen, (0,255,0), [self.movie_1_border_left/2 - 25, max_height + self.movie_1_border_top - sorted_progress_y, 50, sorted_progress_y])

        sortprogress = self.sortprogressfont.render(str(num_compares) + "/" + str(denominator), 1, (255,255,255))
        self.screen.blit(sortprogress, (25, self.movie_1_border_top - sortprogress.get_height()))

        pygame.draw.rect(self.screen, (255,0,0), self.skip_rect(), 0, -1, 10, 10, 10, 10)
        self.drawText(self.screen, "Skip This Comparison For Now", (255,255,255), self.skip_rect(), self.skipfont)

        pygame.draw.rect(self.screen, (0,0,255), self.delete_rect())
        self.drawText(self.screen, "Don't Remember/ Haven't Seen", (255, 255, 255), self.delete_rect(), self.deletefont)
        pygame.display.flip()

    def is_undo_click(self,x,y):
        return x >= self.undo_left and x <= self.undo_right and y >= self.undo_top and y <= self.undo_bottom
    
    def is_movie_1_click(self, x, y):
        return x >= self.movie_1_border_left and x <= self.movie_1_border_right and y <= self.movie_1_border_bottom and y >= self.movie_1_border_top
    
    def is_movie_2_click(self, x, y):
        return x >= self.movie_2_border_left and x <= self.movie_2_border_right and y <= self.movie_2_border_bottom and y >= self.movie_2_border_top
    
    def skip_rect(self):
        return pygame.Rect(self.width/2 - ((self.movie_2_border_left-75) - (self.movie_1_border_right+75))/2, self.vs_bottom + 50, ((self.movie_2_border_left-75) - (self.movie_1_border_right+75)), 100)

    def is_skip_click(self, x, y):
        r = self.skip_rect()
        return is_in_rect(r,x,y)
    
    def delete_rect(self):
        return pygame.Rect(self.movie_1_border_left - 5, self.movie_1_border_top - 65, self.movie_1_border_right - self.movie_1_border_left + 10, 60)

    def is_delete_click(self, x, y):
        d = self.delete_rect()
        return is_in_rect(d,x,y)
    
    def get_user_data(self, user_text):
        self.txt_file = user_text.lower() + "_sorted.txt"
        try:
            with open(self.txt_file, "r") as f:
                self.sorted_movies = [line.strip() for line in f.readlines()]
                self.sorted_movies.reverse()

        except FileNotFoundError:
            print(self.txt_file + " not found. Using an empty list.")
            with open(self.txt_file, "w") as f:
                f.write("")
                self.sorted_movies = []
        self.total_movies = len(self.unsorted_movies) + len(self.sorted_movies)

        # Initial Values for movies to rank
        movie = self.unsorted_movies.pop(0)
        self.undo_stack = []
        if len(self.sorted_movies) == 0: # Put first movie from unsorted into sorted
            self.sorted_movies.append(movie)
            movie = self.unsorted_movies.pop(0)
        upper,lower = len(self.sorted_movies),0
        return movie, upper, lower

    def handle_click(self, movie, event, upper, lower):
        mid = (upper+lower)//2
        x,y = pygame.mouse.get_pos()
        if self.need_user_input:
            if self.input_box.collidepoint(event.pos):
                self.typing_in_box = not self.typing_in_box
            else:
                self.typing_in_box = False
            self.color = self.color_active if self.typing_in_box else self.color_inactive
        else:
            if self.is_movie_1_click(x,y):
                print(movie + " better than " + self.sorted_movies[mid])
                self.undo_stack.append(("compare",upper,lower))
                print(lower)
                lower = mid+1
                print(lower)
            elif self.is_movie_2_click(x,y):
                print(self.sorted_movies[mid] + " better than " + movie)
                self.undo_stack.append(("compare",upper,lower))
                print(upper)
                upper = mid
                print(upper)
            elif self.is_undo_click(x,y):
                if len(self.undo_stack) == 0:
                    return movie, upper, lower #come back to this later
                else:
                    print("undo")
                undo_record = self.undo_stack.pop()

                if undo_record[0] == "compare":
                    print(undo_record[1])
                    print(undo_record[2])
                    upper,lower = undo_record[1],undo_record[2]
                elif undo_record[0] == "skip":
                    self.unsorted_movies.insert(0,movie)
                    movie = undo_record[1]
                    self.unsorted_movies.insert(0,movie)
                    self.unsorted_movies.pop()
                    with open("unsorted.txt", "w") as f:
                        for movie in self.unsorted_movies:
                            f.write(movie + "\n")
                    movie = self.unsorted_movies.pop(0)
                    upper,lower = len(self.sorted_movies),0
                elif undo_record[0] == "delete":
                    self.unsorted_movies.insert(0,movie)
                    movie = undo_record[1]
                    self.unsorted_movies.insert(0,movie)
                    with open("unsorted.txt", "w") as f:
                        for movie in self.unsorted_movies:
                            f.write(movie + "\n")
                    movie = self.unsorted_movies.pop(0)
                    upper,lower = len(self.sorted_movies),0
                    return movie, upper, lower #come back to this later
                elif undo_record[0] == "sort":
                    self.unsorted_movies.insert(0, movie)
                    movie = undo_record[1]
                    self.sorted_movies.remove(movie)
                    self.unsorted_movies.insert(0,movie)
                    with open(self.txt_file, "w") as f:
                        for movie in reversed(self.sorted_movies):
                            f.write(movie + "\n")
                    with open("unsorted.txt", "w") as f:
                        for movie in self.unsorted_movies:
                            f.write(movie + "\n")
                    movie = self.unsorted_movies.pop(0)
                    compare_undo_sort = self.undo_stack.pop()
                    upper,lower = compare_undo_sort[1], compare_undo_sort[2]

            elif self.is_skip_click(x,y):
                print("Skipped " + movie)
                self.unsorted_movies.append(movie)
                self.undo_stack.append(("skip", movie))
                with open("unsorted.txt", "w") as f:
                    for movie in self.unsorted_movies:
                        f.write(movie + "\n")
                movie = self.unsorted_movies.pop(0)
                upper,lower = len(self.sorted_movies),0
                return movie, upper, lower
            elif self.is_delete_click(x,y):
                print("Deleted " + movie)
                self.undo_stack.append(("delete", movie))
                with open("unsorted.txt", "w") as f:
                    for movie in self.unsorted_movies:
                        f.write(movie + "\n")
                movie = self.unsorted_movies.pop(0)
                upper,lower = len(self.sorted_movies),0
                return movie, upper, lower
            if lower >= upper:
                print("in sort if")
                self.sorted_movies.insert(lower, movie)
                print("Sorted " + movie)
                self.undo_stack.append(("sort", movie))
                with open(self.txt_file, "w") as f:
                    for movie in reversed(self.sorted_movies):
                        f.write(movie + "\n")
                with open("unsorted.txt", "w") as f:
                    for movie in self.unsorted_movies:
                        f.write(movie + "\n")
                if len(self.unsorted_movies) == 0:
                    self.running = False
                    print("All Done!")
                    return movie, upper, lower
                if (not self.need_user_input):
                    movie = self.unsorted_movies.pop(0)
                    upper,lower = len(self.sorted_movies),0
        return movie, upper, lower

def is_in_rect(rect, x, y):
    return x >= rect[0] and x <= (rect[0]+rect[2]) and y >= rect[1] and y <= (rect[1] + rect[3])
