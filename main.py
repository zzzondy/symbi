import os
import requests
import pygame



toponym_to_find = 'Конь-Колодезь'

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
delta = '18'


def change_scale(plus):  # второй этап
    global delta
    delta = float(delta)
    if plus:
        delta *= 1.5
    else:
        delta /= 1.5
    delta = str(delta)


def change_coords(coord):
    global toponym_longitude, toponym_lattitude
    toponym_longitude = float(toponym_longitude)
    toponym_lattitude = float(toponym_lattitude)
    if coord == 'up':
        toponym_lattitude += 6
    elif coord == 'down':
        toponym_lattitude -= 6
    elif coord == 'right':
        toponym_longitude += 4.5
    else:
        toponym_longitude -= 4.5
    toponym_longitude = str(toponym_longitude)
    toponym_lattitude = str(toponym_lattitude)


def change_map(param):
    global map_params, map_api_server, response, map_file
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": param
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta]),
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True
param = 'map'
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                change_scale(True)
                change_map(param)
                print(delta)
            if event.key == pygame.K_2:
                change_scale(False)
                change_map(param)
            if event.key == pygame.K_RIGHT:
                change_coords('right')
                change_map(param)
            if event.key == pygame.K_LEFT:
                change_coords('left')
                change_map(param)
            if event.key == pygame.K_DOWN:
                change_coords('down')
                change_map(param)
            if event.key == pygame.K_UP:
                change_coords('up')
                change_map(param)
            if event.key == pygame.K_m:
                param = 'map'
                change_map(param)
            if event.key == pygame.K_h:
                param = 'skl'
                change_map(param)
            if event.key == pygame.K_s:
                param = 'sat'
                change_map(param)


    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
