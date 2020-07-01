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

    # Initiate an empty dict to store the probability distribution for each page
    probability_dist = {}

    # Iterate through all potentail next pages in the corpus
    for next_page in list(corpus):
        # Initiate probability of going from page to next_page at 0
        probability = 0

        # Check if it is possible to go directly from page to next_page
        # If yes, add the odds to probability corrected by damping_factor
        if next_page in list(corpus[page]):
            probability += (damping_factor / len(list(corpus[page])))
        
        # Add the probability to be selected at random for all pages, corrected by (1 - damping_factor)
        # if the page has any outgoing links (which compound the probability with damping_factor)
        if len(corpus[page]) == 0:
            probability += (1 / len(list(corpus)))
        else:
            probability += ((1-damping_factor) / len(list(corpus)))

        # Assign probability of going to next_page to it in the dict
        probability_dist[next_page] = probability

    # Return result once calculations are made
    return probability_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create dict to store sample results
    sample_result = {item: 0 for item in list(corpus)}

    # Initialize variable to start iteration in a random page
    current_page = random.sample(list(corpus), k=1)[0]
    
    # Iterate n times
    for i in range(n):
        # Calculate the probability distribution of current page using transition model
        probability_dist = transition_model(corpus, current_page, damping_factor)

        # Select the next page as current, using probability distribution as weights
        current_page = random.choices(list(probability_dist), weights=probability_dist.values(), k=1)[0]

        # Add next page selected as current to sample count
        sample_result[current_page] += 1
    
    # Divide sample sizes by n to get estimated PageRank and return as result
    return {page: sample_value/n for page, sample_value in sample_result.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize pagerank and pagerank_temp with equal probability for each page
    pagerank = {item: 1/len(list(corpus)) for item in list(corpus)}

    # Define parameters to be used in the iteration
    list_of_pages = list(pagerank)
    number_of_pages = len(list_of_pages)
    accuracy = 0.001

    # Start infinite loop
    while True:
        # Initialize array to store the difference in pageranks between current value and next value
        change_in_pageranks = []

        # Recalculate pagerank for each page
        for page in list_of_pages:
            # Store current value of pagerank
            previous_pagerank = pagerank[page]

            # Calculate the random part of pagerank probability
            random_probability = 1 / number_of_pages

            # Calculate the non-random part (by clicking in a link) of pagerank probability
            # Initialize following_link_probability as 0 (it will be a sum)
            following_link_probability = 0

            # Loop through potential incoming pages
            for incoming_page in list_of_pages:
                # If potential incoming page has no links, override corpus and assume it as having links to all pages including itself
                if len(corpus[incoming_page]) == 0:
                    links_of_incoming_page = list_of_pages

                # Otherwise, use corpus to get links of incoming page
                else:
                    links_of_incoming_page = corpus[incoming_page]
                
                # Check if incoming page has a link to current page: if yes, add it to sum
                if page in links_of_incoming_page:
                    following_link_probability += (pagerank[incoming_page] / len(links_of_incoming_page))

            # Set the sum as the new page rank and store the difference in array
            pagerank[page] = ((1 - damping_factor) * random_probability) + (damping_factor * following_link_probability)
            change_in_pageranks.append(abs(pagerank[page] - previous_pagerank))

        # Check if the new values match condition (all differences lower than 0.001) - if yes, break loop and return result
        if all([i < accuracy for i in change_in_pageranks]):
            return pagerank
    

if __name__ == "__main__":
    main()
