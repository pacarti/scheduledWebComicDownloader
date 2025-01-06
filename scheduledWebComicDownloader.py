#! python3
# scheduledWebComicDownloader.py - checks the websites of several web comics and automatically downloads the images if the comic was updated since the program’s last visit.


import requests, os, bs4, threading
from pathlib import Path

def downloadXkcdComics():

    latestComicIDFileP = Path('latestXkcdComicID.txt')

    if latestComicIDFileP.is_file():
        latestComicIDFile = open('latestXkcdComicID.txt')
        latestComicID = latestComicIDFile.read()

        url = 'https://xkcd.com/' + latestComicID     # starting url

        # Download the page:
        print('Downloading page %s...' % url)
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        nextLinkHref = soup.select('a[rel="next"]')[0].get('href')

        if nextLinkHref == '#':
            print("No new XKCD comics since last download. Exiting...")
            return 0
    else:
        # No file detected - never downloaded so downloading from the 1st comic
        url = 'https://xkcd.com/1/'

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
        currentUrl = url
        url = 'https://xkcd.com' + nextLink.get('href')
        # Last link is: ''https://xkcd.com#''

    # e.g. url = https://xkcd.com/3033/#
    # Remove '/' from the link to save the latest comic ID:
    currentUrl = currentUrl[:-1]

    latestComicID = os.path.basename(currentUrl)



    latestComicIDFile = open('latestXkcdComicID.txt', 'w')
    latestComicIDFile.write(latestComicID)
    latestComicIDFile.close()

def downloadQwantzComics():

    latestQwantzComicIDFileP = Path('latestQwantzComicID.txt')

    if latestQwantzComicIDFileP.is_file():
        latestQwantzComicIDFile = open('latestQwantzComicID.txt')
        latestQwantzComicID = latestQwantzComicIDFile.read()

        url = 'https://qwantz.com/index.php?comic=' + latestQwantzComicID     # starting url

        # Download the page:
        print('Downloading page %s...' % url)
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        try:
            nextLinkHref = soup.select('a[rel="next"]')[0].get('href')
        except IndexError:
            print("No new Qwantz comics since last download. Exiting...")
            exit()

    else:
        # No file detected - never downloaded so downloading from the 1st comic
        url = 'https://qwantz.com/index.php?comic=1'

    os.makedirs('qwantz', exist_ok=True)            # store comics in ./xkcd

    while True:
        # Download the page:
        print('Downloading page %s...' % url)
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        # Find the URL of the comic image:
        comicElem = soup.select('img.comic')
        if comicElem == []:
            print('Could not find comic image.')
        else:
            comicUrl = 'https://www.qwantz.com/' + comicElem[0].get('src')
        # Download the image:
            print('Downloading image %s...' % (comicUrl))
            res = requests.get(comicUrl)
            res.raise_for_status()
        # Save the image to ./xkcd:
            imageFile = open(os.path.join('qwantz', os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
        # Get the Next button's url:
        try:
            nextLink = soup.select('a[rel="next"]')[0]
            url = 'https://qwantz.com/' + nextLink.get('href')
        except IndexError:
            currentUrl = url
            break


    # Strip the link to get latest comic ID:
    latestComicID = currentUrl.strip('https://qwantz.com/index.php?comic=')


    latestComicIDFile = open('latestQwantzComicID.txt', 'w')
    latestComicIDFile.write(latestComicID)
    latestComicIDFile.close()

def main():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    threadXkcd = threading.Thread(target=downloadXkcdComics)
    threadQwantz = threading.Thread(target=downloadQwantzComics)

    threadXkcd.start()
    threadQwantz.start()

if __name__ == "__main__":
    main()

print('Done.')