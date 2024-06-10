import api_keys
import requests
import json
import re
import time

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
        time.sleep(1)
        return fetch_papers_semantic_scholar(query, max_results)
    
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

def find_references_in_document_dict(document_dict):
    # first convert document dict to json and then find the syntax ((citation_needed: ...)) and ((result_needed: ...))
    # for each match, query with ... part and replace the ... part with the fetched paper title and url

    # convert document_dict to json
    document_json = json.dumps(document_dict)
    
    # find the syntax ((citation_needed: ...)) and ((result_needed: ...))
    prefix = '((citation_needed: '
    i = document_json.find(prefix)
    while i != -1:
        j = document_json.find(')', i)
        query = document_json[i+len(prefix):j]
        papers = fetch_papers_semantic_scholar(query)
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
        papers = fetch_papers_semantic_scholar(query)
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
