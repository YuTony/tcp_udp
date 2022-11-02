### TCP server
Ожидает подключения клиентов, выводит их сообщения и возвращает ответные
```
python main.py -ts 127.0.0.1 8080
```

### TCP client
Отправляет сообщение, принимает ответное и ожидает дальнейшего ввода
```
python main.py -tc 127.0.0.1 8080
```

### UDP server
Принимает сообщения, выводит их и возвращает отправителю
```
python main.py -us 127.0.0.1 8080
```

### UDP client
Отправляет одно сообщение, принимает ответное и завершается
```
python main.py -uc 127.0.0.1 8080
```