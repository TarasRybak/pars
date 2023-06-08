import os
import pickle

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth
import time

# options

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_argument('--start-maximized')

service = Service(executable_path="./chromedriver")

driver = webdriver.Chrome(service=service, options=options)

# options = webdriver.ChromeOptions()
#
#
# # user-agent
# options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
# driver = webdriver.Chrome(options=options)


def save_cookies():
    # створення файлу кукіс, треба виконати через дебагер і тільки першого разу
    url = f'https://www.bing.com/images/create/'
    driver.get(url)
    cookies = {'name': 'cookie_name', 'value': 'cookie_value'}
    driver.add_cookie(cookies)
    time.sleep(180)
    driver.refresh()
    pickle.dump(driver.get_cookies(), open("bing_com.pkl", "wb"))

def cheack_token_bal() -> int:
    # Очікуємо, поки елемент з'явиться на сторінці
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "token_bal")))

    # Отримуємо значення елемента
    element_value = element.text
    try:
        element_value = int(element_value)
    except:
        element_value = 0
    # Виводимо значення елемента
    print(element_value)
    return element_value


def edge_gpt_img_save(text: str, language_code: str):
    # загрузка кукіс з файла в селеніум
    url = f'https://www.bing.com/images/create/'
    driver.get(url)
    print(r'load(open("bing_com.pkl", "rb"))')
    cookies = pickle.load(open("bing_com.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(5)
    # Перезавантаження сторінки, щоб застосувати кукі
    driver.refresh()

    search_arg = f"{text} in {language_code}, postcard"
    print(search_arg)
    # Очікуємо, поки поле вводу з'явиться на сторінці
    input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sb_form_q")))

    # Вводимо значення у поле вводу
    input_element.clear()  # Очищаємо поле вводу перед введенням нового значення
    input_element.send_keys(search_arg)

    # Очікуємо, поки кнопка з'явиться на сторінці
    button_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "create_btn_c")))
    # Натискаємо кнопку
    button_element.click()
    print("click")

    time.sleep(30) if cheack_token_bal() else time.sleep(360)  # якщо бонуси закінчаться(=0), то довше треба чекати

    # Очікуємо, поки елементи зображень з'являться на сторінці
    image_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.img_cont.hoff img.mimg")))
    print(len(image_elements))
    # Зберігаємо значення атрибуту src у списку
    image_src_list = []
    for image_element in image_elements:
        image_src = image_element.get_attribute("src")
        image_src_list.append(image_src)

    # Виводимо список src
    print(image_src_list)

    # Створення директорії для збереження зображень (якщо вона ще не існує)
    filename = text
    image_directory = f"./bingIMG/{language_code}"
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    image_directory += f"/{text}"
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    else:
        filename += f"_{int(time.time())}"  # якщо папка вже існує, то напевне там є малюнки

    # Збереження зображень
    for i, image_src in enumerate(image_src_list):
        # Завантажуємо зображення з URL
        response = requests.get(image_src)
        # Генеруємо ім'я файлу для зображення та текстового документа
        image_filename = f"{filename}_{i + 1}.jpg"
        text_filename = f"{filename}_links.txt"
        # Шлях до зображення та текстового документа
        image_path = os.path.join(image_directory, image_filename)
        text_path = os.path.join(image_directory, text_filename)
        # Зберігаємо зображення
        with open(image_path, "wb") as image_file:
            image_file.write(response.content)
        # Зберігаємо ссилку в текстовий документ
        with open(text_path, "a") as text_file:
            text_file.write(image_src + "\n")
        print(f"Зображення {i} збережено: {image_path}")


def main_func_edge_gpt_img_save(text: str, language_code: str = "ua", save_cook: bool = False):
    try:
        print("start")
        stealth(driver,
                languages=["uk-UK", "uk"],
                vendor="Google Inc.",
                platform="Win64",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True, )

        if save_cook:
            print("cookies")
            save_cookies()
            return ["Куки збережені у файлі bing_com.pkl"]
        edge_gpt_img_save(text, language_code)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        # driver.quit()


if __name__ == '__main__':
    main_func_edge_gpt_img_save("чай", "pl")
    # input()

