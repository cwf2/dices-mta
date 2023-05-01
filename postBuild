#!/bin/bash
set -x

# download pickle files from Google Drive
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=11HbOHMOFoTyzOsG1udu9qKhtDJnp-5Js' -O data/iliad_speeches.pickle
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1V0av9x5YqpcCS1Jov6YDEF-XN6XMjrXM' -O data/odyssey_speeches.pickle
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1W6dCXEkkjSSKMJzvEC3KQqlefYHRVWAi' -O data/posthomerica_speeches.pickle
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1RYYclPBbtWc_FyitJy6EvTJ9QCZD9BPq' -O data/seneca_tokens.csv
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1MKr9xb-DEjNmQlL1DYZW3uM1LYc6FTAX' -O data/flavian_tokens.csv


# install perseus mirror
git clone https://github.com/cwf2/canonical-greekLit data/canonical-greekLit
