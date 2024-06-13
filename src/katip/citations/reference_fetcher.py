import api_keys
import requests
import json
import re
import time
import threading

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

@retry(wait=wait_random_exponential(min=1, max=60))
def fetch_papers_semantic_scholar(query, max_results=3):
    # URL for Semantic Scholar API
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    
    # Parameters for the API call
    params = {
        'query': query,
        'limit': max_results
    }

    #provide api_key
    headers = {
        'x-api-key': api_keys.ss_api_key
    }
    
    # Send request to Semantic Scholar API
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch data from Semantic Scholar.")
        print(f"Status code: {response.status_code}")
        #sleep for 1 second and try again
        raise Exception("Failed to fetch data from Semantic Scholar.") 
    
    # Parse the JSON response
    data = response.json()
    
    # Extract and print paper titles and URLs
    papers = []
    if 'data' in data:
        for item in data['data']:
            paper_id = item['paperId']
            title = item['title']
            url = f"https://www.semanticscholar.org/paper/{paper_id}"
            papers.append((title, url))
    
    return papers

def add_to_map(papers_map, query, max_results=3):
    papers = fetch_papers_semantic_scholar(query, max_results)
    papers_map[query] = papers

def fetch_papers_map_semantic_scholar(queries, max_results=3):
    # asynchroneously fetch papers for each query with threading
    papers_map = {}
    threads = []
    for query in queries:
        thread = threading.Thread(target=add_to_map, args=(papers_map, query, max_results))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    return papers_map

def find_references_in_document_dict(document_dict):
    # first convert document dict to json and then find the syntax ((citation_needed: ...)) and ((result_needed: ...))
    # for each match, query with ... part and replace the ... part with the fetched paper title and url

    # convert document_dict to json
    document_json = json.dumps(document_dict)
    matches = re.findall(r'\(citation_needed:.*?\)', document_json)
    queries = [match[18:-1] for match in matches]
    matches = re.findall(r'\(result_needed:.*?\)', document_json)
    queries += [match[16:-1] for match in matches]
    
    papers_map = fetch_papers_map_semantic_scholar(queries)
    
    # find the syntax ((citation_needed: ...)) and ((result_needed: ...))
    prefix = '((citation_needed: '
    i = document_json.find(prefix)
    while i != -1:
        j = document_json.find(')', i)
        query = document_json[i+len(prefix):j]
        papers = papers_map[query]
        str_papers = f"((citation: "

        if len(papers) == 0:
            str_papers += query + ', '

        for title, url in papers:
            # remove any non alphanumeric characters from title
            title = re.sub(r'\W+', ' ', title)
            str_papers += f"[{title}]({url}), "
        str_papers = str_papers[:-2] + ')'

        document_json = document_json[:i] + str_papers + document_json[j+1:]
        i = document_json.find(prefix)

    prefix = '((result_needed: '
    i = document_json.find(prefix)
    while i != -1:
        j = document_json.find(')', i)
        query = document_json[i+len(prefix):j]
        papers = papers_map[query]
        str_papers = f"((result: "

        if len(papers) == 0:
            str_papers += query + ', '

        for title, url in papers:
            # remove any non alphanumeric characters from title
            title = re.sub(r'\W+', ' ', title)
            str_papers += f"[{title}]({url}), "
        str_papers = str_papers[:-2] + ')'

        document_json = document_json[:i] + str_papers + document_json[j+1:]
        i = document_json.find(prefix)

    converted_document_dict = json.loads(document_json)
    return converted_document_dict
