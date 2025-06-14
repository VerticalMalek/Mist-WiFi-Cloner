import os
import requests
from dotenv import load_dotenv
import json
from typing import Dict, List, Optional

class MistWifiCloner:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv('MIST_API_TOKEN')
        self.org_id = os.getenv('MIST_ORG_ID')
        self.base_url = "https://api.eu.mist.com/api/v1"
        
        if not self.api_token or not self.org_id:
            raise ValueError("API token and organization ID must be set in .env file")

    def get_headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Token {self.api_token}',
            'Content-Type': 'application/json'
        }

    def get_sites(self) -> List[Dict]:
        """Get list of all sites in the organization"""
        try:
            url = f"{self.base_url}/orgs/{self.org_id}/sites"
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                raise Exception("Authentication failed. Please check your API token.")
            elif response.status_code == 404:
                raise Exception("Organization not found. Please check your organization ID.")
            else:
                raise Exception(f"Failed to get sites: {str(e)}")

    def get_wifi_list(self, site_id: str) -> List[Dict]:
        """Get list of all WiFis in the specified site"""
        try:
            url = f"{self.base_url}/sites/{site_id}/wlans"
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                raise Exception("Authentication failed. Please check your API token.")
            elif response.status_code == 404:
                raise Exception("Site not found. Please check your site ID.")
            else:
                raise Exception(f"Failed to get WiFi list: {str(e)}")

    def clone_wifi(self, site_id: str, source_wifi_id: str, new_name: str) -> Dict:
        """Clone an existing WiFi configuration with a new name"""
        try:
            # First get the source WiFi configuration
            url = f"{self.base_url}/sites/{site_id}/wlans/{source_wifi_id}"
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            wifi_config = response.json()

            # Modify the configuration for the new WiFi
            wifi_config['ssid'] = new_name
            wifi_config.pop('id', None)

            # Create the new WiFi
            url = f"{self.base_url}/sites/{site_id}/wlans"
            response = requests.post(url, headers=self.get_headers(), json=wifi_config)
            response.raise_for_status()
            result = response.json()
            return result
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                raise Exception("Authentication failed. Please check your API token.")
            elif response.status_code == 404:
                raise Exception("WiFi or site not found. Please check your WiFi ID and site ID.")
            else:
                raise Exception(f"Failed to clone WiFi: {str(e)}")

def main():
    try:
        print("Initializing Mist WiFi Cloner...")
        cloner = MistWifiCloner()
        
        print("\nFetching list of available sites...")
        sites = cloner.get_sites()
        
        if not sites:
            print("No sites found in your organization.")
            return
            
        print("\nAvailable Sites:")
        sites.sort(key=lambda x: x['name'])  # Sort sites by name
        for i, site in enumerate(sites, 1):
            print(f"{i}. Name: {site['name']}")

        site_choice = int(input("\nEnter the number of the site you want to work with: "))
        if site_choice < 1 or site_choice > len(sites):
            raise ValueError("Invalid site number.")
        site_id = sites[site_choice - 1]['id']
        
        print("\nFetching list of available WiFis...")
        wifis = cloner.get_wifi_list(site_id)
        
        if not wifis:
            print("No WiFis found in the selected site.")
            return
            
        print("\nAvailable WiFis:")
        wifis.sort(key=lambda x: x['ssid'])  # Sort WiFis by SSID
        for i, wifi in enumerate(wifis, 1):
            vlan_id = wifi.get('vlan_id', 'N/A')
            print(f"{i}. SSID: {wifi['ssid']}, VLAN ID: {vlan_id}")

        wifi_choice = int(input("\nEnter the number of the WiFi you want to clone: "))
        if wifi_choice < 1 or wifi_choice > len(wifis):
            raise ValueError("Invalid WiFi number.")
        source_wifi_id = wifis[wifi_choice - 1]['id']

        num_clones_input = input("Enter the number of times you want to clone the WiFi (press Enter for 1): ")
        num_clones = int(num_clones_input) if num_clones_input.strip() else 1
        for i in range(num_clones):
            new_name = input(f"Enter the name for clone {i+1} (or press Enter to use the original name): ")
            if not new_name:
                new_name = wifis[wifi_choice - 1]['ssid']  # Use the original SSID if no new name is provided
            print(f"\nCloning WiFi {i+1}...")
            result = cloner.clone_wifi(site_id, source_wifi_id, new_name)
            print(f"\nSuccessfully cloned WiFi {i+1}!")
            print(f"New WiFi ID: {result['id']}")
            print(f"New WiFi SSID: {result['ssid']}")

    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        return
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease check:")
        print("1. Your API token is correct and has proper permissions")
        print("2. Your organization ID is correct")
        print("3. You have network connectivity to Mist API")
        print("4. The site ID and WiFi ID you entered exist in your organization")

if __name__ == "__main__":
    main() 