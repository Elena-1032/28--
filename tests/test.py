import pytest
from pages.auth_page import AuthPage
from pages.registr_page import RegistrPage
from pages.locators import AuthLocators
from settings import *

#1 Открытие формы "Регистрация"______________________________________________
def test_registration_link(selenium):
    page = AuthPage(selenium)
    page.register_link.click()
    assert page.find_other_element(*AuthLocators.registration).text == 'Регистрация'


# Форма "Регистрация" наличие основных активных элементов _______________________________
def test_elements_registration(selenium):
    try:
        page_reg = RegistrPage(selenium)
        card_of_reg = [page_reg.first_name, page_reg.last_name, page_reg.address_registration,
                       page_reg.email_registration, page_reg.password_registration,
                       page_reg.password_registration_confirm, page_reg.registration_btn]
        for i in range(len(card_of_reg)):
            assert page_reg.first_name in card_of_reg
            assert page_reg.last_name in card_of_reg
            assert page_reg.email_registration in card_of_reg
            assert page_reg.address_registration in card_of_reg
            assert page_reg.password_registration in card_of_reg
            assert page_reg.password_registration_confirm in card_of_reg
            assert page_reg.registration_btn in card_of_reg
    except AssertionError:
        print('Элемент отсутствует в форме «Регистрация»')

# 3 Форма "Регистрация" Соответствие названий элементов по требованию ______________________________________
def test_names_elements_registration(selenium):
    try:
        page_reg = RegistrPage(selenium)
        assert 'Имя' in page_reg.card_of_registration.text
        assert 'Фамилия' in page_reg.card_of_registration.text
        assert 'Регион' in page_reg.card_of_registration.text
        assert 'E-mail или мобильный телефон' in page_reg.card_of_registration.text
        assert 'Пароль' in page_reg.card_of_registration.text
        assert 'Подтверждение пароля' in page_reg.card_of_registration.text
        assert 'Продолжить' in page_reg.card_of_registration.text
    except AssertionError:
        print('Название элемента в форме «Регистрация» не соответствует Требованию')

# 4 Форма "Регистрация". Проверка валидных значений "Имя" и "Фамилия" ___________________________________________
def test_registration_valid_data(selenium):
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email_reg)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()
    assert page_reg.find_other_element(*AuthLocators.email_confirm).text == 'Подтверждение email'

# 5 Форма "Регистрация". Проверка на уникальность email (дубль) ______________________________________________
def test_registration_invalid_data(selenium):
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()
    assert "Учётная запись уже существует" in page_reg.find_other_element(*AuthLocators.error_account_exists).text


# 6 Форма "Регистрация" ввод имени допустимыми валидными значениями на кириллице длиной 100
@pytest.mark.parametrize("valid_first_name",
                         [(Settings.russian_generate_string) * 100],
                         ids=['russ_symbols=30'])
def test_first_name_by_valid_data(selenium, valid_first_name):
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(valid_first_name)
    page_reg.first_name.clear()
    page_reg.registration_btn.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' not in page_reg.container_first_name.text


# 7 Форма "Авторизация Тест авторизации с  валидными e-mail и паролем ________________________________________
def test_autoriz_valid_email_pass(selenium):
    page = AuthPage(selenium)
    page.email.send_keys(Settings.valid_email)
    page.email.clear()
    page.pass_eml.send_keys(Settings.valid_password)
    page.pass_eml.clear()
    page.btn_enter.click()

    try:
        assert page.get_relative_link() == '/account_b2c/page'
    except AssertionError:
        assert 'Неверно введен текст с картинки' in page.find_other_element(*AuthLocators.error_message).text

@pytest.mark.parametrize("incor_email", [Settings.invalid_email, Settings.empty_email],
                         ids=['invalid_email', 'empty'])
@pytest.mark.parametrize("incor_passw", [Settings.invalid_password, Settings.empty_password],
                         ids=['invalid_password', 'empty'])

# 8 Форма "Авторизация Тест авторизации с  НЕвалидными e-mail и паролем __________________________________________
def test_autoriz_invalid_email_pass(selenium, incor_email, incor_passw):
    page = AuthPage(selenium)
    page.email.send_keys(incor_email)
    page.email.clear()
    page.pass_eml.send_keys(incor_passw)
    page.pass_eml.clear()
    page.btn_enter.click()
    assert page.get_relative_link() != '/account_b2c/page'

# 9 Форма "Авторизация Активные элементы формы Авторизация ______________________________________________________
def test_elements_of_autoriz(selenium):
    page = AuthPage(selenium)
    assert page.menu_tub.text in page.card_of_auth.text
    assert page.email.text in page.card_of_auth.text
    assert page.pass_eml.text in page.card_of_auth.text
    assert page.btn_enter.text in page.card_of_auth.text
    assert page.forgot_password_link.text in page.card_of_auth.text
    assert page.register_link.text in page.card_of_auth.text

# 10 Форма Авторизации, Поля меняются в зависимости от типа авторизации________________________________
def test_placeholder_name_swap(selenium):
    page = AuthPage(selenium)
    page.tub_phone.click()
    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_email.click()
    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_login.click()
    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_ls.click()
    assert page.placeholder_name.text in Settings.placeholder_name

# 11 Переход к форме Восстановление пароля ____________________________________________
def test_forgot_password_link(selenium):
    page = AuthPage(selenium)
    page.driver.execute_script("arguments[0].click();", page.forgot_password_link)
    assert page.find_other_element(*AuthLocators.password_recovery).text == 'Восстановление пароля'

# 12 Форма "Авторизация" после нажатия кнопки "Войти" при регистрации пользователя e-mail, который уже был использован ранее для регистрации. """
def test_registration_and_redir_auth(selenium):
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()
    page_reg.find_other_element(*AuthLocators.redirect_auth).click()
    assert 'Авторизация' in page_reg.find_other_element(*AuthLocators.authorization).text

# 13 Форма "Регистрация" невалидными значениями в поле ввода Имени
@pytest.mark.parametrize("invalid_first_name",
                         [(Settings.empty), (Settings.numbers), (Settings.latin_generate_string), (Settings.special_chars)],
                         ids=['empty', 'numbers', 'latin_symbols', 'special_symbols'])
def test_first_name_invalid_data(selenium, invalid_first_name):
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(invalid_first_name)
    page_reg.first_name.clear()
    page_reg.registration_btn.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' in \
           page_reg.find_other_element(*AuthLocators.error_first_name).text


# 14 Форма Регистрация поле Пароль значения валидны
@pytest.mark.parametrize("valid_password",
                         [(Settings.passw1), (Settings.passw2), (Settings.passw3)],
                         ids=['valid_symbols=8', 'valid_symbols=15', 'valid_symbols=20'])
def test_last_name_valid_data(selenium, valid_password):
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(valid_password)
    page_reg.password_registration.clear()
    page_reg.registration_btn.click()

    assert 'Длина пароля должна быть не менее 8 символов' and \
           'Пароль должен содержать хотя бы одну заглавную букву' and \
           'Пароль должен содержать хотя бы одну прописную букву' and \
           'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру' not in \
           page_reg.password_registration.text


# 15 Форма Регистрация поле Пароль1 Пароль повторно
def test_registration_confirm_password_invalid_data(selenium):
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(Settings.passw1)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.passw2)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()
    assert 'Пароли не совпадают' in page_reg.find_other_element(*AuthLocators.error_password_confirm).text