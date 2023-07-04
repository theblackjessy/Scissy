# SCISSY

# Introduction
SCISSY is a web-based tool that allows users to shorten long URLs into shorter and more manageable links. It provides a simple, user-friendly interface to generate short URLs, track clicks, and manage the URLs and also user data.

The application is built using the Flask framework, a lightweight and extensible web framework for Python. It utilizes a SQLite database for storing URL mappings and tracking url clicks. The frontend is designed using HTML, CSS, and JavaScript, with support for generating QR codes for shortened URLs. And also other necessary libraries like matplotlib for generating charts for analytics, flask-cache for caching and also flask-limiter for rate limiting etc.

# Features
SCISSY offers the following features:

1. **Shorten long URLs:** Users can input a long URL and generate a shorter, more compact and unique version. The application generates a unique shortcode for each URL, which is used to access the original URL when the shortened link is visited.
2. **Customizable URLs:** Users have the option to customize the shortcode of their shortened URL by providing a custom alias.
3. **Click Tracking and Analytics:** The application tracks the number of clicks received for each shortened URL. Users can view analytics data such as total clicks, clicks per day, and the most clicked day for each shortened URL with graphical representation.
4. **QR Code Generation:** The application generates QR codes for each shortened URL, making it convenient for users to download and share URLs across devices.
5. **History:** For users who would like to browse through URLs they previously shortened, the application also includes a history feature. URLs that were shortened by a user are stored and made accessible to users any time.  
6. **Password-Protected URLs:** One unique feature about this application is the option to secure shortened URLs 
   with passwords. For users that want to shorten and secure URLs contain sensitive data, you can choose to protect 
   your shortened URLs with a password 
   for added security. 

# Installation
To set up the URL Shortener application, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/theblackjessy/Scissy
   ```
2. Change into the project directory:
   ```
   cd Scissy
   ```
3. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Set environment variable:
   - On Windows:
     ```
     set FLASK_APP=app.py
     ```
   - On MacOS/Linux:
     ```
     export FLASK_APP=run.py
     ```
7. Create database:
   ```
   flask shell
  
   db.create_all()
   
   quit()
   ```

8. To run and use the application locally, follow the steps above and execute this command:

```
python app.py
```

# Live Link

Deployed site: [scissy.pythonanywhere.com](https://scissy.pythonanywhere.com/) - hosted via [pythonanywhere](https://www.pythonanywhere.com) 


# Usage and How-tos.

This tool can be accessed via the deployed site or a local copy of the project.

With the application now running, you can test out all the functionalities of the application. 
From the home page, click the _SIGN UP_ button to create a new account. This would give you access to all the 
features of the application as unauthenticated users are restricted to shortening URLs only. 
***

![image0 (2)](https://github.com/theblackjessy/Scissy/assets/102354943/7a7bab3b-0390-4b4e-b4ff-7a6e0193124b)

***

1. Generating short URLs: Go to the home page and click on the 'shorten your url' button, this will load up a new page.
   On the new page, paste in a long URL you'd like to trim and click the 'shorten' button. A new clean and short URL would be generated for you.
   
3. Customizing shortened URLs: To customize the shortened URL to your taste, there's a second input form that allows you
   to customize
   the second half of the generated URL. Enter what you prefer and just like before, click the'shorten' button.
   <br> P.S: All blank spaces will be converted to hyphens.
4. Generating QR Codes: With the short URL generated for you, a QR code will automatically be generated for you. You can also download this image to your device and share it. 
5. Viewing and clearing your SCISSY history: To see a history of URLs you've previously shortened, click
   'Get History'. This would take show you a list of all your URLs, with their respective creation dates. 
   Below the list, you have the CLEAR HISTORY button that will wipe all your generated URLs from the database (giving 
   you the chance to start afresh and fresh :)

Some other feature soon to be added is the View analytics feature. For each URL in your SCISSY history, you can view the analytics and monitor how your shortened URL has been performing.<br>


# Code Base Structure
https://jessyblog.hashnode.dev/creating-a-url-shortener
## Authentication
Users are required to be logged in to use the website. This is to enable the database to map generated links and QR codes to the specific users who created them; thus making sure that each user can only view, edit or delete the links they created.<br>

Routes: sign up . log in . log out
If an unauthenticated user tries to access a protected route, they get redirected to the login page with an error message.

## Authorization
By including user_id=current_user.id as a parameter in the Link.query.filter_by() function, Scissor ensures that users can only interact with the links they created by themselves when visiting the dashboard, history, analytics, update, delete and QR code generation routes.

## Analytics
This page - accessed via https://sciz.site/<short_link>/analytics - shows the details of a specified shortened link and its QR code in the same format as the dashboard but optimized for a single card. <br>

If the link passed into the route does not exist, the 404 template is rendered instead.

# Acknowledgements
SCISSY is built on top of the Flask micro web framework and utilizes various open-source libraries and 
extensions. The development of this application was inspired by the need for a simple and efficient URL shortening 
solution. This project was made possible thanks to the Flask community, the contributors of the used extensions, and all the developers 
involved in creating the underlying technologies. Most especially also the tutors and everyone at [Altschool Africa](https://altschoolafrica.com) for the opportunity to build this application as the capstone project.

# License
The SCISSY application is open source and released under the [MIT License](LICENSE). You are free to use, modify, and distribute the application according to the terms of the license.

# Contributing
Contributions to SCISSY are welcome! If you find any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue on the project's GitHub repository.
