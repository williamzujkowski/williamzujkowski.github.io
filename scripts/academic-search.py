#!/usr/bin/env python3
"""
SCRIPT: academic-search.py
PURPOSE: Academic Search - Use Playwright to search reputable academic sources
CATEGORY: academic_research
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Academic Search - Use Playwright to search reputable academic sources. This script is part of the academic research
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/academic-search.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/academic-search.py

    # With verbose output
    python scripts/academic-search.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in academic_research category]

MANIFEST_REGISTRY: scripts/academic-search.py
"""

import asyncio
import json
import argparse
from pathlib import Path
from playwright.async_api import async_playwright
from typing import List, Dict
from datetime import datetime

class AcademicSearcher:
    def __init__(self):
        self.sources = {
            'arxiv': 'https://arxiv.org/search/',
            'zenodo': 'https://zenodo.org/search',
            'core': 'https://core.ac.uk/search',
            'scholar': 'https://scholar.google.com',
            'semantic': 'https://www.semanticscholar.org/',
            'pubmed': 'https://pubmed.ncbi.nlm.nih.gov/',
            'ieee': 'https://ieeexplore.ieee.org/search/searchresult.jsp',
            'acm': 'https://dl.acm.org/action/doSearch'
        }
        
        self.results = []
    
    async def search_arxiv(self, page, query: str) -> List[Dict]:
        """Search arXiv for papers."""
        results = []
        
        try:
            await page.goto(self.sources['arxiv'])
            await page.wait_for_selector('input[name="query"]', timeout=5000)
            
            # Search
            await page.fill('input[name="query"]', query)
            await page.press('input[name="query"]', 'Enter')
            
            # Wait for results
            await page.wait_for_selector('.arxiv-result', timeout=5000)
            
            # Extract results
            papers = await page.evaluate('''() => {
                const items = document.querySelectorAll('.arxiv-result');
                const results = [];
                for (let i = 0; i < Math.min(items.length, 5); i++) {
                    const titleEl = items[i].querySelector('.title');
                    const abstractEl = items[i].querySelector('.abstract');
                    const authorsEl = items[i].querySelector('.authors');
                    const linkEl = items[i].querySelector('.list-title a');
                    
                    if (titleEl && linkEl) {
                        results.push({
                            title: titleEl.innerText.replace('Title:', '').trim(),
                            url: linkEl.href,
                            abstract: abstractEl ? abstractEl.innerText.substring(0, 200) : '',
                            authors: authorsEl ? authorsEl.innerText : '',
                            source: 'arXiv'
                        });
                    }
                }
                return results;
            }''')
            
            results.extend(papers)
            
        except Exception as e:
            print(f"Error searching arXiv: {e}")
        
        return results
    
    async def search_zenodo(self, page, query: str) -> List[Dict]:
        """Search Zenodo for research outputs."""
        results = []
        
        try:
            search_url = f"{self.sources['zenodo']}?q={query}&sort=bestmatch"
            await page.goto(search_url)
            await page.wait_for_selector('.record-elem', timeout=5000)
            
            # Extract results
            records = await page.evaluate('''() => {
                const items = document.querySelectorAll('.record-elem');
                const results = [];
                for (let i = 0; i < Math.min(items.length, 5); i++) {
                    const titleEl = items[i].querySelector('h4 a');
                    const descEl = items[i].querySelector('.description');
                    const doiEl = items[i].querySelector('.doi');
                    
                    if (titleEl) {
                        results.push({
                            title: titleEl.innerText.trim(),
                            url: titleEl.href,
                            description: descEl ? descEl.innerText.substring(0, 200) : '',
                            doi: doiEl ? doiEl.innerText : '',
                            source: 'Zenodo'
                        });
                    }
                }
                return results;
            }''')
            
            results.extend(records)
            
        except Exception as e:
            print(f"Error searching Zenodo: {e}")
        
        return results
    
    async def search_google_scholar(self, page, query: str) -> List[Dict]:
        """Search Google Scholar for academic papers."""
        results = []
        
        try:
            await page.goto(self.sources['scholar'])
            await page.wait_for_selector('input[name="q"]', timeout=5000)
            
            # Search
            await page.fill('input[name="q"]', query)
            await page.press('input[name="q"]', 'Enter')
            
            # Wait for results
            await page.wait_for_selector('.gs_r', timeout=5000)
            
            # Extract results
            papers = await page.evaluate('''() => {
                const items = document.querySelectorAll('.gs_r');
                const results = [];
                for (let i = 0; i < Math.min(items.length, 5); i++) {
                    const titleEl = items[i].querySelector('h3 a');
                    const snippetEl = items[i].querySelector('.gs_rs');
                    const citedEl = items[i].querySelector('.gs_fl a');
                    
                    if (titleEl) {
                        results.push({
                            title: titleEl.innerText,
                            url: titleEl.href,
                            snippet: snippetEl ? snippetEl.innerText.substring(0, 200) : '',
                            citations: citedEl && citedEl.innerText.includes('Cited by') ? 
                                      citedEl.innerText : '0 citations',
                            source: 'Google Scholar'
                        });
                    }
                }
                return results;
            }''')
            
            results.extend(papers)
            
        except Exception as e:
            print(f"Error searching Google Scholar: {e}")
        
        return results
    
    async def search_core(self, page, query: str) -> List[Dict]:
        """Search CORE for open access papers."""
        results = []
        
        try:
            search_url = f"{self.sources['core']}?q={query}"
            await page.goto(search_url)
            await page.wait_for_selector('.result', timeout=5000)
            
            # Extract results
            papers = await page.evaluate('''() => {
                const items = document.querySelectorAll('.result');
                const results = [];
                for (let i = 0; i < Math.min(items.length, 5); i++) {
                    const titleEl = items[i].querySelector('.title a');
                    const abstractEl = items[i].querySelector('.abstract');
                    const yearEl = items[i].querySelector('.year');
                    
                    if (titleEl) {
                        results.push({
                            title: titleEl.innerText.trim(),
                            url: titleEl.href,
                            abstract: abstractEl ? abstractEl.innerText.substring(0, 200) : '',
                            year: yearEl ? yearEl.innerText : '',
                            source: 'CORE'
                        });
                    }
                }
                return results;
            }''')
            
            results.extend(papers)
            
        except Exception as e:
            print(f"Error searching CORE: {e}")
        
        return results
    
    async def search_all_sources(self, query: str, sources: List[str] = None) -> Dict:
        """Search multiple academic sources for a query."""
        if sources is None:
            sources = ['arxiv', 'scholar', 'zenodo', 'core']
        
        all_results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'sources': {}
        }
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            for source in sources:
                if source not in self.sources:
                    continue
                
                page = await browser.new_page()
                print(f"Searching {source} for: {query}")
                
                if source == 'arxiv':
                    results = await self.search_arxiv(page, query)
                elif source == 'zenodo':
                    results = await self.search_zenodo(page, query)
                elif source == 'scholar':
                    results = await self.search_google_scholar(page, query)
                elif source == 'core':
                    results = await self.search_core(page, query)
                else:
                    results = []
                
                all_results['sources'][source] = results
                await page.close()
                
                # Be respectful to servers
                await asyncio.sleep(2)
            
            await browser.close()
        
        return all_results
    
    def rank_results(self, all_results: Dict) -> List[Dict]:
        """Rank results by relevance and quality."""
        ranked = []
        
        for source, results in all_results['sources'].items():
            for result in results:
                # Basic scoring based on source quality
                score = 0
                if source in ['arxiv', 'zenodo']:
                    score += 10
                elif source == 'scholar':
                    score += 8
                elif source == 'core':
                    score += 7
                
                # Check for citations (if available)
                if 'citations' in result:
                    try:
                        cite_count = int(re.search(r'\d+', result['citations']).group())
                        score += min(cite_count / 10, 10)  # Cap at 10 points
                    except:
                        pass
                
                # Check for DOI
                if 'doi' in result and result['doi']:
                    score += 5
                
                result['relevance_score'] = score
                ranked.append(result)
        
        # Sort by score
        ranked.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return ranked[:10]  # Top 10 results
    
    def format_citations(self, results: List[Dict]) -> List[str]:
        """Format results as proper citations."""
        citations = []
        
        for result in results:
            # Basic citation format
            title = result.get('title', 'Unknown Title')
            url = result.get('url', '')
            source = result.get('source', '')
            year = result.get('year', datetime.now().year)
            authors = result.get('authors', 'Unknown Authors')
            
            if 'doi' in result and result['doi']:
                citation = f"{authors} ({year}). {title}. {source}. DOI: {result['doi']}"
            else:
                citation = f"{authors} ({year}). {title}. {source}. Available at: {url}"
            
            citations.append(citation)
        
        return citations

