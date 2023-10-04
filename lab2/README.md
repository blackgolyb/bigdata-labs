# Лабораторна робота 2 (Kafka)

![](./public/)

## Run production version

### Dependencies

Для використання вам буде потрібені:

-   [Docker](https://www.docker.com/)
-   [docker-compose](https://docs.docker.com/compose/)
-   `make`

### Installation and start step-by-step

Поперше потрібно склонувати репозиторій

```bash
git clone https://github.com/blackgolyb/bigdata-labs.git
```

Потім переходимо до папки з лоборатоною

```bash
cd ./bigdata-labs/lab2
```

Та запускаємо всі компоненти за допомогою наступної команди:

```bash
make up_deploy
```

Тепер переходемо за посиланням для відкриття візуалізатора топа 10 транзакцій.
Посилання: [http://localhost:8080/](http://localhost:8080/)

Після використання сервери можна зупинити так:

```bash
make down_deploy
```

## Modification

### Dependencies

Якщо ж ви бажаете запустити сервер у режимі розробки, то вам потрібно переконатися, що ви маєте наступні залежності:

-   python >= 3.11
-   poetry
-   docker
-   docker-compose
-   make

### Installation step-by-step

Поперше потрібно склонувати репозиторій

```bash
git clone https://github.com/blackgolyb/bigdata-labs.git
```

Потім переходимо до папки з лоборатоною

```bash
cd ./bigdata-labs/lab2
```

Переходимо до папки `producer` та встановлюємо залежності для `Producer`:

```bash
cd producer
poetry install
```

Переходимо до папки `consumer` та встановлюємо залежності для `Consumer`:

```bash
cd ../consumer
poetry install
```

### start up step-by-step

#### Kafka

---

Для запуску `kafka` відкрийте термінал та перейдіть в папку проета та запустіть наступну команду:

```bash
make up
```

Для зупинки `kafka` відкрийте термінал та перейдіть в папку проета та запустіть наступну команду:

```bash
make down
```

#### Producer

---

Для запуску `producer` відкрийте термінал та перейдіть в папку проета:

```bash
cd producer
poetry shell
```

Та запустіть наступну команду:

```bash
python main.py
```

Для зупинки `producer` просто зупиніть процес. Наприклад натисніть <kbd>⌃ Control</kbd> + <kbd>C</kbd>

#### Consumer

---

Для запуску `consumer` відкрийте термінал та перейдіть в папку проета:

```bash
cd consumer
poetry shell
```

Та запустіть наступну команду:

```bash
python main.py
```

Тепер переходемо за посиланням для відкриття візуалізатора топа 10 транзакцій.
Посилання: [http://localhost:8080/](http://localhost:8080/)

Для зупинки `consumer` просто зупиніть процес. Наприклад натисніть <kbd>⌃ Control</kbd> + <kbd>C</kbd>
