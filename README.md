# AUTOMATE RESTAURANT MENU
#### Video Demo: <URL AQUI>  
#### Description: 

This project aims to create a web application that utilizes OCR (Optical Character Recognition) technologies and Artificial Intelligence to extract information from restaurant menus and convert it into a structured JSON format. The goal is to automate the digitization of menus, eliminating the need for manual entry into delivery apps and other services in the sector.
Currently, the project is in its initial stage and is developed using the Flask framework, integrating Google's Gemini API to process and organize the data extracted from menu images. The long-term goal is for the API to be able to post directly to third-party application endpoints, fully automating the registration process that is currently done manually.

##### Key Features
1. Menu Image Upload
The application allows users to upload images of menus. The system supports image files in PNG, JPG, and JPEG formats. After the image is uploaded, the system checks if the file has a valid extension before storing it on the server. This feature is one of the main characteristics of the application, as it enables users to directly upload an image from their device for processing.

2. Text Extraction from Images (OCR)
The core of the project is the use of the <mark>pytesseract</mark> library, a Python interface for Tesseract OCR, to extract text from the uploaded images. Tesseract is a very efficient tool for text recognition in images and is widely used for document and sign scanning, for example. From the menu image, <mark>pytesseract</mark> attempts to identify the text present, such as product names, descriptions, and prices.

3. Generation of JSON with Extracted Data
After text extraction, the application uses the Google Gemini API to process the content and organize the information into a structured JSON format. The API is configured with an API key, which must be provided by the user in the <mark>.env</mark> configuration file. From the extracted text, the AI model is fed with a specific prompt asking it to analyze and organize the menu information. The final result is a list of JSON objects, where each object represents a product with three fields: title (product name), description (product description), and price (product price).

For example, if the menu image contains information such as:

"Product 1 - Product Description 1 - $10.00"
"Product 2 - Product Description 2 - $20.00"

The generated JSON would be:

```json
[
  {
    "title": "Product 1",
    "description": "Product Description 1",
    "price": "$10.00"
  },
  {
    "title": "Product 2",
    "description": "Product Description 2",
    "price": "$20.00"
  }
]
```
This JSON can be used for various purposes, such as feeding mobile apps, websites, or even for data analysis.

4. Storage in SQLite Database
After generating the JSON with the menu information, the system stores this data in a local SQLite database. The database is designed to store the responses in JSON format, allowing the application to access the data whenever necessary. The <mark>shop_res</mark> table was created to store the generated JSON content for each processed image. Using SQLite makes local storage and quick data querying easy, without the need for a more complex database management system.

5. Viewing Results
After processing the menu, the results can be viewed on the results page. The user interface is created using HTML and CSS to provide a simple and straightforward experience. On the results page, the data stored in the database is displayed to the user. This page contains a table or list of the extracted products, showing the title, description, and price of each item. This allows the user to see how the system interpreted and organized the menu information.

6. Data Cleanup and Deletion
The application also includes a feature that allows the deletion of all records stored in the database. This can be useful for clearing old data and starting fresh with new menu image uploads. The deletion functionality is easy to use and helps keep the database organized, especially as the number of uploads increases over time.

##### Technologies Used
* Flask: Web framework used as the foundation for the application. Flask is lightweight and flexible, making it easy to build APIs and user interfaces.
* pytesseract: Python library for Optical Character Recognition (OCR). Used to extract text from menu images.
* Google Gemini API: AI platform that analyzes and organizes the data extracted from images into a JSON format.
* SQLite: Lightweight relational database used to store the extracted information from the images.
* HTML/CSS: Technologies used to create the user interface, enabling user interaction with the system.

##### How to Use

Prerequisites
* Install dependencies: To run the project, you need to have Python installed and the dependencies listed in the <mark>requirements.txt</mark> file. You can install the dependencies using the following command:
```bash
pip install -r requirements.txt
```
* Install Tesseract: Tesseract OCR must be installed on your system [here](https://github.com/tesseract-ocr/tesseract). After installation, you will need to configure the path to the Tesseract executable in the code.

* Configure Gemini API: The project uses Google's Gemini API to generate JSON from the extracted information. To use the API, you need to obtain a valid API key from Google Cloud. Add this key to the project's <mark>.env</mark> file, setting the <mark>TOKEN_API_GEMINI</mark> variable.

* Running the Application
To run the application, simply execute the following command:
```bash
python app.py
```
The application will be available at <mark>http://localhost:5000</mark>, where you can upload a menu image and view the results.
