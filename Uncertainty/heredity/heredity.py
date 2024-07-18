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
    probability = 1.0

    for person in people:
        mother = people[person]["mother"]
        father = people[person]["father"]
        
        if person in have_trait:
            has_trait = True
        else:
            has_trait = False

        # Determine the gene count for the current person
        if person in two_genes:
            gene_count = 2
        elif person in one_gene:
            gene_count = 1
        else:
            gene_count = 0

        if mother is None and father is None:
            # Person is a founder, use unconditional probability
            gene_prob = PROBS["gene"][gene_count]
        else:
            # Person is not a founder, calculate based on parents
            if mother in two_genes:
                mother_prob = 1 - PROBS["mutation"]
            elif mother in one_gene:
                mother_prob = 0.5
            else:
                mother_prob = PROBS["mutation"]

            if father in two_genes:
                father_prob = 1 - PROBS["mutation"]
            elif father in one_gene:
                father_prob = 0.5
            else:
                father_prob = PROBS["mutation"]
            
            if gene_count == 2:
                # If person has two genes, both parents must pass a gene
                gene_prob = mother_prob * father_prob
            elif gene_count == 1:
                # If person has one gene, one parent must pass a gene and the other must not
                gene_prob = mother_prob * (1 - father_prob) + (1 - mother_prob) * father_prob
            else:
                # If person has no gene, both parents must not pass a gene
                gene_prob = (1 - mother_prob) * (1 - father_prob)

        # Determine the trait probability for the current person
        trait_prob = PROBS["trait"][gene_count][has_trait]
        
        # Multiply the gene and trait probabilities to get the joint probability
        probability *= gene_prob * trait_prob
        
        if person == "Harry":  # Add a debug statement for Harry
            print(f"Harry - Gene Count: {gene_count}, Gene Prob: {gene_prob}, Trait Prob: {trait_prob}, Combined Prob: {probability}")


    return probability
    
    
    
    

    # # Create a dict for the total probability
    # # Split into gene and trait
    # joint_prob = {}
    # sum_join_prob = 0
    # for person in people:
    #     joint_prob[person] = {
    #         "gene": 0,
    #         "trait": 0
    #     }

    # for person in people:
    #     gene_prob = 1
    #     trait_prob = 1

    #     mother = people[person]["mother"]
    #     father = people[person]["father"]
    #     gene_count = 1 if person in one_gene else 2 if person in two_genes else 0
    #     trait = True if person in have_trait else False

    #     # Everyone in set `one_gene` has one copy of the gene, and
    #     # everyone in set `two_genes` has two copies of the gene, and
    #     # everyone not in `one_gene` or `two_gene` does not have the gene
    #     gene_prob *= PROBS["gene"][gene_count]

    #     if trait is not None:
    #         trait_prob *= PROBS["trait"][gene_count][trait]

    #     # For anyone with no parents listed in the data set,
    #     if mother is None and father is None:
    #         gene_prob *= PROBS["gene"][gene_count]
    #         trait_prob *= PROBS["trait"][gene_count][trait]

    #     # For anyone with parents in the data set
    #     else:
    #         #loop through the parents
    #         for (mother, father) in people:
    #             if mother in two_genes and father in two_genes:
    #                 gene_prob *= 1 - PROBS["mutation"]
    #             elif mother in two_genes or father in two_genes:
    #                 gene_prob *= 0.5
    #             else:
    #                 gene_prob *= PROBS["mutation"]

    #     joint_prob[person] = {
    #         "gene": gene_prob,
    #         "trait": trait_prob
    #     }

    #     sum_join_prob += gene_prob * trait_prob

    # return sum_join_prob
        # # Update total probability based on gene count
        # joint_prob[person]["gene"] += PROBS["gene"][gene_count]

        # #unconditional probability distribution
        # #For anyone with no parents listed in the data set,
        # if mother and father == None:
        #     #use the probability distribution PROBS["gene"]
        #     # to determine the probability that they have a
        #     # particular number of the gene.
        #     joint_prob[person]["gene"] += PROBS["gene"]

        # #For anyone with parents in the data set
        # else:
        #     #each parent will pass one of their
        #     # two genes on to their child randomly
        #     #TODO^
        #     if mother and father in two_genes:
        #         #there is a PROBS["mutation"] chance that it mutates
        #         joint_prob[person]["gene"] += PROBS["mutation"]

        # #conditional probability distribution
        # if person not in have_trait:
        #     joint_prob[person]["trait"] += PROBS["trait"][gene_count][False]


        # #compute the probability that a person does or does
        # # not have a particular trait.
        # else:
        #     joint_prob[person]["trait"] += PROBS["trait"][gene_count][True]


    #return joint_prob

    #raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # For each person in probabilities
    for person in probabilities:
        gene_count = 1 if person in one_gene else 2 if person in two_genes else 0
        has_trait = True if person in have_trait else False
        # Update the probabilities[person]["gene"] distribution
        probabilities[person]["gene"][gene_count] += p#[person]["gene"]

        # Update the probabilities[person]["trait"] distribution
        probabilities[person]["trait"][has_trait] += p#[person]["trait"]
        


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        print(f"person: {person}", probabilities[person])
        gene_factor = sum(probabilities[person]["gene"].values())
        trait_factor = sum(probabilities[person]["trait"].values())
        print(f"gene_factor: {gene_factor}")
        print(f"trait_factor: {trait_factor}")
        for gene_number in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_number] /= gene_factor
        for trait_value in probabilities[person]["trait"]:
            if trait_factor != 0:
                probabilities[person]["trait"][trait_value] /= trait_factor

    #raise NotImplementedError


if __name__ == "__main__":
    main()