async def main():
    parser = argparse.ArgumentParser(description='Search academic sources for research')
    parser.add_argument('--query', required=True, help='Search query')
    parser.add_argument('--sources', default='arxiv,scholar,zenodo,core', 
                       help='Comma-separated list of sources')
    parser.add_argument('--output', help='Output file for results')
    parser.add_argument('--format', choices=['json', 'citations'], default='json',
                       help='Output format')
    
    args = parser.parse_args()
    
    searcher = AcademicSearcher()
    sources = args.sources.split(',')
    
    # Search all sources
    results = await searcher.search_all_sources(args.query, sources)
    
    # Rank results
    ranked = searcher.rank_results(results)
    
    # Output results
    if args.format == 'citations':
        citations = searcher.format_citations(ranked)
        for i, citation in enumerate(citations, 1):
            print(f"[{i}] {citation}")
    else:
        print(json.dumps({
            'query': args.query,
            'top_results': ranked,
            'total_found': sum(len(r) for r in results['sources'].values())
        }, indent=2))
    
    # Save to file if specified
    if args.output:
        with open(args.output, 'w') as f:
            if args.format == 'citations':
                f.write('\n'.join(searcher.format_citations(ranked)))
            else:
                json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

if __name__ == "__main__":
    import re
    asyncio.run(main())