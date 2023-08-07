# AIFinanceProject
Google I/O Extended Hackathon: Web, Mobile, and AI Focus

## Overview
As a financial planner/investor, I'd like to assess how location (geography/geospatial info) affects financial decision-making.  This project tries to find if any connection between security performance and local economic behavior/news.  The inspiration is the Gamestop (short) story of 2021 ("Gaming Wall Street" - hbo max original series ; "The Lesson Of GameStop: Investing Is Not A Game" – Forbes Advisor).


## Getting Started

To set up and run the AIFinanceProject App on your local machine, follow the steps below:

### Prerequisites

- Python 3.10

### Installation

1. Clone the repository to your local machine and Change Directory:

```
git clone https://github.com/wilberh/AIFinanceProject.git
cd AIFinanceProject
```
2. Create Virtual Env and Install Requirements:

```
python -m venv env
env\Scripts\activate  # On Windows
source env/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### Database Setup and Admin Access

1. **Set up the database:**

   Run the following command(s) to apply the necessary migrations:

   ```
   python manage.py migrate
   ```

2. **Create a superuser for admin access:**

   ```
   python manage.py createsuperuser
   ```

3. **Run the development server:**

   Start the development server with the following command:

   ```
   python manage.py runserver
   ```

4. **Access the UI for the Django-Rest Framework API:**

   Go to `http://127.0.0.1:8000/api/aifinance` in your web browser and use any of follwoing payloads to 
   (1) get stock price, or (2) trend by country.

| API endpoint (GET)  |    Task       |    Payload    |
| -------------       | ------------- | ------------- |
| /api/aifinance      |    quote      | {"task": "quote", "ticker": "AAPL" *[OPTIONAL: ,"strt_dt": "2023-06-29", "end_dt": "2023-07-28"]*}             |
| /api/aifinance      |    trend      | {"task": "trend", "company": "Apple", "country": "us" *[OPTIONAL: ,"strt_dt", "2023-06-29", "end_dt": "2023-07-28"]*}  |

## Bugs and Feature Requests
Have a bug or a feature request? Please open an [issue](https://github.com/wilberh/AIFinanceProject/issues/new).

## License
This project is [MIT](https://github.com/your_username/your_repository/blob/master/LICENSE) licensed.

## Feedback
For feedback or any inquiries, feel free to contact and connect with me on LinkedIn:
[LinkedIn](https://www.linkedin.com/in/wilberhdez26/)

