from django.shortcuts import render
from .models import Paper
import requests
import json
from bs4 import BeautifulSoup
from metaphor_python import Metaphor

def search_view(request):
    papers = []
    if request.method == 'POST':
        subject = request.POST.get('subject')
        num_results = int(request.POST.get('num_results', 1))
        papers = fetch_and_summarize(subject, num_results)
        
    return render(request, 'search.html', {'papers': papers})

def fetch_and_summarize(subject, num_results):
    METAPHOR_API_KEY = "cec7fdd4-e520-47d5-b19b-b6ac9fc2c6e9"
    subject = subject
    num_results = num_results if num_results<=5 else 5

    metaphor = Metaphor(METAPHOR_API_KEY)

    search_response = metaphor.search(
        subject,
        num_results=num_results,
        use_autoprompt=True,
    )

    papers_data = search_response.results
    paper_ids = [paper.id for paper in papers_data]

    contents_response = metaphor.get_contents(paper_ids)

    contents_data = contents_response.contents

    summarized_papers = []
    for content in contents_data:
        clean_text = clean_html(content.extract)
        summary = text_summerization(clean_text) # use hugging face's bart-large-cum as LLM for text summarization

        summarized_papers.append({
            "id": content.id,
            "title": content.title,
            "link": content.url,
            "summary": summary
        })

    return summarized_papers

def text_summerization(input_str):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": input_str,
    })

    return ". ".join(i['summary_text'] for i in output)

def clean_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    
    cleaned_text = soup.get_text()
    cleaned_text = ' '.join(cleaned_text.split())

    return cleaned_text