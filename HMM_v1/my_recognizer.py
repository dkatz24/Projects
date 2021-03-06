import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    x_lengths = test_set.get_all_Xlengths()

    # Iterate through each example in test set
    for X, lengths in x_lengths.values():
        best_score = float('-inf')
        best_guess = None
        word_probs = {}

        # Iterate through each possible word
        for word, model in models.items():
            try:
                score = model.score(X, lengths)
                word_probs[word] = score

                if score > best_score:
                    best_score = score
                    best_guess = word

            except:
                # Word that cannot be scored given '-inf'
                word_probs[word] = float('-inf')

        # Append probailities & guesses to return
        probabilities.append(word_probs)
        guesses.append(best_guess)

    return probabilities, guesses






    return (probabilities, guesses)