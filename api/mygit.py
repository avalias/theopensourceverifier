from pydriller import Repository
from pydriller.repository import MalformedUrl
from pydriller.git import Git
import re

url1 = "https://github.com/algorand/smart-contracts/blob/3aa355c91e02830d4d7a15449ac1892eee972047/devrel/crowdfunding/crowd_fund_escrow.teal"
url = "https://github.com/algorand/smart-contracts/blob/master/devrel/crowdfunding/crowd_fund_escrow.teal"
urlRegexp = "^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)\/([^:\/?\n]+)\/([^:\/?\n]+)\/blob\/(?:[^:\/?\n]+)\/([^:?\n]+)"

#use graphql for the smart api access
#https://stackoverflow.com/questions/15831313/is-it-possible-to-get-commits-history-for-one-file-in-github-api
#Create lookup repo file history - give commit names
#And maybe code for couple of 
#Create lookup particular commit - give code
#Create lookup this version - give code, with commit
#Look up latest version, return code, 
#https://stackoverflow.com/questions/20055398/is-it-possible-to-get-commit-logs-messages-of-a-remote-git-repo-without-git-clon
#https://api.github.com/repos/learningequality/ka-lite/git/trees/7b698a988683b161bdcd48a949b01e2b336b4c01

#Try url to urlToRepoAndFilename
def urlToRepoAndFilename(url):
    urlParts = url.split("/")
    fileName = urlParts[-1]
    matches = re.search(urlRegexp, url)
    filePath = matches.group(4)
    domain = matches.group(1)
    company = matches.group(2)
    repo = matches.group(3)
    return (domain, company, repo, filePath, fileName)

def lookUpRepoUrl(url):
    (domain, company, repo, filePath, fileName) = urlToRepoAndFilename(url)
    output = lookUpRepo((domain, company, repo, filePath, fileName))
    return output

def lookUpRepo(info):
    (domain, company, repo, filePath, fileName) = info
    repoUrl = "https://" + domain + "/" + company + "/" + repo
    myRepo = Repository(repoUrl, filepath = filePath)

    fileCommits = myRepo.traverse_commits()
    output = []
    for commit in fileCommits:
        
        print(commit.hash)
        print(commit.msg)
        print(commit.author.name)
        for m in commit.modified_files:    
            if (m.new_path != filePath): continue
            output.append({"commit_hash": commit.hash, "source": m.source_code})
            print(
                "Author {}".format(commit.author.name),
                " modified {} {}".format(m.filename, m.new_path),
                " with a change type of {}".format(m.change_type.name),
                " and the complexity is {}".format(m.complexity)
            )
    return output
#https://github.com/algorand/smart-contracts/blob/master/devrel/crowdfunding/crowd_fund_escrow.teal
# (domain, company, repo, filePath, fileName) = urlToRepoAndFilename("https://github.com/algorand/smart-contracts/blob/master/devrel/crowdfunding/crowd_fund.teal")
# commits, sources = lookUpRepo((domain, company, repo, filePath, fileName))
# print(commits, sources)

#Last commit is the newest one
