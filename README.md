# Wheel Deal

Wheel Deal is a Google Chrome Extension that helps users find the best deals on car rentals. The extension uses web scraping to gather data from popular cars-for-sale websites and provides users with a list of the cheapest available cars.

## Installation

### Chrome Extension
To install the Chrome extension, follow these steps:

1. Make sure you have npm installed.
2. Install Yarn by running the following command in your terminal:

`npm install --global yarn`

3. Check that Yarn has been installed by running the following command in your terminal:

`yarn --version`

4. Navigate to the "Carcow/vite-react-chrome-extension" directory in your terminal.
Run the following command in your terminal to build the extension:

`yarn build`

6. Open Google Chrome and navigate to the Extensions page by typing chrome://extensions in the URL bar.
7. Turn on Developer mode by toggling the switch in the top right corner of the page.
8. Click the Load unpacked button in the top left corner of the page.
9. Select the dist folder inside the Carcow-/vite-react-chrome-extension directory.
10. The Wheel Deal extension is now installed and ready to use!

### Server
To run the server, follow these steps:

1. Make sure you have Python 3 installed.
2. Install memcached by running the following command in your terminal:

`sudo apt-get install memcached`

3. Start the memcached service by running the following command in your terminal:

`sudo service memcached start`

4. Navigate to the wheeldeal directory in your terminal.

### Dependencies
Before you can run the Wheel Deal project, you need to install the following dependencies:

- json
- sys
- shutil
- flask
- csv
- mysql-connector-python
- dotenv
- pymemcache
1. Install the required libraries by running the following command in your terminal:

`pip install example`

### Database

1. Create your own MySQL database
2. Connect your MyhSQL database to the application by modifying code in 'server.py', and 'database.py'
3. Run the following command to start scraping from different cars-for-sale websites (this will populate your database):

`python3 scrapeV1_6_database_mass_search`

### Usage

To start the Wheel Deal project, run the following command:

`python3 server.py`

6. The server is now running and ready to receive requests from the Wheel Deal Chrome extension.



## Contributing

If you would like to contribute to the Wheel Deal project, please follow these steps:

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your changes.
4. Make your changes and commit them to your branch.
5. Push your branch to your forked repository on GitHub.
6. Open a pull request on the original repository.
7. We welcome all contributions, including bug fixes, feature requests, and documentation improvements. Thank you for your support!
