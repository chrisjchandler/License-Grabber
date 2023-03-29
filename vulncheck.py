import requests

def read_libraries_from_file(file_path):
    with open(file_path, 'r') as file:
        libraries = [line.strip() for line in file.readlines()]
    return libraries

def get_cves_for_libraries(libraries):
    nvd_api_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    cves = []

    for library in libraries:
        params = {
            "keyword": f"python {library}",
            "resultsPerPage": 100,  # You can modify this to retrieve more results per request
        }
        response = requests.get(nvd_api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            cves.extend(data["result"]["CVE_Items"])

    return cves

file_path = "requirements_no_versions.txt"
libraries = read_libraries_from_file(file_path)
cves = get_cves_for_libraries(libraries)

for cve in cves:
    print(f"{cve['cve']['CVE_data_meta']['ID']}: {cve['cve']['description']['description_data'][0]['value']}")
