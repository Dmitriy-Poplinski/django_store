# DB Schema
[DB_schema.drawio](DB_schema.drawio)

# Django Store

This is a Django-based project designed to provide a robust web application framework. The project includes several dependencies for handling various functionalities, such as web requests, image processing, and integrating payment systems.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Dmitriy-Poplinski/django_store
    cd your-repo-name
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run the development server:

1. **Apply migrations:**

    ```sh
    python manage.py migrate
    ```

2. **Start the server:**

    ```sh
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000/`.

## Features

- **Django 5.0.3:** The core web framework providing the foundation for the project.
- **Image processing with Pillow:** Handle image uploads and manipulations.
- **Payment integration:** LiqPay integration for processing payments.
- **Environment variable management:** Use `python-dotenv` to manage environment-specific settings.
- **HTTP requests:** Utilize `requests` library for making external HTTP requests.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:

    ```sh
    git checkout -b feature/your-feature-name
    ```

3. Make your changes and commit them:

    ```sh
    git commit -m "Add some feature"
    ```

4. Push to the branch:

    ```sh
    git push origin feature/your-feature-name
    ```

5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Dependencies

Here is a list of the dependencies used in this project as specified in `requirements.txt`:

- **asgiref~=3.7.2:** ASGI (Asynchronous Server Gateway Interface) reference implementation.
- **certifi==2024.2.2:** Python package for providing Mozilla’s CA Bundle.
- **charset-normalizer==3.3.2:** Library for detecting the character encoding of text.
- **Django==5.0.3:** High-level Python web framework.
- **idna~=3.6:** Internationalized Domain Names in Applications (IDNA) support.
- **liqpay-python==1.0:** Python client for the LiqPay API.
- **pillow~=10.2.0:** Python Imaging Library (PIL) fork.
- **requests==2.31.0:** Simple HTTP library for Python.
- **sqlparse==0.4.4:** SQL parsing library.
- **tzdata==2024.1:** Time zone database for dateutil.
- **urllib3==2.2.1:** HTTP client for Python.
- **python-dotenv~=1.0.1:** Read key-value pairs from a `.env` file and set them as environment variables.

## Contact

For any inquiries or support, please contact [dmytro.poplinski@gmail.com].

---

Feel free to customize this `README.md` to better suit your project's needs.
