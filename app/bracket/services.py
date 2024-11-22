from typing import Literal

import random
from app.bracket.entities import Match
from app.student.schema.group import StudentSchema


class BracketService:
    def create_matches(
        self, students: list[StudentSchema], match_type: Literal["single", "double"]
    ) -> dict:
        level_groups = {"상": [], "중": [], "하": []}

        for student in students:
            if student.level:
                level_groups[student.level].append(student)

        matches = []

        for level, level_students in level_groups.items():
            random.shuffle(level_students)

            if match_type == "single":
                for i in range(0, len(level_students) - 1, 2):
                    if i + 1 < len(level_students):
                        match = Match(
                            match_type="single",
                            student1=[level_students[i].name],
                            student2=[level_students[i + 1].name],
                        )
                        matches.append(match)

            else:
                for i in range(0, len(level_students) - 3, 4):
                    if i + 3 < len(level_students):
                        match = Match(
                            match_type="double",
                            student1=[
                                level_students[i].name,
                                level_students[i + 1].name,
                            ],
                            student2=[
                                level_students[i + 2].name,
                                level_students[i + 3].name,
                            ],
                        )
                        matches.append(match)

        return {
            "matches": matches,
            "unmatched_count": self.get_unmatched_count(students, matches),
            "total_matches": len(matches),
        }

    @staticmethod
    def get_unmatched_count(
        students: list[StudentSchema], matches: list[Match]
    ) -> dict:
        matched_ids = set()
        for match in matches:
            matched_ids.update(match.student1)
            matched_ids.update(match.student2)

        unmatched = {"상": 0, "중": 0, "하": 0}
        for student in students:
            if student.level and student.student_id not in matched_ids:
                unmatched[student.level] += 1

        return unmatched
