#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)
    print(f"Limit = {limit}")
    """
    YOUR CODE HERE
    Given a weight 'limit' and a list of 'weights'
    Find a combo of weights whose sums equal the weight limits
    Return a tuple of their weights: (zero, one)
    """
    # Step 1: Creates a hash table with 16 buckets
    ht = HashTable(16)

    for item in range(length):
        weight = weights[item]
        item_index = item
        diff_from_limit = limit - weight
        if hash_table_retrieve(ht, weight) is not None:
            answer = (item_index, hash_table_retrieve(ht, diff_from_limit))
            return answer
            
        else:
            hash_table_insert(ht, weight, item_index)
            if hash_table_retrieve(ht, diff_from_limit):
                value_of_matching_key = hash_table_retrieve(ht, diff_from_limit)
                answer = (item_index, value_of_matching_key)
                return answer
            else:
                print("not a match")
    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
