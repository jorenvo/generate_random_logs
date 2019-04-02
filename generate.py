#!/usr/bin/env python3
import argparse
import random
from collections import namedtuple
from datetime import datetime, timedelta
from scipy.stats import gamma


def random_ip():
    return "{}.{}.{}.{}".format(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def get_endpoint():
    Endpoint = namedtuple("Endpoint", ["url", "gamma_shape"])
    return random.choice(
        (
            Endpoint("/user/status", 0.05),
            Endpoint("/user/messages", 0.10),
            Endpoint("/message/send", 0.05),
            Endpoint("/post/read", 0.05),
            Endpoint("/export", 5),
            Endpoint("/logout", 0.05),
            Endpoint("/login", 0.15),
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
        endpoint = get_endpoint()
        output.append(
            fmt.format(
                timestamp=timestamp,
                ip=random_ip(),
                endpoint=endpoint.url,
                time=gamma.rvs(endpoint.gamma_shape, scale=max_seconds / 10),
            )
        )

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lines", help="How many lines to generate", type=int)
    args = parser.parse_args()

    print(generate_lines(args.lines))
