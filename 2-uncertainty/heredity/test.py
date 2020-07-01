from heredity import *

# Joint probability
people = {"Harry": {"mother": "Lily",
                    "father": "James"},
          "James": {"mother": None,
                    "father": None},
          "Lily":  {"mother": None,
                    "father": None}}
one_gene = {"Harry"}
two_genes = {"James"}
have_trait = {"James"}

result = joint_probability(people, one_gene, two_genes, have_trait)
print(result)

# Normalize
# probabilities = {
#         "Harry": {
#             "gene": {
#                 2: 0.1,
#                 1: 0.1,
#                 0: 0.1
#             },
#             "trait": {
#                 True: 0.2,
#                 False: 0.3
#             }
#         },
#         "James": {
#             "gene": {
#                 2: 0.2,
#                 1: 0.2,
#                 0: 0.2
#             },
#             "trait": {
#                 True: 0.1,
#                 False: 0.1
#             }
#         }
#     }

# print("before")
# print(probabilities)
# result = normalize(probabilities)
# print("after")
# print(probabilities)