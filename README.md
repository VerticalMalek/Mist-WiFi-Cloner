## Mist WiFi Cloner

This script automates the process of cloning WiFi configurations in MistAI through an API. It allows you to select a site, list available WiFis, and clone them with a new SSID.

### Features
- List all available sites in your organization.
- List all available WiFis in a selected site.
- Clone a WiFi configuration with a new SSID.
- Choose how many times to clone the WiFi and whether to set a new name for each clone.

### Prerequisites
- Python 3.x
- `requests` library
- `python-dotenv` library

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. (Recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the required libraries:
   ```bash
   pip install requests python-dotenv
   ```

4. Create a `.env` file in the project directory with the following content:
   ```
   MIST_API_TOKEN=your_api_token
   MIST_ORG_ID=your_organization_id
   ```

### Usage
Run the script using Python 3 (with your virtual environment activated):
```bash
python3 mist_wifi_cloner.py
```

Follow the prompts to select a site, choose a WiFi to clone, and specify the number of clones and their names. If you press Enter when asked for the number of times to clone, the script will default to cloning the WiFi only once.

### Error Handling
- The script includes error handling for API authentication, site and WiFi existence, and network connectivity issues.
- If the script is interrupted, it will display a message indicating the interruption.

### License
This project is licensed under the MIT License - see the LICENSE file for details. 