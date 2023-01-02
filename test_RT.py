from time import sleep
from base_data import *
from settings import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 1. Тест RT-1. Визуальная проверка соответствия технической документации. Общий вид (скриншот).
def test_001(selenium):
    form = AuthForm(selenium)
    form.driver.save_screenshot('screen_test_RT2.jpg')


# 2. Тест RT-2. Проверка на соответствие наименования вида аутентификации - Телефон.
def test_002(selenium):
    form = AuthForm(selenium)

    assert form.phone_tab.get_text() == "Телефон"


# 3. Тест RT-3. Проверка на соответствие наименования вида аутентификации - Почта.
def test_003(selenium):
    form = AuthForm(selenium)

    assert form.mail_tab.get_text() == "Почта"


# 4. Тест RT-4. Проверка на соответствие наименования вида аутентификации - Логин.
def test_004(selenium):
    form = AuthForm(selenium)

    assert form.login_tab.get_text() == "Логин"


# 5. Тест RT-5. Проверка на соответствие наименования вида аутентификации - Лицевой счёт.
def test_005(selenium):
    form = AuthForm(selenium)

    assert form.ls_tab.get_text() == "Лицевой счёт"


# 6. Тест RT-6. Проверка авторизации. Аутентификация по телефону и паролю по умолчанию.
def test_006(selenium):
    form = AuthForm(selenium)

    assert form.placeholder.text == 'Мобильный телефон'


# 7. Тест RT-7. Позитивное тестирование авторизации пользователя по почте.
def test_007(selenium):
    form = AuthForm(selenium)

    # вводим корректный email и пароль
    form.username.send_keys(valid_email)
    form.password.send_keys(valid_pass)
    sleep(10)
    form.btn_click()

    assert form.get_current_url() != '/account_b2c/page'


# 8. Тест RT-8. Негативное тестирование авторизации пользователя по почте.
def test_008(selenium):
    form = AuthForm(selenium)

    # вводим некорректный email и пароль
    form.username.send_keys('111@mail.ru')
    form.password.send_keys('password')
    sleep(10)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# 9. Тест RT-9. Автоматическое изменение меню выбора типа аутентификации
def test_009(selenium):
    form = AuthForm(selenium)

    # ввод произвольного мобильного телефона
    form.username.send_keys('+77771117711')
    form.password.send_keys('_')
    sleep(10)

    assert form.placeholder.text == 'Мобильный телефон'

    # очистка поля ввода
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # ввод произвольной почты
    form.username.send_keys('111@mail.ru')
    form.password.send_keys('_')
    sleep(10)

    assert form.placeholder.text == 'Электронная почта'

    # очистка поля ввода
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # ввод произвольного логина
    form.username.send_keys('Login')
    form.password.send_keys('_')
    sleep(10)

    assert form.placeholder.text == 'Логин'


# 10. Тест RT-10. Переход в форму восстановления пароля
def test_010(selenium):
    form = AuthForm(selenium)

    form.forgot.click()
    sleep(10)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Восстановление пароля'


# 11. Тест RT-11. Переход в форму регистрации
def test_011(selenium):
    form = AuthForm(selenium)

    form.register.click()
    sleep(10)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Регистрация'


# 12. Тест RT-12. Переход на страницу пользовательского соглашения/политики конфиденциальности
def test_012(selenium):
    form = AuthForm(selenium)

    original_window = form.driver.current_window_handle
    form.agree.click()
    sleep(5)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    win_title = form.driver.execute_script("return window.document.title")

    assert win_title == 'User agreement'


# 13. Тест RT-13. Авторизация через Вконтакте
def test_013(selenium):
    form = AuthForm(selenium)
    form.vk_btn.click()
    sleep(5)

    assert form.get_base_url() == 'oauth.vk.com'


# 14. Тест RT-14. Авторизация через Одноклассники
def test_014(selenium):
    form = AuthForm(selenium)
    form.ok_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.ok.ru'


# 15. Тест RT-15. Авторизация через Мой мир
def test_015(selenium):
    form = AuthForm(selenium)
    form.mailru_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.mail.ru'


# 16. Тест RT-16. Авторизация через Google
def test_016(selenium):
    form = AuthForm(selenium)
    form.google_btn.click()
    sleep(5)

    assert form.get_base_url() == 'accounts.google.com'


# 17. Тест RT-17. Авторизация через Яндекс
def test_017(selenium):
    form = AuthForm(selenium)
    form.ya_btn.click()
    sleep(5)

    assert form.get_base_url() == 'passport.yandex.ru'
