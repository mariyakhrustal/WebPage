# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов"""
        try:
            with open("templates/contacts.html", "r", encoding="utf-8") as file:
                content = file.read()
            self.send_response(200)  # Отправка кода ответа
            # Отправка типа данных, который будет передаваться
            self.send_header("Content-type", "text/html")
            self.end_headers()  # Завершение формирования заголовков ответа
            self.wfile.write(bytes(content, "utf-8"))  # Тело ответа
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Page Not Found</h1>")

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """
        try:
            # Получаем длину тела запроса (Content-Length)
            content_length = int(self.headers['Content-Length'])
            # Читаем данные из тела запроса
            post_data = self.rfile.read(content_length)
            # Печатаем полученные данные как текст
            print("Received data:", post_data.decode('utf-8'))
            # Отправляем успешный ответ с кодом 200
            self.send_response(200)
            # Указываем тип ответа, в данном случае - текстовый
            self.send_header('Content-type', 'text/plain')
            self.end_headers()  # Завершаем формирование заголовков
            # Отправляем клиенту сообщение "Data received"
            self.wfile.write(b'Data received')
        except Exception as e:
            # В случае ошибки (например, если данные не могут быть прочитаны)
            self.send_response(500)  # Отправляем код ошибки 500 (внутренняя ошибка сервера)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<h1>500 - Internal Server Error: {str(e)}</h1>".encode("utf-8"))


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
