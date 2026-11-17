import argparse
import sys

import agent
import rag_store


def main():
    parser = argparse.ArgumentParser(description="Screen-observing bot agent")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("run", help="Start the periodic observation loop")
    sub.add_parser("once", help="Capture a single observation")

    query_parser = sub.add_parser("query", help="Search past observations")
    query_parser.add_argument("text", help="Free-text query")
    query_parser.add_argument("-n", "--n-results", type=int, default=5)

    args = parser.parse_args()

    if args.command == "run":
        agent.run_loop()
    elif args.command == "once":
        obs = agent.observe_once()
        print(obs["description"])
    elif args.command == "query":
        for match in rag_store.query(args.text, n_results=args.n_results):
            ts = match["metadata"].get("timestamp", "?")
            print(f"[{ts}] (dist={match['distance']:.3f}) {match['description']}")


if __name__ == "__main__":
    sys.exit(main())
