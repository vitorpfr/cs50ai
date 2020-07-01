from pagerank import *

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"1.html"}}
# corpus = crawl("corpus0")
page = "3.html"
damping_factor = 0.85

# Transition model test
# result = transition_model(corpus, page, damping_factor)
# print("transition model result:")
# print(result)
# print("sum of prob dist:")
# print(sum(list(result.values())))
# print(list(result))
# print(list(result.values()))

# random value taking distribution
# print(random.choices(list(result), weights=result.values(), k=1)[0])


# Sample pagerank test
print("sample pagerank result:")
print(sample_pagerank(corpus, damping_factor, 100000))
# print(sum(sample_pagerank(corpus, damping_factor, 1).values()))

# Iterate pagerank results
print("iterate pagerank result:")
iterate_result = iterate_pagerank(corpus, damping_factor)
print(iterate_result)
print(sum(iterate_pagerank(corpus, damping_factor).values()))

# Generate list with incoming pages for each page
# incoming_pages = {item: set() for item in list(corpus)}
# for current_page in corpus:
#     for next_page in corpus[current_page]:
#         incoming_pages[next_page].add(current_page)
# print(incoming_pages)