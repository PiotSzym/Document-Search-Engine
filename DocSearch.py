from math import acos, pi

with open("docs.txt", "r") as docs_file:
    corpus = docs_file.read()
    corpus = corpus.splitlines()
corpus_split = [document.split() for document in corpus]

with open("queries.txt","r") as queries_file:
    queries = queries_file.read()
    queries = queries.splitlines()

dictionary = {}

'''
this dictionary will hold all unique words as the keys and as the values
it will hold all documents which contain the word, which makes the
dictionary work both as a unique word dictionary and an inverted index dictionary.
'''

for index, document in enumerate(corpus_split, 1):
    current_doc_words = set()
    for word in document:
        if word not in current_doc_words:
            current_doc_words.add(word)
            if word not in dictionary: # check if word has been seen in corPus so far
                dictionary[word] = [index]
            else:
                dictionary[word].append(index)
print("Words in dictionary:", len(dictionary))

for query in queries:
    print("Query:",query)
    query_words = query.split()
    num_words = len(query_words)
    relevant_docs = None
    for word in query_words:
        if word in dictionary: # If the query word isn't in the dictionary, it's not in any document
            word_docs = set(dictionary[word])
            if relevant_docs == None: # checks if 1st iteration
                relevant_docs = word_docs
            else:
                relevant_docs = relevant_docs & word_docs
        else:
            relevant_docs = set()
            break # if at any point a query wOrd isn't in the dictionary then there are no docs which have the query
    if relevant_docs == None: # check if there was a query, edge case
        relevant_docs = set()
    relevant_docs = list(relevant_docs)
    rel_docs_text = ' '.join(map(str,relevant_docs)) # make it into a string with spaces between The values
    print("Relevant documents:",rel_docs_text)
    
    doc_vectors = {}
    for doc in relevant_docs:
        doc_vectors[doc] = []
        temp_document = corpus_split[doc-1]
        for word in dictionary:
            doc_vectors[doc].append(temp_document.count(word))
            '''
            this counts the number of times each word in the dictionary
            shows up in the document and adds that number as a vector value
            '''
    
    query_vector = []
    query_word_set = set(query_words)
    for word in dictionary:
        query_vector.append(1 if word in query_word_set else 0)
    mag_of_query_vector = sum(query_vector)**0.5

    # angle = cos-1 (A.B / |A||B|) 
    angles = {}
    for document_id in relevant_docs:
        mag_of_doc_vector = sum([i**2 for i in doc_vectors[document_id]])**0.5
        dot_product = 0
        for i in range(len(query_vector)):
            dot_product += query_vector[i]*doc_vectors[document_id][i]
        angles[document_id] = round(acos(min(1.0, dot_product / (mag_of_doc_vector*mag_of_query_vector))) * 180 / pi, 6)
        # big math, its just the angle math from the comment above + tuRning the angle from radian to degree + rounding the value
    angles = dict(sorted(angles.items(), key=lambda item: item[1])) # sort dict by value
    for key in angles:
        print(key, angles[key])