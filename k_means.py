import pygame
import math
from random import randint
from sklearn.cluster import KMeans

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("kmeans visualization")

running = True

clock = pygame.time.Clock()

BACKGROUND = (214,214,214)
BLACK = (0,0,0)
CREAM = (255,253,208)
WHITE = (255,255,255)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

COLORS = [RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]

k_value = 0
points = []
clusters = []
labels = []

font_sign = pygame.font.SysFont('Sans', 70, bold=pygame.font.Font.bold)
font_letter = pygame.font.SysFont('Sans', 25)
font_xy = pygame.font.SysFont('Sans', 10)

def create_text_sign(string):
	return font_sign.render(string, True, WHITE)

def create_text_letter(string):
	return font_letter.render(string, True, WHITE)

def create_text_letter2(string):
	return font_letter.render(string, True, BLACK)

def distance(point1, point2):
	return math.sqrt((point1[0]-point2[0])*(point1[0]-point2[0]) + (point1[1]-point2[1])*(point1[1]-point2[1]))

sign_1 = create_text_sign("+")
sign_2 = create_text_sign("-")
run_letter = create_text_letter("RUN")
random_letter = create_text_letter("RANDOM")
algorithm_letter = create_text_letter("ALGORITHM")
reset_letter = create_text_letter("RESET")
k_letter = create_text_letter2("K = ")
error_letter = create_text_letter2("ERROR = ")

while running:
	clock.tick(60)
	screen.fill(BACKGROUND)
	mouse_x, mouse_y = pygame.mouse.get_pos()
	mousex = mouse_x - 55
	mousey = mouse_y - 75

	# Draw interface

	# Draw work screen
	pygame.draw.rect(screen, BLACK, pygame.Rect(50, 70, 700, 500))
	pygame.draw.rect(screen, CREAM, pygame.Rect(55, 75, 690, 490))

	# Draw K button
	pygame.draw.rect(screen, BLACK, pygame.Rect(850, 70, 50, 50))
	pygame.draw.rect(screen, BLACK, pygame.Rect(950, 70, 50, 50))

	screen.blit(sign_1, (855, 50))
	screen.blit(sign_2, (962, 50))

	# K value
	if k_value > 9:
		k_value = 9
	if k_value < 0:
		k_value = 0
	k_value_letter = font_letter.render(str(k_value), True, BLACK)
	screen.blit(k_letter, (1065, 80))
	screen.blit(k_value_letter, (1105, 80))

	# Draw RUN button
	pygame.draw.rect(screen, BLACK, pygame.Rect(850, 170, 150, 50))
	screen.blit(run_letter, (900, 180))

	# Draw RAMDOM button
	pygame.draw.rect(screen, BLACK, pygame.Rect(850, 270, 150, 50))
	screen.blit(random_letter, (880, 280))


	# Draw ALGORITHM button
	pygame.draw.rect(screen, BLACK, pygame.Rect(850, 470, 150, 50))
	screen.blit(algorithm_letter, (865, 480))

	# Draw RESET button
	pygame.draw.rect(screen, BLACK, pygame.Rect(850, 570, 150, 50))
	screen.blit(reset_letter, (890, 580))

	# Draw mouse position when mouse is in panel
	if 55<mouse_x<745 and 75<mouse_y<565:
		text_mouse = font_xy.render("(" + str(mousex) + "," + str(mousey) + ")", True, BLACK)
		screen.blit(text_mouse, (mouse_x + 10, mouse_y + 15))

	# Draw point
	for i in range(len(points)):
		pygame.draw.circle(screen, BLACK, (points[i][0] ,points[i][1]), 6)
		if labels == []:
			pygame.draw.circle(screen, CREAM, (points[i][0] ,points[i][1]), 4)
		else:
			pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] ,points[i][1]), 4)

	# Draw clusters
	for i in range(len(clusters)):
		pygame.draw.circle(screen, BLACK, (clusters[i][0] ,clusters[i][1]), 10)
		pygame.draw.circle(screen, COLORS[i], (clusters[i][0] ,clusters[i][1]), 8)

	# Draw ERROR
		error_value = 0
		if clusters != [] and labels != []:
			for i in range(len(points)):
				error_value += distance(points[i], clusters[labels[i]])
		error_value_letter = font_letter.render(str(int(error_value)), True, BLACK)
		screen.blit(error_value_letter, (980, 380))
		screen.blit(error_letter, (880, 380))

	# End draw interface

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Change K button +
			if 850<mouse_x<900 and 70<mouse_y<120:
				k_value += 1
			# Change K button -
			if 950<mouse_x<1000 and 70<mouse_y<120:
				k_value -= 1
			# RUN button
			if 850<mouse_x<1000 and 170<mouse_y<220:
				if clusters != []:
					labels = []
					# Assign points to closest clusters
					for p in points:
						distances_to_clusters = []
						for c in clusters:
							dis = distance(p,c)
							distances_to_clusters.append(dis)
						min_dis = min(distances_to_clusters)
						label = distances_to_clusters.index(min_dis)
						labels.append(label)
					#Update clusters
					for i in range(k_value):
						point_x = 0
						point_y = 0
						count = 0
						for j in range(len(points)):
							if labels[j] == i:
								point_x += points[j][0]
								point_y += points[j][1]
								count += 1
						if count != 0:
							new_x_cluter = point_x/count
							new_y_cluter = point_y/count
							clusters[i]=[new_x_cluter, new_y_cluter]
			# RANDOM button
			if 850<mouse_x<1000 and 270<mouse_y<320:
				labels = []
				clusters = []
				for i in range(k_value):
					random_point = [randint(60,685),randint(80,485)]
					clusters.append(random_point)
			# ALGORITHM button
			if 850<mouse_x<1000 and 470<mouse_y<520:
				if points == [] and k_value == 0:
					continue
				else:
					kmeans = KMeans(n_clusters=k_value).fit(points)
					labels = kmeans.predict(points)
					clusters = kmeans.cluster_centers_
			# RESET button
			if 850<mouse_x<1000 and 570<mouse_y<620:
				k_value = 0
				points = []
				clusters = []
				labels = []
			# Create point on panel
			if 55<mouse_x<745 and 75<mouse_y<565:
				labels = []
				point = [mouse_x,mouse_y]
				points.append(point)

	pygame.display.flip()

pygame.quit()