import sys, gzip
from epub_conversion.wiki_decoder import almost_smart_open, get_redirection_list
import time

def main(path, outpath):
    wiki = almost_smart_open(path)
    redirects_to = {}
    print("Getting redirections")
    redirects = 0
    t0 = time.time()
    speed = 0.0
    for page_title, destination in get_redirection_list(wiki):
        # can we skip a step?
        redirects += 1
        if destination in redirects_to:
            # if yes we can shortcut destination and
            # immediately connect to redirects_ot
            redirects_to[page_title] = redirects_to[destination]
        else:
            # if not wire up page_title to destination
            redirects_to[page_title] = destination
        if redirects % 100 == 0:
            speed = 0.8 * speed + 0.2 * ((1000.0) / (time.time() - t0))
            t0 = time.time()
            print("%d so far, %.3f redirects/s     \r" % (redirects, speed), end="", flush=True)

    print("Got all the redirections, now following redirections")
    total_rewires = 0
    rewires = 0
    epoch = 0
    while True:
        rewires = 0
        print("Epoch %d, total_rewires %d" % (epoch, total_rewires))
        for link, value in redirects_to.items():
            if value in redirects_to:
                redirects_to[link] = redirects_to[value]
                rewires += 1

        total_rewires += rewires
        if rewires is 0:
            break

    with gzip.open(outpath, "wt") as f:
        for source, target in redirects_to.items():
            f.write("%s->%s\n" % (source, target))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("resolve_redirections [wiki_dump_path.bz2] [outpath]")
    dump_path = sys.argv[1]
    outpath = sys.argv[2]
    main(dump_path, outpath)
