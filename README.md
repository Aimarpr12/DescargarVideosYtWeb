# YouTube Video Downloader

This is a Flask-based web application that allows users to download YouTube videos and their audio in MP3 format. The application also includes a check for copyrighted content and prompts the user for confirmation before proceeding with the download.

## Features

- Download YouTube videos in the highest resolution available.
- Extract and download only the audio in MP3 format.
- Check for copyrighted content and prompt the user for confirmation.
- Simple and user-friendly web interface.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Installation

### Prerequisites

- Python 3.7 or higher
- [YouTube Data API Key](https://developers.google.com/youtube/registering_an_application)

### Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/PRSpidy/YouTubeVideoDownloader.git
    cd YouTubeVideoDownloader
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Create a `.env` file** and add your YouTube Data API Key:

    ```plaintext
    API_KEY=YOUR_YOUTUBE_API_KEY
    ```

6. **Create the downloads directory**:

    ```bash
    mkdir downloads
    ```

## Usage

1. **Run the Flask application**:

    ```bash
    python app.py
    ```

2. **Open your browser and go to** `http://127.0.0.1:8888`.

3. **Enter the YouTube video URL** you want to download in the provided input field and click on `Download Video` or `Download Audio`.

4. If the video has copyrighted content, a warning pop-up will appear. You can choose to continue with the download or cancel it.

5. The downloaded files will be saved in the `downloads` directory.

## Configuration

### Environment Variables

The application uses the following environment variables:

- `API_KEY`: Your YouTube Data API Key.

Make sure to create a `.env` file in the root of the project with the required variables.

### Application Structure

- `app.py`: The main Flask application file.
- `templates/index.html`: The HTML template for the web interface.
- `static/images/ytlogo.png`: The YouTube logo used in the application.
- `downloads/`: The directory where downloaded files are saved.

### Customizing the Web Interface

You can modify the HTML and CSS files in the `templates` and `static` directories to customize the appearance of the web interface.

## Contributing

If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.
