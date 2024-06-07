import nltk
from nltk.corpus import wordnet

def find_species(text):
  """
  This function takes text as input and returns a list of possible species names (common and scientific).

  Args:
      text: String containing the text to be analyzed.

  Returns:
      list: A list of potential species names found in the text.
  """
  species_list = []
  # Tokenize the text (split into words)
  tokens = nltk.word_tokenize(text.lower())

  # Loop through each token
  for token in tokens:
    # Check if the token is a named entity using NLTK
    if nltk.pos_tag([token])[0][1] == "NNP":  # Proper Noun
      # Check if it's also a word in WordNet
      if wordnet.synsets(token):
        # Loop through each synset (meaning) of the token
        for synset in wordnet.synsets(token):
          # Get the lemmas (possible forms) of the synset
          lemmas = synset.lemmas()
          # Check if any lemma has a hypernym (parent term) labeled as 'fauna'
          for lemma in lemmas:
            hypernyms = lemma.hypernyms()
            for hypernym in hypernyms:
              if hypernym.name() == 'fauna.n.01':  # 'fauna' synset
                species_list.append(token)
                species_list.append(lemma.name())
                break  # Move to next token after finding a species

  return list(set(species_list))  # Remove duplicates

# Example usage
text = "I saw a brown bear (Ursus arctos) while hiking yesterday. There were also some robins singing in the trees."
species_found = find_species(text)
print(species_found)