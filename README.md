# Multimodal E-Commerce Search

Assignment 06 by Trần Hải Nam, B23DCDT176, class D23CQCE01-B.

The complete assignment is in [assignment06](assignment06/). It includes
the Python prototype, product and order datasets, sample images,
three editable Visual Paradigm diagrams, report, tests, and demo results.

## Main files

- [Python entry point](assignment06/main.py)
- [Setup and example commands](assignment06/README.md)
- [PDF report](assignment06/report/Bao_cao_Assignment06_Tran_Hai_Nam.pdf)
- [Editable Word draft](assignment06/report/Bao_cao_Assignment06_Tran_Hai_Nam_EDITABLE_DRAFT.docx)
- [Final Visual Paradigm project](assignment06/uml/assignment06_multimodal_search_final.vpp)
- [Complete package ZIP](Assignment06_Tran_Hai_Nam_B23DCDT176.zip)

## Run the prototype

Requires Python 3.10 or later and Pillow.

```sh
cd assignment06
python -m pip install -r requirements.txt
python main.py
```

The demonstration runs text, simulated voice, image, combined text/image,
and order searches. For the local browser interface:

```sh
python web.py
```

Open http://127.0.0.1:8765.

## Implementation

The source follows three layers:

- `presentation/`: input handling and displaying results.
- `application/`: query processing, image features, retrieval, and ranking.
- `data/`: repositories, in-memory vector index, JSON data, and images.

Task 5 includes a product repository, keyword search, simulated voice
search, image-similarity search, and Top-k ranking. Optional features
include text/image score fusion, price and category filters, stock-aware
ranking, order-status lookup, and a local web interface.

Voice input is a typed transcript. Image matching uses handcrafted
64-dimensional pixel features and cosine similarity. This version does
not use real speech recognition, neural embeddings, or a vector database.

## Check the program

From the `assignment06` folder:

```sh
python -m unittest discover -s tests -v
python evaluate.py
```

The recorded results are 13 passing functional tests and 10 successful
queries out of 12 (83.33%) on the bundled test data.

## Report screenshots

The report currently contains native Visual Paradigm exports, which retain
the evaluation watermark. [SCREENSHOTS.txt](assignment06/SCREENSHOTS.txt)
explains how to replace Figures 1-3 with screenshots from the final project.
The PDF layout was checked. The optional Word draft needs its page layout
checked after inserting screenshots.
