import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Combat with Levels")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)

# Player settings
player_size = (50, 50)
player_img = pygame.Surface(player_size)
player_img.fill(GREEN)
player_speed = 5

# Bullet settings
bullet_size = (5, 15)
bullet_img = pygame.Surface(bullet_size)
bullet_img.fill(WHITE)
bullet_speed = -7
bullet_cooldown = 300  # in milliseconds
last_bullet_time = pygame.time.get_ticks()

# Enemy settings
enemy_types = {
    'basic': {'size': (50, 50), 'color': RED, 'speed': 3, 'health': 20},
    'fast': {'size': (50, 50), 'color': CYAN, 'speed': 5, 'health': 10},
    'tank': {'size': (70, 70), 'color': PURPLE, 'speed': 2, 'health': 40}
}

# Power-up settings
power_up_size = (30, 30)
health_powerup_img = pygame.Surface(power_up_size)
health_powerup_img.fill(GREEN)
shield_powerup_img = pygame.Surface(power_up_size)
shield_powerup_img.fill(BLUE)
shooting_speed_powerup_img = pygame.Surface(power_up_size)
shooting_speed_powerup_img.fill(YELLOW)

# Player attributes
player_pos = [WIDTH // 2, HEIGHT - 60]
player_health = 100
player_has_shield = False
shield_duration = 5000  # 5 seconds
shield_end_time = 0
score = 0
level = 1

# Difficulty progression
score_threshold = 100  # Score needed to level up
enemy_spawn_rate = 0.02  # Base enemy spawn rate

# Bullet, enemy, and power-up lists
bullets = []
enemies = []
power_ups = []

# Font settings
font = pygame.font.SysFont("Arial", 24)

# Health bar function for enemies
def draw_health_bar(x, y, health, max_health, width=40, height=5):
    ratio = health / max_health
    pygame.draw.rect(screen, RED, (x, y, width, height))
    pygame.draw.rect(screen, GREEN, (x, y, width * ratio, height))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot bullets on spacebar press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_time = pygame.time.get_ticks()
                if current_time - last_bullet_time >= bullet_cooldown:
                    bullets.append(pygame.Rect(player_pos[0] + player_size[0] // 2 - bullet_size[0] // 2, player_pos[1], *bullet_size))
                    last_bullet_time = current_time

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size[0]:
        player_pos[0] += player_speed

    # Level up and increase difficulty
    if score >= level * score_threshold:
        level += 1
        enemy_spawn_rate += 0.01  # Increase spawn rate slightly
        for enemy_type in enemy_types.values():
            enemy_type['speed'] += 0.5  # Increase speed of each enemy type slightly

    # Enemy spawning
    if random.random() < enemy_spawn_rate:
        enemy_type = random.choice(list(enemy_types.keys()))
        enemy_x = random.randint(0, WIDTH - enemy_types[enemy_type]['size'][0])
        enemy = {
            'rect': pygame.Rect(enemy_x, 0, *enemy_types[enemy_type]['size']),
            'type': enemy_type,
            'health': enemy_types[enemy_type]['health'],
            'max_health': enemy_types[enemy_type]['health'],
            'speed': enemy_types[enemy_type]['speed'],
            'color': enemy_types[enemy_type]['color']
        }
        enemies.append(enemy)

    # Power-up spawning
    if random.random() < 0.005:
        power_up_type = random.choice(['health', 'shield', 'shooting_speed'])
        power_up_x = random.randint(0, WIDTH - power_up_size[0])
        power_ups.append({'rect': pygame.Rect(power_up_x, 0, *power_up_size), 'type': power_up_type})

    # Move bullets
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies[:]:
        enemy['rect'].y += enemy['speed']
        if enemy['rect'].y > HEIGHT:
            enemies.remove(enemy)
            if not player_has_shield:
                player_health -= 10  # Lose health if enemy reaches the bottom

    # Move power-ups
    for power_up in power_ups[:]:
        power_up['rect'].y += 3
        if power_up['rect'].y > HEIGHT:
            power_ups.remove(power_up)

    # Collision detection
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if enemy['rect'].colliderect(bullet):
                bullets.remove(bullet)
                enemy['health'] -= 10
                if enemy['health'] <= 0:
                    enemies.remove(enemy)
                    score += 10
                break

    # Check for collisions between player and power-ups
    for power_up in power_ups[:]:
        if pygame.Rect(player_pos, player_size).colliderect(power_up['rect']):
            if power_up['type'] == 'health':
                player_health = min(player_health + 20, 100)
            elif power_up['type'] == 'shield':
                player_has_shield = True
                shield_end_time = pygame.time.get_ticks() + shield_duration
            elif power_up['type'] == 'shooting_speed':
                bullet_cooldown = 150
                pygame.time.set_timer(pygame.USEREVENT, 5000)
            power_ups.remove(power_up)

    # Check if shield is active and expire it if time is up
    if player_has_shield and pygame.time.get_ticks() > shield_end_time:
        player_has_shield = False

    # Event to reset shooting speed after power-up duration
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            bullet_cooldown = 300
            pygame.time.set_timer(pygame.USEREVENT, 0)

    # Draw player, bullets, enemies, and power-ups
    screen.blit(player_img, player_pos)
    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x, bullet.y))
    for enemy in enemies:
        pygame.draw.rect(screen, enemy['color'], enemy['rect'])
        draw_health_bar(enemy['rect'].x, enemy['rect'].y - 10, enemy['health'], enemy['max_health'])
    for power_up in power_ups:
        if power_up['type'] == 'health':
            screen.blit(health_powerup_img, (power_up['rect'].x, power_up['rect'].y))
        elif power_up['type'] == 'shield':
            screen.blit(shield_powerup_img, (power_up['rect'].x, power_up['rect'].y))
        elif power_up['type'] == 'shooting_speed':
            screen.blit(shooting_speed_powerup_img, (power_up['rect'].x, power_up['rect'].y))

    # Draw health bar, shield status, score, and level
    draw_health_bar(10, 10, player_health, 100, width=100, height=10)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 40))

    # Display shield status
    if player_has_shield:
        shield_text = font.render("SHIELD ACTIVE", True, BLUE)
        screen.blit(shield_text, (10, 30))

    # End game if player health is depleted
    if player_health <= 0:
        running = False

    pygame.display.flip()
    clock.tick(60)  # Maintain 60 FPS

# Quit Pygame
pygame.quit()
