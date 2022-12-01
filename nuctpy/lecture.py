from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import List, Literal

from nuctpy import NUCT

day_ja2en = {
    "月": "MON",
    "火": "TUE",
    "水": "WED",
    "木": "THU",
    "金": "FRI",
    "土": "SAT",
    "日": "SUN",
    "その他": "OTHER",
}


@dataclass
class Lecture:
    site_id: str
    title: str
    raw_title: str
    year: int | None
    term: Literal["SPR", "FALL", "SPR1", "SPR2", "FALL1", "FALL2", "OTHER"]
    day: List[Literal["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN", "OTHER"]]
    hour: List[int]

    def to_dict(self):
        return asdict(self)


def get_title(raw_title) -> str:
    regex = re.compile(r"(^.+?)\(")
    matched = re.match(regex, raw_title)
    return matched.group(1) if matched else raw_title


def get_year(raw_title, site_id) -> int:
    regex = re.compile(r"^(\d\d\d\d)_")
    matched = re.match(regex, site_id)
    if matched:
        return int(matched.group(1))

    regex = re.compile(r"(\d\d\d\d)")
    matched = re.match(regex, raw_title)
    if matched:
        return int(matched.group(1))

    return 0


def get_term(
    raw_title,
) -> Literal["SPR", "FALL", "SPR1", "SPR2", "FALL1", "FALL2", "OTHER"]:
    regex = re.compile(r"\(.+?年度(..?)\/")
    matched = re.search(regex, raw_title)
    if matched:
        term = matched.group(1)
        if "春１" in term:
            return "SPR1"
        elif "春２" in term:
            return "SPR2"
        elif "秋１" in term:
            return "FALL1"
        elif "秋２" in term:
            return "FALL2"
        elif "春" in term:
            return "SPR"
        elif "秋" in term:
            return "FALL"
        else:
            return "OTHER"
    else:
        return "OTHER"


def get_day_hour(raw_title) -> dict:
    regex = re.compile(r"\(.+?年度..?\/(.+?)\)")
    matched = re.search(regex, raw_title)
    day = set("")
    hours = []
    if matched:
        day_hours = matched.group(1).split(",")
        for day_hour in day_hours:
            for ja, en in day_ja2en.items():
                if ja in day_hour:
                    day.add(en)
            count = 0
            for t in "０１２３４５６７８９":
                if t in day_hour:
                    hours.append(count)
                count += 1
        return {"day": list(day), "hours": hours}
    else:
        return {"day": ["OTHER"], "hours": []}


def get_lectures(nuct=None) -> List[Lecture]:
    if nuct is None:
        nuct = NUCT()

    lectures: List[Lecture] = []
    for site_id, raw_title in nuct.site_id_title.items():
        lectures.append(
            Lecture(
                site_id,
                get_title(raw_title),
                raw_title,
                get_year(raw_title, site_id),
                get_term(raw_title),
                day=get_day_hour(raw_title)["day"],
                hour=get_day_hour(raw_title)["hours"],
            )
        )
    return lectures
