# Assignment10


## Table of Contents
- [Description](#description)
- [Git Clone Instructions](#git-clone-instructions)
- [Database Management](#database_management)
- [Django CLI Commands](#django_cli_commands)
- [Test](#test)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Code Coverage](#code_coverage)
- [Code Coverage Report](#code_coverage_report)
- [Dependencies](#dependencies)



## Description
This project aims to develop a Django CLI application that enhances property data by leveraging the GEmini API and language models. It will automate rewriting property titles and descriptions, generate comprehensive summaries, and create ratings and reviews. The application integrates Ollama's model for processing, rewrites data using the GEmini API, and stores the updated information in a property table. Additionally, it generates property summaries and insights, storing them in separate tables, providing enriched data for improved property analysis and management.

## Git Clone Instructions

To clone this project to your local machine, follow these steps:

1. **Open terminal (Command Prompt, PowerShell, or Terminal)**

2. **Clone the repository**:
   
   ```git clone https://github.com/M-E-U-E/Assignment_10.git or git clone git@github.com:M-E-U-E/Assignment_10.git```
   
    Go to the Directory:
    ```bash
    cd Assignment_10
    ```
4. **Set Up Virtual Environment**
   
    ```bash
    # Create virtual environment On macOS/Linux:
       python3 -m venv env
       source env/bin/activate

    # Activate virtual environment
    # Create virtual environment On Windows:
       python -m venv env
       venv\Scripts\activate
    ```
    Create a .env file and add this:
    ```
    GEMINI_API_KEY=AIzaSyCevagytgYUSdjbfQ7koD05dcS4B2IWJYE
    ```
    Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
    **Run In docker**
    ```
    docker-compose up --build
    ```
    After set up the docker
    **Run migrations to set up the database schema:**
    ```
    docker-compose exec -it django_app python manage.py makemigrations
    docker-compose exec -it django_app python manage.py migrate
    ```
    if having any issue
    drop the hotel table using this commands then again Compose the Docker:
    ```
    docker exec -it postgres_db psql -U username -d hotel_db
    DROP TABLE hotels;
    ```
    **To see the django application and django admin:**
    ```
    create superuser: docker-compose exec -it django_app python manage.py createsuperuser
    http://localhost:8000/admin/
    ```
## Database Management
    Access the database:
    Using Django Admin: 
    ```
    docker exec -it postgres_db psql -U username -d hotel_db
    ```
    View database tables:
    ```
    \dt [list of the tables]
    ```
    Query specific tables:
   ```
    SELECT * FROM hotels; [see all hotels]
    SELECT * FROM hotels LIMIT 10; [only show 10 hotels]
    SELECT * FROM llm_commands_propertyrating;
    SELECT * FROM llm_commands_summary;
    \q for exit
   ```
   Using PgAdmin:
   ```
   Go to http://localhost:5050/
   Enter these credentials and press the Login button:
   Email Address / Username: admin@admin.com
   Password: admin
   Right click on Servers and then Register > Server
   In General tab, enter Name: LLM
   In Connection tab, enter these details and click Save
   Host name/address: postgres_db
   Username: user
   Password: password
   Then go to Servers > LLM > Databases > hotels_db > Schemas > public > Tables
   To view the AI generated names and description of hotels, right click on the new_hotels table and click on View/Edit Data > All Rows
   To view the AI generated summary of hotels, right click on the hotel_summaries table and click on View/Edit Data > All Rows
   To view the AI generated ratings and reviews of hotels, right click on the hotel_ratings_reviews table and click on View/Edit Data > All Rows
   ```
   


## Django CLI Commands
**Rewrite Hotel Title and Add a Description for the hotel:**
Go to the Bash using this command:
```
docker exec -it django_app bash
```
```
python manage.py rewrite_hotel_data
```
Generate Summaries and Rating for hotel:
```
python manage.py generate_summaries_and_ratings
```

## Test
  Run the testing file:
  ```
   docker exec -it django_app python manage.py test
  ```
 Get the Coverage:
  ```
   docker exec -it django_app coverage run manage.py test
   docker exec -it django_app coverage report

  ```
 
    

## Project Structure
```
Assignment_10/
├── llm/
│   ├── llm/
│   │   ├── pycache/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── llm_commands/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── __init__.py
│   │   │       ├── generate_summaries_and_ratings.py
│   │   │       ├── rewrite_hotel_data.py
│   │   │       └── run_scrapy.py
│   │   └── __init__.py
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── generate_summaries_and_ratings.log
├── manage.py
├── rewrite_hotel.log
└── scraper/
    ├── city_data/
    │   ├── images_of_hotels/
    │   └── json_of_hotels/
    ├── trip/
    │   ├── __pycache__/
    │   ├── db/
    │   └── spiders/
    │       ├── __pycache__/
    │       ├── __init__.py
    │       └── async_trip_spider.py
    └── __init__.py
├── .gitignore             # Gitignore file
├── Dockerfile             # Docker build configuration
├── docker-compose.yml     # Docker Compose setup
├── requirements.txt       # Python dependencies
├── manage.py              # Django management script
└── README.md              # Project documentation

```
## Technologies Used

- Python: Programming language
- Django: Web framework for the CLI application
- PostgreSQL: Database to store property data, summaries, ratings, and reviews
- SQLAlchemy: ORM for database interaction
- Django ORM: ORM for database interaction
- Gemini API: API for rewriting and enhancing property data
- Docker: Containerization for environment consistency
- pytest: Testing framework


  
 ## Dependencies
  All dependencies are listed in requirements.txt. Install them using:

    pip install -r requirements.txt


