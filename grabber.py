import requests
import json
import base64
import time

GITHUB_TOKEN = 'your_token_here'

headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'token {GITHUB_TOKEN}'
}

def get_github_repo(package_name):
    url = f'https://pypi.org/pypi/{package_name}/json'
    response = requests.get(url)

    if response.status_code == 200:
        package_info = response.json()
        repo_url = package_info['info'].get('home_page', None)
        if repo_url and 'github.com' in repo_url:
            return repo_url
    return ''

def get_license_text(repo_url):
    repo_info = repo_url.split('github.com/')[-1]
    api_url = f'https://api.github.com/repos/{repo_info}/license'
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        license_data = response.json()
        license_content_base64 = license_data['content']
        license_content = base64.b64decode(license_content_base64).decode('utf-8')
        return license_content
    else:
        return 'License Not Found'

def main():
    input_file = 'requirements_no_versions.txt'
    output_file = 'licenses.txt'
    delay_seconds = 2

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        packages = [package.strip() for package in infile]
        total_packages = len(packages)

        for index, package_name in enumerate(packages):
            print(f'Processing package {index + 1} of {total_packages}: {package_name}')

            repo_url = get_github_repo(package_name)

            if repo_url:
                license_text = get_license_text(repo_url)
                outfile.write(f'{package_name} License:\n{license_text}\n\n')
                print(f'{package_name}: License found')
            else:
                outfile.write(f'{package_name}: License Not Found\n\n')
                print(f'{package_name}: License Not Found')

            # Add a delay to prevent rate limiting issues
            if index < total_packages - 1:
                time.sleep(delay_seconds)

if __name__ == '__main__':
    main()

