import pygame
import pygame.locals as pl
import sys
import GameScreen
import Scores
pygame.init()


def load_wordbank(path):
    """One word per line; blank lines (e.g. a trailing newline) are dropped."""
    with open(path, 'r', encoding='utf-8') as f:
        return [w.strip() for w in f.read().splitlines() if w.strip()]

class Wordbanks:
    words_english = load_wordbank('Media/words.txt')
    words_french = load_wordbank('Media/mots.txt')
    words_german = load_wordbank('Media/Wörtern.txt')


#####################
#   Game Specifics  #
#####################
def save_current_score(game):
    Scores.save_score(GameScreen.get_words_per_min(game), game.seconds)

def quit_game(game):
    save_current_score(game)
    pygame.quit()
    sys.exit(0)

def play_music(game, music):
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    game.music_playing = True
    return

def update_seconds(game, delay):
    game.frame_tracker += 1
    if (game.frame_tracker == (game.max_FPS * delay)):
        game.frame_tracker = 0
        game.seconds += 1
        return True
    return False

def blink_text(game, screen, text, start_screen):
    if (game.update_seconds(game.text_blink_delay)):
        game.blinking = not game.blinking
    if (game.blinking):
        game.draw_blink_text(screen, text, start_screen)
    return

def update_player_input(game, events):
    if (game.words_moving):
        if (game.player_input_obj.update(events, game)):
            game.player_input = game.player_input_obj.get_text()
            game.player_input_obj.reset_input_text()
    return


#####################
#       Frames      #
#####################
def check_frame_count(game):
    if (game.frame_count >= game.max_FPS):
        game.frame_count = 0
        game.seconds += 1
        game.add_word_seconds += 1
    return

def check_quick_frame_count(game):
    max_FPS_fraction = game.max_FPS * game.add_word_delay
    if (game.quick_frame_count == max_FPS_fraction):
        game.quick_frame_count = 0
        return True
    game.quick_frame_count += 1
    return False


#####################
#    Title Events   #
#####################
def check_title_events(game):
    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
            quit_game(game)
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                return True
    return False


#####################
#    Menu Events    #
#####################
def get_avg_word_length(wordbank):
    # Standard typing-test convention (the old code computed the real average
    # and then ignored it).
    return 4.5

def check_menu_mouse_position(game, mouse_position, button):
    if (button.is_over(mouse_position)):
        button.color = game.button_hover_color
        button.textColor = game.button_text_color
        button.hovering = True
        if (button.play_sound):
            if game.music_playing is True:
                game.button_hover_sound.play()
                button.play_sound = False
    else:
        button.color = game.button_color
        button.textColor = game.button_text_color
        button.hovering = False
        button.play_sound = True
    return

def check_button(game, button):
    if (button.text == "1st"):
        game.wordbank = Wordbanks.words_english
    elif (button.text == "2nd"):
        game.wordbank = Wordbanks.words_french
    elif (button.text == "3rd"):
        game.wordbank = Wordbanks.words_german
    elif (button.text == 'information'):
        return False
    elif (button.text == 'mute'):
        if game.music_playing is False:
            pygame.mixer.music.unpause()
            game.music_playing = True
        else:
            pygame.mixer.music.pause()
            game.music_playing = False
        return False
    game.avg_word_length = get_avg_word_length(game.wordbank)
    return True

def check_menu_events(game, buttons):
    mouse_position = pygame.mouse.get_pos()
    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
            quit_game(game)
        elif (event.type == pygame.MOUSEMOTION):
            for button in buttons:
                check_menu_mouse_position(game, mouse_position, button)
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            for button in buttons:
                if (button.is_over(mouse_position)):
                    if (check_button(game, button)):
                        return True
    return False

def click_button(mouse_position, buttons, game):
    for button in buttons:
        if (button.is_over(mouse_position)):
            if (button.text == "Start"):
                game.words_moving = True
                button.visible = True
            elif (button.text == "Pause"):
                game.words_moving = not game.words_moving
            elif (button.text == "Mute"):
                if (game.music_playing):
                    pygame.mixer.music.pause()
                    game.music_playing = False
                else:
                    pygame.mixer.music.unpause()
                    game.music_playing = True
    return

def check_game_events(game, buttons):
    events = pygame.event.get()
    for event in events:
        if (event.type == pygame.QUIT):
            quit_game(game)
        elif (event.type == pygame.KEYDOWN):
            if event.key == pl.K_ESCAPE:
                if (game.words_moving):
                    game.words_moving = False
                    game.is_paused = True
                    game.pause_high_score = Scores.get_high_score()
                else:
                    game.words_moving = True
                    game.is_paused = False
            if game.is_paused:
                if event.key == pygame.K_r:
                    game.restart_variable = True
                    save_current_score(game)

    update_player_input(game, events)
    return True
