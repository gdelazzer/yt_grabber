import re
import requests
from bs4 import BeautifulSoup
from pytube import YouTube

payload = {
    "email": "",
    "password": ""
}
course_url = ""
domain = ""

def getSoup(session, url):
    result = session_requests.get(
        url,
        headers = dict(referer = url)
    )
    soup = BeautifulSoup(result.content, 'html.parser')

    return soup

if __name__ == "__main__":
    session_requests = requests.session()
    login_url = "https://{0}/login".format(domain)
    result = session_requests.get(login_url)
    result = session_requests.post(
        login_url,
        data=payload,
        headers = dict(referer=login_url)
    )
    soup = getSoup(session_requests, course_url)

    print("- {0}".format(soup.title.string.strip()))
    xmodules = soup.select(".course-component-module-title a[href]")

    modules = {}
    module_nb = 0
    for i in xmodules:
        module_nb += 1
        soup = getSoup(session_requests, "https://{0}{1}".format(domain, i["href"]))
        print("  - {0}".format(soup.title.string.strip()))

        classes = soup.select("ul li a")
        for j in classes:
            soup = getSoup(session_requests, "https://courses.{0}{1}".format(domain, j["href"]))
            youtube_ids = re.findall('\"1\.00\:(.+?)\"', str(soup))

            print("    - {0}".format(soup.title.string.strip()))
            for yt_id in youtube_ids:
                yt_url = "https://www.youtube.com/watch?v={0}".format(yt_id)
                print("      -> Downloading {0}".format(yt_url))
                yt = YouTube(yt_url)
                yt.streams\
                    .filter(progressive=True)\
                    .order_by("resolution")\
                    .desc()\
                    .first()\
                    .download()
