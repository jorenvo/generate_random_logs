#!/usr/bin/env python3
import argparse
import random
from datetime import datetime, timedelta
from scipy.stats import gamma


def random_ip():
    return "{}.{}.{}.{}".format(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def endpoint():
    return random.choice(
        (
            "/user/status",
            "/user/messages",
            "/message/send",
            "/money/send",
            "/logout",
            "/login",
        )
    )


def generate_lines(n):
    fmt = "[{timestamp}] {ip} {endpoint} {time:.2f}"
    max_seconds = 100
    log_length = timedelta(days=30)
    end = datetime.now()
    begin = end - log_length
    output = []

    timestamps = [
        datetime.fromtimestamp(random.uniform(end.timestamp(), begin.timestamp()))
        for _ in range(n)
    ]

    for timestamp in sorted(timestamps):
        output.append(
            fmt.format(
                timestamp=timestamp,
                ip=random_ip(),
                endpoint=endpoint(),
                time=gamma.rvs(0.05, scale=max_seconds / 10),
            )
        )

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lines", help="How many lines to generate", type=int)
    args = parser.parse_args()

    print(generate_lines(args.lines))
