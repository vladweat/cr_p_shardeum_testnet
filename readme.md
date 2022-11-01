## Требования 

1. Установлен Microsoft Visual C++ 14.0 и выше. [Сюда](https://learn.microsoft.com/en-us/answers/questions/136595/error-microsoft-visual-c-140-or-greater-is-require.html) если нет
   

## Настройка

1. Создать виртуальное окружение 

```python
python -m vevn .
```

2. Активировать виртуальное окружение

- linux/macos
```python
source Scripts/activate
```

 - windows
```python
Scripts\activate.bat   
```

Когда-нибудь я точно начну писать сразу в venv.

3. Установить библиотеки

```python
(venv) pip install -r requirements.txt
```

4. Скопировать файл `.env copy`, переименовать файл на `.env` добавить необходимые переменные в файл

## Функционал

1. Запуск

```python
(venv) python main.py
```


## Для понимания

`client.create_accounts(10)` - создание 10 аккаунтов в файл wallets.txt
`client.get_adresses()` - получение адресов из wallet.txt
`client.disperse_smh_to_wallets(client.get_adresses())` - рассылка по кошелькам иwallet.txt
`client.get_wallets_balance(сюда передать кошельки)` - вывод баланса кошельков из wallet.txt
`client.send_smh_to_main(сюда передать кошельки)` - сбор всех токенов с кошельков на кошелек из .env
`client.deploy_contract_on_wallets(сюда передать кошельки)` - деплой контракта Attendence.sol с кошельков
