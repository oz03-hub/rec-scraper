import argparse, json, time
from collections import deque
from innertube import InnerTube
import pandas as pd
from tqdm import tqdm

client = InnerTube("WEB")

def get_recs(video_id, limit=11):
    try:
        resp = client.next(video_id=video_id)
        results = (
            resp["contents"]["twoColumnWatchNextResults"]["secondaryResults"]["secondaryResults"]["results"]
        )
        ids = [
            item['lockupViewModel']['contentId']
            for item in results
            if "lockupViewModel" in item and len(item['lockupViewModel']['contentId']) == 11
        ]
        # print(ids)
        print(f"Collected {len(ids)} ids from {video_id}")
        return ids[:limit]
    except Exception as e:
        print(f"[warn] {video_id}: {e}")
        return []

def recursive_dfs(current_id: str, current_depth: int, max_depth: int):
    if current_depth == max_depth:
        return dict(), 0
    
    sub_tree = dict()
    stack = get_recs(current_id)
    l = len(stack)
    for child_id in stack:
        child_tree, ls = recursive_dfs(child_id, current_depth+1, max_depth)
        l += ls
        sub_tree[child_id] = child_tree

    return sub_tree, l

def crawl(start_id: str, depth: int = 2):
    """
    DFS Crawl
    """
    tree = dict()
    sub_tree, l = recursive_dfs(start_id, 0, depth)
    tree [start_id] = sub_tree
    return tree, l

if __name__ == "__main__":
    input_file = "random_prefix_26000_20240617_150es.csv"
    depth = 3
    max_retries = 5

    df = pd.read_csv(input_file, header=0)
    ids = df["id"].to_list()
    print(f"{len(ids)} IDs to process")

    for id in ids:
        print(f"===> Crawling {id}.")
        out_file = f"out/{id}_rec.json"

        retries = 0
        tree, number_nodes = crawl(id, depth)
        while number_nodes < 10 and retries < max_retries:
            print("---> Sleeping to try again")
            time.sleep(2)
            tree, number_nodes = crawl(id, depth)
            retries += 1

        with open(out_file, "w") as fh:
            json.dump(tree, fh, indent=2)
        print(f"===> Total {number_nodes} videos captured.")


# if __name__ == "__main__":
#     start_time = time.time()
#     ap = argparse.ArgumentParser()
#     ap.add_argument("video_id", help="starting YouTube video ID")
#     ap.add_argument("--depth", type=int, default=2, help="max hop distance")
#     ap.add_argument("--out", default="rec_tree.json", help="output file")
#     args = ap.parse_args()

#     print(f"Starting crawl from video: {args.video_id}")
#     print(f"Crawl depth: {args.depth}")

#     max_retries = 5
#     retries = 0
#     tree, number_nodes = crawl(args.video_id, args.depth)
#     while number_nodes < 10 and retries < max_retries:
#         print("Sleeping to try again")
#         time.sleep(2)
#         tree, number_nodes = crawl(args.video_id, args.depth)
#         retries += 1

#     with open(args.out, "w") as fh:
#         json.dump(tree, fh, indent=2)
#     print(f"Total time: {time.time() - start_time:.2f} seconds")
#     print(f"Total {number_nodes} videos captured.")
