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
    
    #create a dict for the total probability
    #split into gene and trait
    joint_prob = {}
    for person in people:
        joint_prob[person] = {
            "gene": 0,
            "trait": 0
        }
    print(people, "people")
    print(one_gene, "one_gene")
    print(two_genes, "two_genes")
    print(have_trait, "have_trait")
    gene_prob = 1
    trait_prob = 1

    for person in people:
        mother = people[person]["mother"]
        father = people[person]["father"]
        gene_count = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = people[person]["trait"]
        
        print(f"{person}'s mother is {mother}")
        print(f"{person}'s father is {father}")
        print(f"{person} has {gene_count} gene(s)")
        print(f"{person} has trait: {trait}")
        
        #everyone in set `one_gene` has one copy of the gene, and
        #everyone in set `two_genes` has two copies of the gene, and
        #everyone not in `one_gene` or `two_gene` does not have the gene
        gene_prob *= PROBS["gene"][gene_count]
         
        if trait is not None:
            trait_prob *= PROBS["trait"][gene_count][trait]

        #For anyone with no parents listed in the data set,
        if mother and father == None:
        #     #use the probability distribution PROBS["gene"] 
        #     # to determine the probability that they have a 
        #     # particular number of the gene.
            gene_prob *= PROBS["gene"][gene_count]
            trait_prob *= PROBS["trait"][trait]
        
        #For anyone with parents in the data set
        else:
        #     #each parent will pass one of their 
        #     # two genes on to their child randomly
            if mother and father in two_genes:
                gene_prob *= 1
            elif mother in two_genes:
                gene_prob *= 0.5
            elif father in two_genes:
                gene_prob *= 0.5
            gene_prob *= PROBS["mutation"]
                
        #     if mother and father in two_genes:
        #         #there is a PROBS["mutation"] chance that it mutates
        #         joint_prob[person]["gene"] += PROBS["mutation"]
        
        print(f"{person}'s gene probability: {gene_prob}")
        print(f"{person}'s trait probability: {trait_prob}")
        
        joint_prob[person] = {
            "gene": gene_prob,
            "trait": trait_prob
        }
    
    sum_join_prob = gene_prob * trait_prob
    
    print(f"joint_prob: {joint_prob}")
    print(f"sum_join_prob", sum_join_prob)
    return sum_join_prob
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
    
            
    return joint_prob
    
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
        trait = True if person in have_trait else False
        # Update the probabilities[person]["gene"] distribution
        probabilities[person]["gene"][gene_count] += p#[person]["gene"]
        
        if trait:
            # Update the probabilities[person]["trait"] distribution
            probabilities[person]["trait"][trait] += p#[person]["trait"]
        else:
            #update for no trait
            probabilities[person]["trait"][trait] += 1 - p#[person]["trait"]
    
    # raise NotImplementedError


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
