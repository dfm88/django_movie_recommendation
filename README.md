## Contents
- [Intro](#intro)
- [Models](#models)
  - [User Models](#user-models)
  - [Movie Models](#movie-models)
  - [Recommendation Models](#recommendation-models)
- [Views](#views)
  - [User Views](#user-views)
  - [Movie Views](#movie-views)
  - [Recommendation Views](#recommendation-views)

## Run
- [Run from docker-compose](#run-from-docker-compose)

## Next
- [Todo](#todo)

__________
__________
## [Intro](#intro)

The structure of the projects follows for most parts the following guidelines https://github.com/HackSoftware/Django-Styleguide. Shortly, every app has a `selector` file where the __reading__ operations business logic lives and a `service` file for the __writing__ operations.

Rest Framework serializers are used only to serialize object and to check validity for input data. Validation in general is inside the models `clean` method and on models `constraints`.

Authentication is handled by `djangorestframework-simplejwt` library and filtering is handled by `django-filter` library.

## [Models](#models)

* **common/models:BaseModel**

    Abstract model to handle common columns

### [User Models](#user-models)

* **user/models:UserCustom**

    Simply inherits from Django default `AbstractUser` model.

### [Movie Models](#movie-models)

* **movie/models:Movie**

    Has a title and a genre. It has a many-to-many relationship with `User` by the `UserWatchedMovie` through table, a many-to-many relationship with `Platform`, a many-to-many relationship with `User` by the `UserRecommendMovie` through table.

* **movie/models:Platform**

    A movie can belongs to different platform and viceversa

### [Recommendation Models](#recommendation-models)

* **recommendation/models:UserRecommendMovie**

    Bridge table for many-to-many relation `Movie-UserCustom`, it has a `unique_toghether` constraint so that one user can recommend only a movie. It halso has a `vote` and `description` attribute related to the recommendation.

## [Views](#views)

### [User Views](#user-views)

* **user/views:UserRegistrationView**

    ```shell
    /user/register
    ```

    Creates a new user

    _body_
    ```json
    {
        "username": "user1",
        "email": "user1@mmail.com",
        "password": "Passw0rd!"
    }
    ```

    __example__
    ```shell
    curl -X POST 'http://127.0.0.1:7777/user/register' \
    --header 'Content-Type: application/json' \
    --data '{
        "username": "user1",
        "email": "user1@mmail.com",
        "password": "Passw0rd!"
    }'
    ```

    ```shell
    /user/login
    ```

    _body_
    ```json
    {
        "username": "user1",
        "email": "user1@mmail.com",
        "password": "Passw0rd!"
    }
    ```

    __example__
    ```shell
    curl -X POST 'http://127.0.0.1:7777/user/login' \
    --header 'Content-Type: application/json' \
    --data '{
        "username": "user1",
        "password": "Passw0rd!"
    }'
    ```

    ```shell
    /user/login/refresh
    ```

    to refresh JWT token

### [Movie Views](#movie-views)

* **movie/views:MovieListCreateView**

    Authentication is required only for writing operation.

    For reading operation it can leads to different result, for instance the possibility to filter by watched/unwatched movies

    ```shell
    /movie/
    ```

    **GET**

    Returns the list of movies with recommendation and platform references.

    * Available filters:

        * `platform: str`
        * `has_watched: bool`
        * `recommend_by: str`
        * `recommend_by_others: bool`

    * Available ordering options:

        * `order_by_title: str`

    __example no auth__
    ```shell
    curl -X GET "http://127.0.0.1:7777/movie/" \
    --header "Content-Type: application/json"
    ```

    __example auth__
    ```shell
    BEARER_TOKEN=""
    curl -X GET "http://127.0.0.1:7777/movie/" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $BEARER_TOKEN"
    ```

    **POST**

    Creates a new movie

    _body_
    ```json
    {
        "title": "IT",
        "genre": "HORROR",
        "platforms": [
            {
                "name": "NETFLIX"
            }

        ]
    }
    ```

    __example__
    ```shell
    BEARER_TOKEN=""
    curl -X POST "http://127.0.0.1:7777/movie/" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $BEARER_TOKEN" \
    --data '{
        "title": "IT",
        "genre": "HORROR",
        "platforms": [
            {
                "name": "NETFLIX"
            }

        ]
    }'
    ```

* **movie/views:MovieRetrieveView**

    ```shell
    /movie/{slug-title}
    ```

    **GET**

    Returns the detail of a single movie

    __example no auth__
    ```shell
    curl -X GET "http://127.0.0.1:7777/movie/{movie-slug-title}" \
    --header "Content-Type: application/json"
    ```

    __example auth__
    ```shell
    BEARER_TOKEN=""
    curl -X GET "http://127.0.0.1:7777/movie/{movie-slug-title}" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $BEARER_TOKEN"
    ```

* **movie/views:MovieSwitchWatched**

    ```shell
    /movie/{slug-title}
    ```

    **POST**

    Set and unset the association between a user that watched a movie

    __example__
    ```shell
    BEARER_TOKEN=""
    curl -X POST "http://127.0.0.1:7777/movie/switch_watched/{movie-slug-title}" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $BEARER_TOKEN"
    ```

### [Recommendation Views](#recommendation-views)

* **recommendation/views:RecommendationMovieListCreateView**

    Authentication is required only for writing operation.


    ```shell
    /recommendation/movie/{slug-title}
    ```

    **GET**

    Returns the list of all recommendation for a given movie.

    * Available filters:

        * `platform: str`
        * `user: str`

    * Available ordering options:

        * `order_by: Literal['vote', 'platform']`

    __example__
    ```shell
    curl -X GET "http://127.0.0.1:7777/recommendation/movie/{slug-title}" \
    --header "Content-Type: application/json"
    ```

    **POST**

    Creates a new recommendation. If the specified platform was not yet associated to the movie, will be added to the available platforms of the movie

    _body_
    ```json
    {
        "vote": 7,
        "comment": "nice",
        "platform": {
            "name": "DISNEY_PLUS"
        }
    }
    ```

    __example__
    ```shell
    BEARER_TOKEN=""
    curl -X POST "http://127.0.0.1:7777/recommendation/movie/{slug-title}" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $BEARER_TOKEN" \
    --data '{
        "vote": 7,
        "comment": "nice",
        "platform": {
            "name": "DISNEY_PLUS"
        }
    }'
    ```

* **recommendation/views:RecommendationUserListView**

    ```shell
    /recommendation/user/{username}
    ```

    **GET**

    Returns the list of all recommendation for a given user.

    * Available filters:

        * `platform: str`
        * `user: str`

    * Available ordering options:

        * `order_by: Literal['vote', 'platform']`

    __example__
    ```shell
    curl -X GET "http://127.0.0.1:7777/recommendation/user/{username}" \
    --header "Content-Type: application/json"

__________
__________

## [Run from docker-compose](#run-from-docker-compose)

The Django server is exposed on port `7777`
```shell
docker compose -f django_movie_recommendation/docker/docker-compose.yaml up --build
```

To run tests, from a different terminal run
```shell
docker exec movie_recomm python django_movie_recommendation/manage.py test tests
```

__________
__________

## [Todo](#todo)

* pagination
* complete tests
* caching
