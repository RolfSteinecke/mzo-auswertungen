from git import Repo

PATH_OF_GIT_REPO = r'https://github.com/RolfSteinecke/mzo-auswertungen.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'Neue Logdaten'

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except Exception as e:
        print(f'Some error occured while pushing the code {e}')    

git_push()