# <input name="q" class="b_searchbox gi_sb" id="sb_form_q" title="" type="search" value="tree in Canada, bright, picturesque,  postcard" aria-label="Хочете дізнатися, як працює Творець зображень? Виберіть &quot;Здивуй мене&quot;, а потім – &quot;Створити&quot;" placeholder="Хочете дізнатися, як працює Творець зображень? Виберіть &quot;Здивуй мене&quot;, а потім – &quot;Створити&quot;" autocapitalize="off" autocorrect="true" autocomplete="off" spellcheck="true" aria-live="polite" maxlength="480" data-maxlength="480">
# <a role="button" id="create_btn_c" class="gi_btn_p" aria-label="Створити" aria-live="polite" name="Create" href="javascript:void(0)" h="ID=images,5121.1"><div id="create_btn_e" class=""></div><img id="create_btn_i" aria-label="Створити" width="20" height="20" role="img" class="rms_img" src="data:image/svg+xml,%3Csvg%20viewport%3D%220%200%2020%2020%22%20fill%3D%22none%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%0D%0A%20%20%20%20%3Cpath%20d%3D%22M11.499%203.25a1.25%201.25%200%201%201%200%202.5%201.25%201.25%200%200%201%200-2.5zM11.706%2014.53a.999.999%200%200%201%200-1.414l4.907-4.907a1.71%201.71%200%200%201%202.417%202.417l-4.907%204.907a.999.999%200%200%201-1.414%200l-1.003-1.003z%22%20fill%3D%22%23fff%22%2F%3E%0D%0A%20%20%20%20%3Cpath%20d%3D%22M4.499%2014H8.55c.256-.394.675-.762%201.088-1h-5.14a1.51%201.51%200%200%201-1.483-1.336l4.53-3.731a1.503%201.503%200%200%201%201.907%200l3.302%202.72.711-.711-3.377-2.781a2.501%202.501%200%200%200-3.18%200L3%2010.382V3.5c0-.827.673-1.5%201.5-1.5h8c.827%200%201.5.673%201.5%201.5v5.908l1-1V3.5c0-1.379-1.122-2.5-2.5-2.5h-8a2.503%202.503%200%200%200-2.5%202.5v7.764c-.111%201.457%201.025%202.744%202.5%202.736z%22%20fill%3D%22%23fff%22%2F%3E%0D%0A%20%20%20%20%3Cpath%20d%3D%22M19.03%208.208a1.71%201.71%200%200%200-2.417%200l-4.719%204.719a.979.979%200%200%200-.27.593c-1.172-.212-2.813%201.026-2.488%202.184.095.394-.117%201.084-.444%201.304-.467.008-1.175.492-1.142%200%20.202-.502.261-1.545-.455-1.914-1.317-.679-3.045.78-4.287%201.213-.435.123-.955-.095-1.369-.359-.239-.153-.542.117-.405.411.613%201.539%202.564%201.44%203.717.597.451-.255.907-.515%201.464-.615.096-.018.164.131.125.245-.57%201.881%201.218%202.57%203.16%201.855.984.204%202.301-.139%203.244-1.085a2.498%202.498%200%200%200%20.74-1.744c.295.036.6-.043.827-.27l4.72-4.719a1.71%201.71%200%200%200%200-2.417v.002zm-6.993%208.442c-.863.862-1.959.907-2.423.812.368-.302.65-1.449.517-1.859-.03-.303-.04-.394.212-.646%201.304-1.291%202.984.389%201.694%201.693z%22%20fill%3D%22%23fff%22%2F%3E%0D%0A%3C%2Fsvg%3E"><span id="create_btn" data-sm="ЗДИВУЙТЕ МЕНЕ" data-ct="Створити" data-enabled="Створити" data-disabled="Триває створення">Створити</span></a>
# <div class="img_cont hoff"><img class="mimg" style="" height="270" width="270" src="https://th.bing.com/th/id/OIG.a9YInmuR2ZW.vgbWLpl0?w=270&amp;h=270&amp;c=6&amp;r=0&amp;o=5&amp;dpr=2&amp;pid=ImgGn" alt="tree, ua, logo"></div>
