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
    prob_dist = {}
    n_corpus = len(corpus)
    n_links = len(corpus[page])

    # prob of choosing all pages
    for p in corpus:
        prob_dist[p] = (1 - damping_factor) / n_corpus

    # prob of choosing linked pages
    if n_links > 0:
        for p in corpus[page]:
            prob_dist[p] += damping_factor / n_links

    # no linked pages
    else:
        for p in corpus:
            prob_dist[p] += damping_factor / n_corpus

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample = None
    sample_count = {}

    for i in range(n):
        # for 1st iter
        if not sample:
            sample = random.choice(list(corpus.keys()))

        # for subsequent iters
        else:
            next_prob = transition_model(corpus, sample, damping_factor)
            sample = random.choices(list(next_prob.keys()), list(next_prob.values()))[0]

        # count sample
        sample_count[sample] = sample_count.get(sample, 0) + 1

    pagerank = {page: count / n for (page, count) in sample_count.items()}

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    def sum_incoming_links(current_page):
        sum = 0

        # find pages that link to current_page
        for page in corpus:
            if current_page in corpus[page]:
                sum += pagerank_prev[page] / len(corpus[page])

        return sum

    # make pages with no links to have links to every page
    for page in corpus:
        if len(corpus[page]) < 1:
            corpus[page] = set(corpus.keys())

    # init variables
    threshold = 0.001
    d = damping_factor
    n = len(corpus)
    pagerank = dict.fromkeys(corpus.keys(), 1/n)

    while True:
        pagerank_prev = pagerank.copy()

        # iterate all pages with formula
        for p in corpus:
            pagerank[p] = ((1 - d)/n) + (d * sum_incoming_links(p))

        # check if page rank for each page satisfies threshold
        changes = [abs(curr - prev) for (curr, prev) in zip(list(pagerank.values()), list(pagerank_prev.values()))]
        converged = [change <= threshold for change in changes]

        # terminate if all pages have converged
        if all(converged):
            break

    return pagerank


if __name__ == "__main__":
    main()
