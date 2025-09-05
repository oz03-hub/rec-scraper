# Installation
1. Create a Python virtual environment: `python -m venv env_rec`
2. Activate: `source env_rec/bin/activate`
3. Install the libraries: `pip install -r requirements.txt`
4. Frequently run `pip install -U innertube` while your environment is active, so you get the latest innertube version.

5. Create an `out/` directory at the project's root directory to store scraped trees. You can point the `--out_dir` argument to wherever you want really.

6. Ensure you have `tmux` installed. Why? So you can start the process and forget about it, no longer sitting at the screen and waiting to finish.

# Project Layout
These are open for customization for the developer, but as of now:
- `out/`: Direcotry to store the resulting recommendation trees. Each file here will end in `_rec`.
- `rec_test.ipynb`: innertube API changes, it is not stable, and does not return a clean data format. We need to occasionally verify where the recommendation data is residing in the API results. This notebook helps you interactively filter down the results to recommendations. Read comments there for more explanation.
- `rec.py`: Main script to run the recommendations and save them. Read comments for understanding the arguments.

# How to run
1. Open a tmux session so you can exit and log back in: `tmux new -s rec`.
2. Activate venv: `source env_rec/bin/activate`
3. In the tmux session you can run the python script, example: `python rec.py --input test.csv --out_dir out`, you can leave other arguments default.
4. To exit that tmux session, you do `ctrl+b` then `d`. When you want to attach back `tmux attach -t rec`. To kill a session `tmux kill-ses -t rec`.

Easy tmux: https://tmuxcheatsheet.com/

# Notes
You might notice some videos will keep failing even after many retries, there is a good chance those videos are removed from the website, the test.csv has an example `mDZFZ-IKZT4` id will keep failing, don't panic, other ids should be downloaded.

# Future work
1. Can be multithreaded for faster scraping.
