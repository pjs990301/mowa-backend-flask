# mowa-backend-flask

The project provides MoWA back-end framework and front-end framework services

## Content

<!-- TOC -->
* [mowa-backend-flask](#mowa-backend-flask)
  * [Content](#content)
  * [Getting Started](#getting-started)
    * [Installing](#installing)
  * [Usage](#usage)
    * [Execution Program](#execution-program)
    * [Configuration](#configuration)
  * [Demo](#demo)
    * [Back-end (Flask)](#back-end-flask)
    * [Front-end (Dash)](#front-end-dash)
  * [License](#license)
<!-- TOC -->

## Getting Started

### Installing

1. Clone the project repository

    ```sh
    git https://github.com/oss-inc/mowa-backend-flask
    ```

2. Python Virtual Environment Setup

    ```sh
    conda create -n mowa-backend-flask python=3.8
    ```

3. Installing the Flask Server

    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Execution Program

1. Run `app.py` for Flask Server(Back-end)

    ```sh
    python -m flask run 
    ```

2. Run `app.services.dashboard.py` for Management page (Front-end)

    ```sh
    python -m app.services.dashboard run
    ```

### Configuration

1. Database setting with `app/databases/db_info.json`

    ```json
    {
      "Database": {
        "host": "DATABASE_IP",
        "user": "USER_NAME",
        "password": "USER_PASSWORD!",
        "database": "DATABASE_NAME"
      }
    }
    ```

2. Server Host and Port setting in `__init__.py`

    ```python
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=8000)
    ```
    > You can change host IP and port number<br> The IP default is `0.0.0.0` and the port default is `8000`.

3. Web page Host and Port setting in `app.services.dashboard.py`
    
    ```python
    if __name__ == '__main__':
        server.run(debug=True, host="0.0.0.0", port=8050)
    ```
    > You can change host IP and port number<br> The IP default is `0.0.0.0` and the port default is `8050`.

4. Database setting with mysql query
    <details>
    <summary>SQL Code </summary>
    <div markdown="1">
    
    ```sql
    create table users
    (
        id       int auto_increment
            primary key,
        name     varchar(255) not null,
        email    varchar(255) not null,
        password varchar(255) not null,
        constraint email
            unique (email)
    );
    
    create table activity
    (
        id             int          not null,
        email          varchar(255) not null,
        date           date         not null,
        warning_count  int          null,
        activity_count int          null,
        fall_count     int          null,
        primary key (id, date, email),
        constraint activity_ibfk_1
            foreign key (id) references users (id)
                on update cascade on delete cascade,
        constraint activity_ibfk_2
            foreign key (email) references users (email)
                on update cascade on delete cascade
    );
    
    create table profile
    (
        id    int          not null
            primary key,
        email varchar(255) null,
        src   varchar(255) null,
        constraint profile_ibfk_1
            foreign key (id) references users (id)
                on update cascade on delete cascade,
        constraint profile_ibfk_2
            foreign key (email) references users (email)
                on update cascade on delete cascade
    );
    ```
    </div>
    </details>
5. Change Request URL in `app.services.controller.callback.py`
      ```python
      if tab == 'user-tab-1':
            response = requests.get("http://{ServerIP}:{ServerPort}/user/users")
            return response.json()
      ```
   > If you are going to use the dashboard, you should change to `server IP and server port`.
## Demo
### Back-end (Flask)
1. User API
![swagger_1.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/swagger_1.png?raw=true)
2. Activity API
![swagger_2.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/swagger_2.png?raw=true)
3. Model
![swagger_3.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/swagger_3.png?raw=true)

### Front-end (Dash)
1. User Management
![dashboard_1.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_1.png?raw=true)
![dashboard_2.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_2.png?raw=true)
![dashboard_3.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_3.png?raw=true)
![dashboard_4.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_4.png?raw=true)

2. User Statistics
![dashboard_5.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_5.png?raw=true)
![dashboard_6.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_6.png?raw=true)

## License

This project is licensed under the MIT License - see
the [LICENSE.md](https://github.com/oss-inc/mowa-backend-flask/blob/develop/LICENSE) file for details


