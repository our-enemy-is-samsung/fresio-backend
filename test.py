from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel, Field
from typing_extensions import Literal
import random


class StudentSchema(BaseModel):
    student_id: str = Field(..., description="학생 ID")
    name: str = Field(..., description="학생 이름")
    gender: Literal["male", "female"] = Field(..., description="성별")
    level: Literal["상", "중", "하"] = Field(None, description="등급")


def create_matches(
    students: List[StudentSchema],
    match_type: Literal["singles", "doubles"],
    shuffle: bool = True,
) -> List[Dict]:
    """
    학생들을 레벨별로 단식 또는 복식 매칭을 생성합니다.

    Args:
        students: 학생 목록
        match_type: 'singles' 또는 'doubles'
        shuffle: 랜덤 매칭 여부 (기본값: True)

    Returns:
        매칭 결과 리스트
    """
    # 레벨별로 학생들을 그룹화
    level_groups: Dict[str, List[StudentSchema]] = {"상": [], "중": [], "하": []}

    for student in students:
        if student.level:  # None이 아닌 경우만
            level_groups[student.level].append(student)

    matches = []

    for level, level_students in level_groups.items():
        if shuffle:
            random.shuffle(level_students)

        if match_type == "singles":
            # 단식 매칭
            for i in range(0, len(level_students) - 1, 2):
                if i + 1 < len(level_students):
                    match = {
                        "type": "singles",
                        "level": level,
                        "match_id": len(matches) + 1,
                        "team1": {
                            "player1": {
                                "id": level_students[i].student_id,
                                "name": level_students[i].name,
                            }
                        },
                        "team2": {
                            "player1": {
                                "id": level_students[i + 1].student_id,
                                "name": level_students[i + 1].name,
                            }
                        },
                    }
                    matches.append(match)

        else:  # doubles
            # 복식 매칭
            for i in range(0, len(level_students) - 3, 4):
                if i + 3 < len(level_students):
                    match = {
                        "type": "doubles",
                        "level": level,
                        "match_id": len(matches) + 1,
                        "team1": {
                            "player1": {
                                "id": level_students[i].student_id,
                                "name": level_students[i].name,
                            },
                            "player2": {
                                "id": level_students[i + 1].student_id,
                                "name": level_students[i + 1].name,
                            },
                        },
                        "team2": {
                            "player1": {
                                "id": level_students[i + 2].student_id,
                                "name": level_students[i + 2].name,
                            },
                            "player2": {
                                "id": level_students[i + 3].student_id,
                                "name": level_students[i + 3].name,
                            },
                        },
                    }
                    matches.append(match)

    # 매칭되지 못한 학생들 정보 추가
    unmatched = get_unmatched_students(students, matches, match_type)

    return {
        "matches": matches,
        "unmatched_students": unmatched,
        "total_matches": len(matches),
        "statistics": {
            "상": len([m for m in matches if m["level"] == "상"]),
            "중": len([m for m in matches if m["level"] == "중"]),
            "하": len([m for m in matches if m["level"] == "하"]),
        },
    }


def get_unmatched_students(
    students: List[StudentSchema], matches: List[Dict], match_type: str
) -> List[Dict]:
    """
    매칭되지 못한 학생들을 찾습니다.
    """
    matched_ids = set()

    for match in matches:
        matched_ids.add(match["team1"]["player1"]["id"])
        matched_ids.add(match["team2"]["player1"]["id"])

        if match_type == "doubles":
            matched_ids.add(match["team1"]["player2"]["id"])
            matched_ids.add(match["team2"]["player2"]["id"])

    unmatched = []
    for student in students:
        if student.student_id not in matched_ids:
            unmatched.append(
                {"id": student.student_id, "name": student.name, "level": student.level}
            )

    return unmatched


# 사용 예시
def main():
    # 테스트 데이터
    test_students = [
        StudentSchema(student_id="1", name="학생1", gender="male", level="상"),
        StudentSchema(student_id="2", name="학생2", gender="male", level="상"),
        StudentSchema(student_id="3", name="학생3", gender="female", level="상"),
        StudentSchema(student_id="4", name="학생4", gender="male", level="상"),
        StudentSchema(student_id="5", name="학생5", gender="female", level="중"),
        StudentSchema(student_id="6", name="학생6", gender="male", level="중"),
        StudentSchema(student_id="7", name="학생7", gender="male", level="중"),
        StudentSchema(student_id="8", name="학생8", gender="female", level="중"),
    ]

    # 단식 매칭
    singles_result = create_matches(test_students, "singles")
    print("\n=== 단식 매칭 결과 ===")
    for match in singles_result["matches"]:
        print(f"\n매치 {match['match_id']} (레벨: {match['level']})")
        print(
            f"{match['team1']['player1']['name']} vs {match['team2']['player1']['name']}"
        )

    if singles_result["unmatched_students"]:
        print("\n매칭되지 않은 학생들:")
        for student in singles_result["unmatched_students"]:
            print(f"{student['name']} (레벨: {student['level']})")

    # 복식 매칭
    doubles_result = create_matches(test_students, "doubles")
    print("\n\n=== 복식 매칭 결과 ===")
    for match in doubles_result["matches"]:
        print(f"\n매치 {match['match_id']} (레벨: {match['level']})")
        print(
            f"{match['team1']['player1']['name']}, {match['team1']['player2']['name']} vs "
            f"{match['team2']['player1']['name']}, {match['team2']['player2']['name']}"
        )

    if doubles_result["unmatched_students"]:
        print("\n매칭되지 않은 학생들:")
        for student in doubles_result["unmatched_students"]:
            print(f"{student['name']} (레벨: {student['level']})")


if __name__ == "__main__":
    main()
