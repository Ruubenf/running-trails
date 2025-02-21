import requests
import os

def get_trails():
    """ Download trail routes from API
    Args:
        None
    Returns:
        None
    """
    # Create the output file
    # API base url
    base_url = "https://trails.rfemenia.com/get_trails.php"
    download_url = "https://trails.rfemenia.com/trails_dir/"

    # Dir where to download kml files
    output_dir = "etl/data/original/"
    os.makedirs(output_dir, exist_ok=True)

    # Get KML file list
    response = requests.get(base_url)
    if response.status_code == 200:
        kml_files = response.json()
        for kml_file in kml_files:
            file_url = download_url + kml_file
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                with open(os.path.join(output_dir, kml_file), "wb") as f:
                    f.write(file_response.content)
                print(f"✅ Downloading: {kml_file}")
            else:
                print(f"❌ Failure to download {kml_file}")
    else:
        print("❌ File list could not be found on the api")