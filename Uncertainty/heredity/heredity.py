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
    probability = 1
    
    for person in people:
        gene_count = (1 if person in one_gene else
                      2 if person in two_genes else 0)
        has_trait = person in have_trait

        mother = people[person]["mother"]
        father = people[person]["father"]

        if mother is None and father is None:
            gene_prob = PROBS["gene"][gene_count]
        else:
            mother_probs = get_parent_probability(mother, one_gene, two_genes)
            father_probs = get_parent_probability(father, one_gene, two_genes)

            if gene_count == 0:
                gene_prob = mother_probs[0] * father_probs[0]
            elif gene_count == 1:
                gene_prob = (mother_probs[0] * father_probs[1] +
                             mother_probs[1] * father_probs[0])
            elif gene_count == 2:
                gene_prob = mother_probs[1] * father_probs[1]

        trait_prob = PROBS["trait"][gene_count][has_trait]

        probability *= gene_prob * trait_prob

    return probability

def get_parent_probability(parent, one_gene, two_genes):
    """
    Return the probability that a parent passes on a gene to their child.
    """
    if parent in two_genes:
        return (1 - PROBS["mutation"]), PROBS["mutation"]
    elif parent in one_gene:
        return 0.5, 0.5
    else:
        return PROBS["mutation"], (1 - PROBS["mutation"])


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    #P FORMAT:
    #p {'Arthur': {'gene': 0.0003, 'trait': 0.44}, 
    # 'Charlie': {'gene': 8.999999999999999e-08, 'trait': 0.1936},
    # 'Fred': {'gene': 2.6999999999999994e-11, 'trait': 0.108416000000000
    
    
    # For each person in probabilities
    for person in probabilities:
        gene_count = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = True if person in have_trait else False
        # Update the probabilities[person]["gene"] distribution
        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][trait] += p

    
    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    # Normalize the probability distributions for each person
    for person in probabilities:
        print(f"person: {person}", probabilities[person])
        
        # Calculate the sum of probabilities for the gene distribution
        gene_factor = sum(probabilities[person]["gene"].values())
        # Calculate the sum of probabilities for the trait distribution
        trait_factor = sum(probabilities[person]["trait"].values())
        
        print(f"gene_factor: {gene_factor}")
        print(f"trait_factor: {trait_factor}")
        
        # Check if the gene_factor is 0, which means no gene probabilities
        if gene_factor == 0:
            print(f"Warning: gene_factor for {person} is 0. Skipping normalization for genes.")
        # Check if the trait_factor is 0, which means no trait probabilities
        if trait_factor == 0:
            print(f"Warning: trait_factor for {person} is 0. Skipping normalization for traits.")
        
        # Normalize the gene distribution probabilities
        for gene_number in probabilities[person]["gene"]:
            if gene_factor != 0:
                probabilities[person]["gene"][gene_number] /= gene_factor
            else:
                probabilities[person]["gene"][gene_number] = 0
        
        # Normalize the trait distribution probabilities
        for trait_value in probabilities[person]["trait"]:
            if trait_factor != 0:
                probabilities[person]["trait"][trait_value] /= trait_factor
            else:
                probabilities[person]["trait"][trait_value] = 0
    
    # Ensure that the sum of each distribution is exactly 1 after normalization
    for person in probabilities:
        gene_total = sum(probabilities[person]["gene"].values())
        trait_total = sum(probabilities[person]["trait"].values())
        
        # Check if the sum of gene probabilities is approximately 1
        assert abs(gene_total - 1.0) < 1e-9, f"Normalization error in genes for {person}: {gene_total}"
        # Check if the sum of trait probabilities is approximately 1
        assert abs(trait_total - 1.0) < 1e-9, f"Normalization error in traits for {person}: {trait_total}"


if __name__ == "__main__":
    main()
