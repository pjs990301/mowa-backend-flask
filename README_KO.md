# mowa-backend-flask

이 프로젝트는 MoWA-backend 프레임워크 및 프론트엔드 프레임워크 서비스를 제공합니다

## 내용

<!-- TOC -->
* [mowa-backend-flask](#mowa-backend-flask)
  * [내용](#내용)
  * [시작하기](#시작하기)
    * [설치](#설치)
  * [사용](#사용)
    * [프로그램 실행](#프로그램-실행)
    * [구성](#구성)
  * [Demo](#demo)
    * [Back-end (Flask)](#back-end-flask)
      * [1. 유저 API](#1-유저-api)
      * [2. 활동 API](#2-활동-api)
      * [3. 모델](#3-모델)
    * [Front-end (Dash)](#front-end-dash)
      * [1. 유저 관리](#1-유저-관리)
      * [2. 유저 통계](#2-유저-통계)
  * [라이선스](#라이선스)
<!-- TOC -->

## 시작하기

### 설치

1. project repository 복제

    ```sh
    git https://github.com/oss-inc/mowa-backend-flask
    ```

2. Python 가상 환경 셋팅

    ```sh
    conda create -n mowa-backend-flask python=3.8
    ```

3. Flask 서버 설치

    ```sh
    pip install -r requirements.txt
    ```

## 사용

### 프로그램 실행

1. 플라스크 서버용 `app.py` 실행(Back-end)

    ```sh
    python -m flask run 
    ```

2. 관리 페이지 `app.services.dashboard.py` 실행 (프론트엔드)

    ```sh
    python -m app.services.dashboard run
    ```

### 구성

1. `app/databases/db_info.json` 데이터베이스 설정

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

2. `__init_.py`의 서버 호스트 및 포트 설정

    ```python
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=8000)
    ```
    > 호스트 IP 및 포트 번호를 변경할 수 있습니다.<br> IP 기본값은 `0.0.0.0`이고 포트 기본값은 `8000`입니다.

3. 웹페이지 `app.services.dashboard.py`의 호스트 및 포트 설정
    
    ```python
    if __name__ == '__main__':
        server.run(debug=True, host="0.0.0.0", port=8050)
    ```
    > 호스트 IP 및 포트 번호를 변경할 수 있습니다.<br> IP 기본값은 `0.0.0.0`이고 포트 기본값은 `8050`입니다.

4. mysql 쿼리를 사용한 데이터베이스 설정
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
5. `app.services.controller.callback.py`에서 요청 URL 변경
      ```python
      if tab == 'user-tab-1':
            response = requests.get("http://{ServerIP}:{ServerPort}/user/users")
            return response.json()
      ```
   > 대시보드를 사용하려면 `서버 IP 및 서버 포트`로 변경해야 합니다.
## Demo
### Back-end (Flask)
#### 1. 유저 API
![swagger_1.png](https://github.com/oss-inc/mowa-backend-flask/blob/main/img/swagger_1.png?raw=true)
#### 2. 활동 API
![swagger_2.png](https://github.com/oss-inc/mowa-backend-flask/blob/main/img/swagger_3.png?raw=true)
#### 3. 모델
![swagger_3.png](https://github.com/oss-inc/mowa-backend-flask/blob/main/img/swagger_2.png?raw=true)

### Front-end (Dash)
#### 1. 유저 관리
![dashboard_1.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_1.png?raw=true)
![dashboard_2.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_2.png?raw=true)
![dashboard_3.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_3.png?raw=true)
![dashboard_4.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_4.png?raw=true)

#### 2. 유저 통계
![dashboard_5.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_5.png?raw=true)
![dashboard_6.png](https://github.com/oss-inc/mowa-backend-flask/blob/develop/img/dashboard_6.png?raw=true)

## 라이선스

이 프로젝트는 MIT 라이센스로 라이센스가 부여됩니다. 자세한 내용은 [LICENSE.md](https://github.com/oss-inc/mowa-backend-flask/block/develop/LICENCE) 파일을 참조하십시오

