#! python3
# scheduledWebComicDownloader - checks the websites of several web comics and automatically downloads the images if the comic was updated since the program’s last visit.

# Step1: start at 3028 and download until 3033

import requests, os, bs4

os.chdir(os.path.dirname(os.path.abspath(__file__)))

url = 'https://xkcd.com/3028/'                # starting url    

os.makedirs('xkcd', exist_ok=True)            # store comics in ./xkcd

while not url.endswith('#'):
    # Download the page:
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # Find the URL of the comic image:
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        comicUrl = 'https:' + comicElem[0].get('src')
    # Download the image:
        print('Downloading image %s...' % (comicUrl))
        res = requests.get(comicUrl)
        res.raise_for_status()
    # Save the image to ./xkcd:
        imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
    # Get the Next button's url:
    nextLink = soup.select('a[rel="next"]')[0]
    url = 'https://xkcd.com' + nextLink.get('href')

print('Done.')