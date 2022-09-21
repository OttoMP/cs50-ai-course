from copy import deepcopy
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    out_links = corpus[page]
    probability_distribution = dict()
    for i in out_links:
        probability_distribution[i] = damping_factor/len(out_links)
    for p in corpus:
        probability_distribution[p] = probability_distribution.get(p, 0) + (1-damping_factor)/len(corpus)

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    for key in corpus.keys():
        page_rank[key] = 0

    page = random.choice(list(corpus.keys()))
    for _ in range(n):
        tm = transition_model(corpus, page, damping_factor)
        weights = []
        population = []
        for key, value in tm.items():
            weights.append(value)
            population.append(key)
        page = random.choices(population, weights=weights)[0]
        page_rank[page] = page_rank.get(page, 0) + 1


def links(corpus, page):
    links = []
    for key, value in corpus.items():
        if page in value:
            links.append(key)
    return links


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    for key in corpus.keys():
        page_rank[key] = 1/len(corpus)

    changed = True
    it = 0
    while changed:
        changed = False
        it += 1
        update = deepcopy(page_rank)
        for p in update.keys():
            links = links(corpus, p)
            update[p] = (1-damping_factor)/len(corpus) + damping_factor*(sum([page_rank[link]/len(corpus[link]) for link in links]))
            if abs(update[p]-page_rank[p]) >= 0.001:
                changed = True
        page_rank = update


if __name__ == "__main__":
    main()
