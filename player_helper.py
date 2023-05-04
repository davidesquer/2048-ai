# %%
import logic

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import random
import numpy as np

import os
import time

# %%
def juego(depth): #funcion que juega 2048
    current_username = os.getlogin() #obtiene el nombre de usuario de la computadora

    driver_path_mac = "Users/davidesquer/Documents/chromedriverfolder/chromedrive"  #direccion del driver de chrome
    driver_path_windows = "C:/Users/David/Downloads/chromedriver_win32/chromedriver.exe" #direccion del driver de chrome

    if current_username == "David": #checa si el nombre de usuario es David
        driver_path = driver_path_windows #si es David, usa la direccion del driver de chrome para windows
    else:
        driver_path = driver_path_mac #si no es David, usa la direccion del driver de chrome para mac

    driver = webdriver.Chrome(executable_path=driver_path) #abre el navegador
    driver.get("https://2048.io") #abre el juego

    moves = {"up": Keys.UP, "right": Keys.RIGHT, "down": Keys.DOWN, "left": Keys.LEFT} #diccionario de movimientos posibles

    while True: #loop infinito, hasta que el juego termine
        l1 = []
        js_code = """
        var elements = document.querySelectorAll(".tile");
        var classNames = [];
        for (var i = 0; i < elements.length; i++) {
            classNames.push(elements[i].className);
        }
        return classNames;
        """
        class_names = driver.execute_script(js_code)
        for i in class_names:
            l1.append(i.split(" "))
            
        board = np.array([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]) #matriz que contiene el estado del juego actual en ceros
        for i in range(len(l1)): #loop sobre el estado del juego actual
            value = int(l1[i][1].split("-")[1]) #valor de la casilla

            col = int(l1[i][2].split("-")[2])-1 #columna de la casilla
            row = int(l1[i][2].split("-")[3])-1 #fila de la casilla

            if board[row][col] < value: #si el valor de la casilla es mayor al valor de la casilla en la matriz, se actualiza el valor de la casilla en la matriz
                board[row][col] = value #actualiza el valor de la casilla en la matriz
        
        elements = driver.find_elements(By.CSS_SELECTOR, ".game-message") #elemento de mensaje de juego

        if elements[0].text == "Game over!\nTry again": #si el juego termina, se rompe el loop
            break
        else:
            move = logic.best_move(board, depth) #mejor movimiento que se puede realizar
            game_element = driver.find_element(By.TAG_NAME, "body") #elemento para mandar los movimientos
            game_element.send_keys(moves[move]) #ejecuta el movimiento elegido
        
    driver.close() #cierra el navegador

# %%
juego(7)


