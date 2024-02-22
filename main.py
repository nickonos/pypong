# Example file showing a circle moving on screen
import numpy
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
line_height = 100
line_width = 10
font = pygame.font.SysFont("Arial", 24 )

# Ball variables
max_velocity = 15
min_velocity = 5
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_direction = pygame.Vector2(min_velocity, numpy.random.randint(-min_velocity, min_velocity + 1))

# Player variables
player_1_pos = pygame.Vector2(10, screen.get_height() / 2 - (line_height / 2) )
player_2_pos = pygame.Vector2(screen.get_width() - 10, screen.get_height() / 2 - (line_height / 2) )
score = (0,0)

paused = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw
    screen.fill("black")
    pygame.draw.circle(screen, "white", ball_pos, 10)
    pygame.draw.line(screen, "blue", pygame.Vector2(player_1_pos.x, player_1_pos.y), pygame.Vector2(player_1_pos.x, player_1_pos.y + line_height), line_width)
    pygame.draw.line(screen, "red", pygame.Vector2(player_2_pos.x, player_2_pos.y), pygame.Vector2(player_2_pos.x, player_2_pos.y + line_height), line_width)

    score_text = font.render('Score', True, "white")
    screen.blit(score_text, (screen.get_width()/2 - 50, 0))
    score_display = font.render(f'{score[0]} - {score[1]}', True, "white")
    screen.blit(score_display, (screen.get_width()/2 - 45, 30))

    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_1_pos.y = numpy.clip(0, player_1_pos.y - (300 * dt), screen.get_height())
    if keys[pygame.K_s]:
        player_1_pos.y = numpy.clip(0, player_1_pos.y + (300 * dt), screen.get_height() - line_height)
    if keys[pygame.K_i]:
        player_2_pos.y = numpy.clip(0, player_2_pos.y - (300 * dt), screen.get_height())
    if keys[pygame.K_k]:
        player_2_pos.y = numpy.clip(0, player_2_pos.y + (300 * dt), screen.get_height() - line_height)
    if keys[pygame.K_SPACE] and paused:
        paused = False

    if not paused:
        # Move ball
        ball_pos = pygame.Vector2(ball_pos.x + ball_direction.x, ball_pos.y + ball_direction.y)

        # Player collision detection
        if ball_pos.x > player_1_pos.x and ball_pos.x < player_1_pos.x + line_width + line_width and ball_pos.y > player_1_pos.y and ball_pos.y < player_1_pos.y + line_height:
            ball_direction = pygame.Vector2(numpy.clip(-max_velocity, -ball_direction.x * 1.1, max_velocity), numpy.clip(-max_velocity, ball_direction.y * 1.1, max_velocity))
        if ball_pos.x < player_2_pos.x and ball_pos.x > player_2_pos.x - line_width - line_width and ball_pos.y > player_2_pos.y and ball_pos.y < player_2_pos.y + line_height:
             ball_direction = pygame.Vector2(numpy.clip(-max_velocity, -ball_direction.x * 1.1, max_velocity), numpy.clip(-max_velocity, ball_direction.y * 1.1, max_velocity))

        # Map collision detection
        if ball_pos.y <= 0:
            ball_direction = pygame.Vector2(ball_direction.x, -ball_direction.y)
        if ball_pos.y >= screen.get_height():
            ball_direction = pygame.Vector2(ball_direction.x, -ball_direction.y)

        # Goal collision detection
        if ball_pos.x <= 0:
            score = (score[0], score[1] + 1)
            ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            ball_direction = pygame.Vector2(min_velocity, numpy.random.randint(-min_velocity, min_velocity + 1))
            paused = True
        if ball_pos.x >= screen.get_width():
            score = (score[0] + 1, score[1])
            ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            ball_direction = pygame.Vector2(-min_velocity, numpy.random.randint(-min_velocity, min_velocity + 1))
            paused = True

    # Render
    pygame.display.flip()

    # Time
    dt = clock.tick(60) / 1000

pygame.quit()