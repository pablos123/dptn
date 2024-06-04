#!/bin/python3
"""Fetch and search news from Debian Package Tracker."""

import argparse
import json
import time
from pathlib import Path

from bs4 import BeautifulSoup

from dptn.constants import DPT_URL, DPTN_DIR_PATH, NEWS_URL
from dptn.utils import EscapeSecs, make_request


class DebianPackageTrackerNews:
    def __init__(self, package_names: list, color: bool) -> None:
        self.packages = {
            package_name: [
                Path(DPTN_DIR_PATH) / str(package_name),
                Path(DPTN_DIR_PATH) / f"{package_name}.json",
            ]
            for package_name in package_names
        }
        self.color = color

    def fetch_news(self) -> None:
        self.clean_old_files()

        for package_name in self.packages:
            news_list = []
            page_number = 1
            response = make_request(self.get_news_url(package_name, page_number))
            while response.status_code != 404:
                self.get_news(response.text, news_list)
                page_number += 1
                time.sleep(0.5)
                response = make_request(self.get_news_url(package_name, page_number))

            if news_list == []:
                print(f"\nThe are no news for the package {package_name}.")
                continue

            self.write_files(package_name, news_list)

    def write_files(self, package_name: str, news_list: list) -> None:
        str_news = ""
        for news in news_list:
            str_news = f"{str_news}{news['date']};;{news['title']};;{news['url']}\n"

        with self.packages[package_name][0].open(mode="w+") as fh:
            fh.write(str_news)

        str_news_json = json.dumps(news_list)
        with self.packages[package_name][1].open(mode="w+") as fh:
            fh.write(str_news_json)

    def clean_old_files(self) -> None:
        for package_file_paths in self.packages.values():
            package_file_paths[0].unlink(missing_ok=True)
            package_file_paths[1].unlink(missing_ok=True)

    def search(self, search_strings: list) -> None:
        print()
        for package_name, package_file_paths in self.packages.items():
            if self.color:
                print(
                    f"{EscapeSecs.BOLD}{EscapeSecs.UNDERLINE}"
                    f"{EscapeSecs.RED}{package_name}:{EscapeSecs.RESET}"
                )
            else:
                print(f"{package_name}:")

            json_file_path = package_file_paths[1]
            if not json_file_path.is_file():
                print(f"Fetch the news for the package {package_name} first.\n")
                continue

            with json_file_path.open(mode="r") as fh:
                str_json = fh.read()

            for n in json.loads(str_json):
                if all(
                    string in n["title"] or string in n["date"]
                    for string in search_strings
                ):
                    if self.color:
                        self.print_news_color(n)
                    else:
                        self.print_news(n)

    @staticmethod
    def get_news(html: str, news_list: list) -> None:
        soup = BeautifulSoup(html, "html.parser")
        news_li = soup.find_all("li", class_="list-group-item")
        for n in news_li:
            n_soup = BeautifulSoup(str(n), "html.parser")

            title = n_soup.find_all("span", class_="news-title")[0].text.strip()
            date = n_soup.find_all("span", class_="news-date")[0].text.strip()
            url = f"{DPT_URL}{n_soup.a['href'].strip()}"

            news_list.append({"date": date, "title": title, "url": url})

    @staticmethod
    def get_news_url(package_name: str, page_number: int) -> str:
        return NEWS_URL.format(package_name, page_number)

    @staticmethod
    def print_news(n: dict) -> None:
        print(f"{n['date']} " f"{n['title']}\n" f"{n['url']}\n")

    @staticmethod
    def print_news_color(n: dict) -> None:
        print(
            f"{EscapeSecs.BOLD}{EscapeSecs.YELLOW}{n['date']}{EscapeSecs.RESET} "
            f"{EscapeSecs.GREEN}{n['title']}{EscapeSecs.RESET}\n"
            f"{EscapeSecs.ITALIC}{EscapeSecs.BLUE}{n['url']}{EscapeSecs.RESET}\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser("dptn")
    parser.add_argument("packages", nargs="+", help="Names of the selected packages.")
    parser.add_argument(
        "-f",
        "--fetch",
        action="store_true",
        help="Fetch selected packages' news.",
    )
    parser.add_argument(
        "-s",
        "--search",
        action="append",
        help="Search strings in the selected packages' news.",
    )
    parser.add_argument(
        "-C",
        "--no-color",
        action="store_false",
        help="Suppress all escaped sequences.",
    )

    args = parser.parse_args()

    DPTN_DIR_PATH.mkdir(exist_ok=True)

    dptn_inst = DebianPackageTrackerNews(list(args.packages), args.no_color)

    if args.fetch:
        dptn_inst.fetch_news()

    if args.search:
        dptn_inst.search(args.search)
    else:
        dptn_inst.search([""])


if __name__ == "__main__":
    main()
