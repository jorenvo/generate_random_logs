#!/usr/bin/env python3
import argparse
import random
from datetime import datetime, timedelta


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
    max_time = 30
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
                time=random.uniform(0, max_time),
            )
        )

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lines", help="How many lines to generate", type=int)
    args = parser.parse_args()

    print(generate_lines(args.lines))
