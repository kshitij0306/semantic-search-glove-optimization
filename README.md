# Semantic Search with GloVe Optimization

Welcome to the Semantic Search with GloVe Optimization project! This repository contains an enhanced semantic search algorithm using GloVe word embeddings for efficient navigation of WordNet.

## Table of Contents

- [Introduction](#introduction)
- [Objective](#objective)
- [Key Features](#key-features)
- [Usage](#usage)
- [Optimization Strategies](#optimization-strategies)
- [Evaluation](#evaluation)
- [Folder Structure](#folder-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The project is inspired by the "Twenty Questions" game, where the goal is to guess a target concept within a limited number of logical queries expressed in Conjunctive Normal Form (CNF). The algorithm leverages GloVe word embeddings to streamline the search process in WordNet.

## Objective

The primary objective is to optimize the search algorithm, replacing an inefficient depth-first approach with a more effective strategy guided by word embeddings. The goal is to achieve quick and accurate identification of target synsets within an average of 100 steps.

## Key Features

- Integration of GloVe word embeddings for semantic analysis.
- Logical queries in CNF for exploring hypernyms, hyponyms, and part-meronyms.
- Binary elimination of possibilities to expedite the search.
- Modular and extensible code structure.

## Usage

To use the semantic search algorithm, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/semantic-search-glove-optimization.git`
2. Navigate to the project directory: `cd semantic-search-glove-optimization`
3. Run the algorithm: `python wn_search.py`
4. Follow on-screen instructions and observe the search efficiency.

## Optimization Strategies

The algorithm employs the following optimization strategies:

- Utilization of GloVe embeddings to calculate centroids for remaining possibilities.
- Binary elimination of potential answers based on logical queries.
- Exploration of hypernyms, hyponyms, and part-meronyms in WordNet.

## Evaluation

The success of the optimization is evaluated based on the algorithm's ability to find the target synset in WordNet within an average of 100 steps. The `Oracle` class in the `wn_eval` module is used for evaluation.

## Folder Structure

- `data/`: Contains GloVe word embeddings files.
- `wn_eval.py`: Module for evaluation using the Oracle class.
- `wn_search.py`: Main search algorithm implementation.
- `README.md`: Project documentation.

## Dependencies

Ensure you have the following dependencies installed:

- nltk
- gensim

Install dependencies using: `pip install -r requirements.txt`

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Your feedback and enhancements are highly appreciated!

## License

This project is licensed under the [MIT License](LICENSE).

Happy searching!
