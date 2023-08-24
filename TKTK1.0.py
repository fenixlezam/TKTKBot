from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import random

from time import sleep
from selenium.webdriver.chrome.service import Service

# Leer el nombre de usuario desde el archivo "user.txt"
with open("user.txt", "r") as file:
    nombre_usuario = file.read().strip()

# Leer la contraseña desde el archivo "usuario.txt"
with open("pass.txt", "r") as file:
    pass_user = file.read().strip()

# Leer los nombres de usuario desde el archivo de texto
with open('usuarios.txt', 'r') as file:
    usuarios = file.read().splitlines()
    
# Leer los mensajes desde el archivo "mensajes.txt"
with open("mensajes.txt", "r") as message_file:
    mensajes = message_file.readlines()




options = Options()
options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
options.add_argument('--incognito')

#chrome_driver_path = ChromeDriverManager().install()
#driver = webdriver.Chrome(service=driver_service, options=options)
driver = webdriver.Chrome()

# Iniciar sesión en Instagram
driver.get("https://www.tiktok.com/login/phone-or-email/email")



username_field = driver.find_element(By.NAME, "username")
username_field.send_keys(nombre_usuario)
sleep(4)
password_field = driver.find_element(By.XPATH, "//input[@type='password']")
password_field.send_keys(pass_user)
sleep(3)
login_button = driver.find_element(By.XPATH, "//button[@data-e2e='login-button']")
login_button.click()
# Esperar a que la página cargue completamente
sleep(7)

# Iterar a través de los usuarios y realizar las interacciones en sus perfiles
for usuario in usuarios:
    usuario = usuario.strip()
    perfil_url = (f"https://www.tiktok.com/@"+usuario)
    driver.get(perfil_url)
    sleep(6)

    try:
        # Hacer clic en el botón de "Seguir"
        follow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Seguir')]"))
        )
        follow_button.click()
        sleep(5)

         # Esperar hasta que el botón "Enviar mensaje" esté presente y sea clickable
        message_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='button' and contains(text(), 'Enviar mensaje')]")
            )
        )

        # Hacer clic en el botón "Enviar mensaje"
        message_button.click()
        sleep(3)
         
        try:
             # Esperar hasta que el botón "Ahora no" esté presente y sea clickable dentro del modal
            ahora_no_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='_a9-z']//button[contains(., 'Ahora no')]")
                )
            )

            # Hacer clic en el botón "Ahora no"
            ahora_no_button.click()

        except TimeoutException:
            print("El botón 'Ahora no' no está presente en la pantalla.")

        chat_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@aria-label='Mensaje' and @contenteditable='true']")
                )
            )

# Quitar saltos de línea y espacios en blanco de los mensajes
        mensajes = [mensaje.strip() for mensaje in mensajes]

# Seleccionar un mensaje al azar de la lista
        mensaje_aleatorio = random.choice(mensajes)

# Escribir el mensaje aleatorio en el cuadro de chat
        chat_box.send_keys(mensaje_aleatorio)


            # Esperar hasta que el botón "Enviar" esté presente y sea clickable
        send_div = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(text(), 'Enviar')]")
                )
            )

            # Hacer clic en el div "Enviar"
        send_div.click()

            # Esperar un momento para que el mensaje se envíe
        sleep(6)

    except TimeoutException:
        print(f"No se pudo encontrar el botón de 'Seguir' para {usuario}. Pasando al siguiente usuario.")

            # Agregar el usuario a la lista "seguidos.txt"
        with open("seguidos.txt", "a") as seguidos_file:
            seguidos_file.write(usuario + "\n")

            # Eliminar el usuario de la lista "usuarios.txt"
        with open("usuarios.txt", "r") as usuarios_file:
            usuarios = usuarios_file.read().splitlines()
    
        with open("usuarios.txt", "w") as usuarios_file:
            usuarios_file.write("\n".join([u for u in usuarios if u.strip() != usuario]))
    
        continue  # Repite el ciclo con el siguiente usuario
    
input("Presiona Enter para cerrar el navegador...")
driver.quit()




