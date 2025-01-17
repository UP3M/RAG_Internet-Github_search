import requests
from .tokens_keys import headers
from .repo_utils import match_repository
from .repo_utils import rank_repositories
from chains import search_question_chain
from .generate_keywords import generate_keywords

def search_github(keyword: list) -> dict:
  """
  Searches github database based on keywords

  Parameters:
  -----------
  keyword: the list of keywords

  Returns:
  ----------
  dict: json format reponse
  """

  # Prefix github url for retrieval
  url = f"https://api.github.com/search/repositories?q={keyword}"

  response = requests.get(url, headers=headers)
  if response.status_code == 200:
      return response.json()
  else:
      print(f"Error: {response.status_code}")
      return None


def find_repo(keywords: list) -> str:
  """
  Find repos (<1000) by similarity

  Parameters:
  -----------
  keywords: The list of keywords

  Returns:
  -----------
  str: top 5 list of repos based on similarity rank
  """

  repositories = []
  for keyword in keywords:
    results = search_github(keyword)
    itr = 0
    if results:
      for item in results["items"]:
       if itr < 1000:
        repo_url = item["html_url"]
        similarity = match_repository(gigatext, repo_url)
        repositories.append({"html_url": repo_url, "similarity": similarity})
        itr += 1
      else: break
  
  joined_repo = "\n*".join(rank_repositories(repositories))
  ranked_repos = gigatext + "\n\nGitHub repos \n-------------- \n" + "*" + joined_repo
  return ranked_repos


# Store the report content in gigatext
gigatext = ""

def retrive_repos(gigachain_text: str) -> str:
  """
  Retrieves repos, and saves the report from the crawl, to append later with github links

  Parameters:
  -----------
  gigachain_text: the report content generated by gigachat using the crawl

  Returns:
  -----------
  results: The final results combined with gigachat generated report, reference, and github link
  """

  global gigatext
  gigatext = gigachain_text

  # Generate keywords from keywords, and find the repos
  results = search_question_chain | generate_keywords | find_repo
  return results