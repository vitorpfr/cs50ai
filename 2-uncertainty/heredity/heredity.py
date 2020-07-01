import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    # set empty dict to store probabilities
    probabilities = {}

    # set empty dict to store genes for each person
    genes = {}
    for person in list(people):
        if person in one_gene:
            genes[person] = 1
        elif person in two_genes:
            genes[person] = 2
        else:
            genes[person] = 0

    # iterate for each person in the list to calculate probability
    for person in list(people):
        # store initial vals to infer probabilities
        # store person gene
        gene = genes[person]

        # store person trait
        trait = person in have_trait

        # store person parents
        mother = people[person]["mother"]
        father = people[person]["father"]

        # if person has no parents
        if (mother == None) and (father == None):
            # add probability associated to person
            probabilities[person] = PROBS["gene"][gene] * PROBS["trait"][gene][trait]
        
        # else, if person has parents
        else:
            # set mother and father genes
            mother_gene = genes[mother]
            father_gene = genes[father]

            # define the chance of passing normal or mutated genes based on how many mutated genes the parent have (index of array)
            mutation = PROBS["mutation"]
            chance_of_passing_normal_gene = [(1 - mutation), 0.5, mutation]
            chance_of_passing_mutated_gene = [mutation, 0.5, (1 - mutation)]

            # disclaimer: the chance of a person with one copy of the mutated gene passing it is still 0.5 (even considering additional mutation),
            # because either the mutated gene and the non-mutated gene can undergo additional mutation
            # and therefore the mutation value cancels out
            # P(pass mutation) = P(select original mutated and not mutation) + P(select original normal and mutation)
            # P(pass mutation) = 0.5 * (1 - mutation) + 0.5 * (mutation)
            # P(pass mutation) = 0.5

            # 2 genes passed: person must get mutated genes from both mother and father
            if gene == 2: 
                prob_gene = chance_of_passing_mutated_gene[mother_gene] * chance_of_passing_mutated_gene[father_gene]

            # 1 gene passed: person must get from mother or father, but not both
            elif gene == 1: 
                # possibility one: mother passes normal gene and father passes mutated gene
                prob_gene_mutated_father = chance_of_passing_normal_gene[mother_gene] * chance_of_passing_mutated_gene[father_gene]

                # possibility two: mother passes mutated gene and father passes normal gene
                prob_gene_mutated_mother = chance_of_passing_mutated_gene[mother_gene] * chance_of_passing_normal_gene[father_gene]

                # sum both possibilities
                prob_gene = prob_gene_mutated_father + prob_gene_mutated_mother

             # 0 genes passed: person must get normal gene from both mother and father
            else:  
                prob_gene = chance_of_passing_normal_gene[mother_gene] * chance_of_passing_normal_gene[father_gene]
            
            # add probability associated to person
            probabilities[person] = prob_gene * PROBS["trait"][gene][trait]

    # multiply all probabilities (and) to get to final result
    final_probability = 1
    for probability in list(probabilities.values()):
        final_probability = final_probability * probability

    return final_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # set empty dict to store genes for each person
    genes = {}
    for person in list(probabilities):
        if person in one_gene:
            genes[person] = 1
        elif person in two_genes:
            genes[person] = 2
        else:
            genes[person] = 0

    # iterate for each person in the list to update probabilities
    for person in list(probabilities):
        # store person gene
        gene = genes[person]

        # store person trait
        trait = person in have_trait

        # update relevant probabilities for this person
        probabilities[person]["gene"][gene] += p
        probabilities[person]["trait"][trait] += p
 

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in list(probabilities):
        # calculating gene sum for this person
        gene_sum = sum(list(probabilities[person]["gene"].values()))

        # normalizing gene
        for gene, value in probabilities[person]["gene"].items():
            probabilities[person]["gene"][gene] = value / gene_sum
        
        # calculating trait sum for this person
        trait_sum = sum(list(probabilities[person]["trait"].values()))

        # normalizing trait
        for trait, value in probabilities[person]["trait"].items():
            probabilities[person]["trait"][trait] = value / trait_sum


if __name__ == "__main__":
    main()
