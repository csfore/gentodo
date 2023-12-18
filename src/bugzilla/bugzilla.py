import requests


BUGZILLA_ROOT = "https://bugs.gentoo.org"

class Bugzilla:

    def __init__(self, token):
        self.token = token
        print("bug zilla initialized")

def main():
    #bugzilla = Bugzilla(TOKEN)
    r = requests.get(BUGZILLA_ROOT + f"/rest/bug?assigned_to=Maintainer Needed?api_key={TOKEN}")
    print(r.text)

main()
