#!/usr/bin/env python3
# Copyright 2019 Joren Van Onder <joren.vanonder@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse
import random
import sys
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


def generate_lines(n, abuse_ratio=None):
    fmt = "[{timestamp}] {ip} {endpoint} {time:.2f}"
    max_seconds = 100
    log_length = timedelta(days=30)
    end = datetime.now()
    begin = end - log_length
    output = []
    bad_ip = random_ip()

    timestamps = [
        datetime.fromtimestamp(random.uniform(end.timestamp(), begin.timestamp()))
        for _ in range(n)
    ]

    for timestamp in sorted(timestamps):
        endpoint = get_endpoint()
        output.append(
            fmt.format(
                timestamp=timestamp,
                ip=random.choice((bad_ip,) + (random_ip(),) * (abuse_ratio - 1))
                if abuse_ratio
                else random_ip(),
                endpoint=endpoint.url,
                time=gamma.rvs(endpoint.gamma_shape, scale=max_seconds / 10),
            )
        )

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--abuse-ratio",
        help="How many times on average an abuser will do a request per [abuse ratio] requests",
        type=int,
    )
    parser.add_argument("lines", help="How many lines to generate", type=int)
    args = parser.parse_args()

    if args.abuse_ratio < 1:
        print("Abuse ratio must be >= 1.")
        sys.exit(1)

    print(generate_lines(args.lines, args.abuse_ratio))
