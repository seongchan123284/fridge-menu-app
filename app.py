import json
import os
from datetime import date, timedelta
from pathlib import Path

import streamlit as st

DATA_FILE = Path("fridge_data.json")

# 작은 예제 레시피 데이터베이스. 필요하면 계속 추가할 수 있습니다.
RECIPES = [
    {
        "name": "두부 계란국",
        "ingredients": ["두부", "계란", "양파", "대파"],
        "extra": ["국간장 또는 소금", "물"],
        "time": 15,
        "difficulty": "쉬움",
        "steps": [
            "양파와 두부를 먹기 좋은 크기로 썹니다.",
            "냄비에 물과 양파를 넣고 끓입니다.",
            "두부를 넣고 3~4분 더 끓입니다.",
            "풀어 둔 계란을 천천히 둘러 넣습니다.",
            "대파를 넣고 소금이나 국간장으로 간을 맞춥니다.",
        ],
    },
    {
        "name": "계란말이",
        "ingredients": ["계란", "양파", "대파"],
        "extra": ["소금", "식용유"],
        "time": 10,
        "difficulty": "보통",
        "steps": [
            "양파와 대파를 잘게 다집니다.",
            "계란을 풀고 다진 채소와 소금을 섞습니다.",
            "팬에 기름을 얇게 두르고 약불로 달굽니다.",
            "계란물을 나누어 부으며 조금씩 말아 익힙니다.",
        ],
    },
    {
        "name": "두부부침",
        "ingredients": ["두부", "대파"],
        "extra": ["식용유", "간장", "참기름(선택)"],
        "time": 10,
        "difficulty": "쉬움",
        "steps": [
            "두부의 물기를 키친타월로 제거하고 도톰하게 썹니다.",
            "팬에 식용유를 두르고 중불에서 앞뒤로 노릇하게 굽습니다.",
            "대파를 잘게 썰어 간장과 섞어 곁들입니다.",
        ],
    },
    {
        "name": "채소 계란볶음",
        "ingredients": ["계란", "양파", "대파"],
        "extra": ["식용유", "소금 또는 간장"],
        "time": 8,
        "difficulty": "쉬움",
        "steps": [
            "양파와 대파를 얇게 썹니다.",
            "팬에 기름을 두르고 양파를 볶습니다.",
            "계란을 풀어 넣고 크게 저으며 익힙니다.",
            "대파를 넣고 소금이나 간장으로 간을 맞춥니다.",
        ],
    },
    {
        "name": "두부 채소볶음",
        "ingredients": ["두부", "양파", "대파"],
        "extra": ["식용유", "간장", "고춧가루(선택)"],
        "time": 12,
        "difficulty": "쉬움",
        "steps": [
            "두부의 물기를 빼고 한입 크기로 자릅니다.",
            "양파와 대파를 썹니다.",
            "팬에 두부를 먼저 노릇하게 굽습니다.",
            "양파와 대파를 넣고 간장으로 간해 볶습니다.",
        ],
    },
    {
        "name": "간단 두부조림",
        "ingredients": ["두부", "양파", "대파"],
        "extra": ["간장", "물", "고춧가루(선택)", "설탕 약간(선택)"],
        "time": 15,
        "difficulty": "쉬움",
        "steps": [
            "두부를 도톰하게 썰고 양파와 대파를 썹니다.",
            "팬에 두부와 양파를 올립니다.",
            "간장, 물, 선택 양념을 섞어 붓습니다.",
            "중약불에서 양념이 자작해질 때까지 끓이고 대파를 올립니다.",
        ],
    },
    {
        "name": "김치볶음밥", "ingredients": ["김치"], "extra": ["밥", "식용유", "참기름(선택)"],
        "time": 10, "difficulty": "쉬움",
        "steps": ["김치를 잘게 썰어 준비합니다.", "팬에 식용유를 두르고 김치를 2~3분 볶습니다.", "밥을 넣고 골고루 볶습니다.", "기호에 따라 참기름을 넣어 마무리합니다."],
    },
    {
        "name": "김치전", "ingredients": ["김치"], "extra": ["밀가루", "물", "식용유"],
        "time": 12, "difficulty": "쉬움",
        "steps": ["김치를 잘게 썹니다.", "밀가루와 물을 섞어 반죽하고 김치를 넣습니다.", "팬에 식용유를 두르고 반죽을 얇게 펼칩니다.", "앞뒤로 노릇하게 부칩니다."],
    },
    {
        "name": "김치찌개", "ingredients": ["김치"], "extra": ["물", "참치 또는 돼지고기(선택)", "두부(선택)"],
        "time": 20, "difficulty": "쉬움",
        "steps": ["김치를 먹기 좋은 크기로 썹니다.", "냄비에 김치를 넣고 2~3분 볶습니다.", "물을 붓고 끓입니다.", "선택한 재료를 넣고 충분히 끓입니다."],
    },
    {
        "name": "김치 계란볶음", "ingredients": ["김치", "계란"], "extra": ["식용유", "소금 약간"],
        "time": 8, "difficulty": "쉬움",
        "steps": ["김치를 잘게 썹니다.", "팬에 식용유를 두르고 김치를 볶습니다.", "계란을 넣고 취향에 맞게 익힙니다.", "필요하면 소금으로 간을 맞춥니다."],
    },
    {
        "name": "두부김치", "ingredients": ["김치", "두부"], "extra": ["식용유", "참기름(선택)"],
        "time": 15, "difficulty": "쉬움",
        "steps": ["두부를 먹기 좋게 썰어 데우거나 굽습니다.", "김치를 썰어 팬에 볶습니다.", "두부와 볶은 김치를 함께 담습니다."],
    },

    {
        "name": "삼겹살 구이",
        "ingredients": ["삼겹살"],
        "extra": ["소금", "후추", "쌈채소(선택)", "쌈장(선택)"],
        "time": 15, "difficulty": "쉬움",
        "steps": ["삼겹살의 물기를 닦고 먹기 좋은 크기로 준비합니다.", "달군 팬에 삼겹살을 올려 중불에서 굽습니다.", "앞뒤로 노릇하게 익히고 기름이 많으면 키친타월로 제거합니다.", "속까지 충분히 익었는지 확인한 뒤 소금이나 쌈장과 함께 먹습니다."]
    },
    {
        "name": "삼겹살 김치볶음",
        "ingredients": ["삼겹살", "김치"],
        "extra": ["대파(선택)", "고춧가루(선택)"],
        "time": 15, "difficulty": "쉬움",
        "steps": ["삼겹살과 김치를 먹기 좋은 크기로 썹니다.", "팬에서 삼겹살을 먼저 충분히 익힙니다.", "김치를 넣고 삼겹살 기름에 함께 볶습니다.", "기호에 따라 대파나 고춧가루를 넣어 마무리합니다."]
    },
    {
        "name": "간장 삼겹살 볶음",
        "ingredients": ["삼겹살", "양파"],
        "extra": ["간장", "설탕 또는 올리고당", "마늘(선택)"],
        "time": 15, "difficulty": "쉬움",
        "steps": ["삼겹살과 양파를 썹니다.", "팬에서 삼겹살을 충분히 익힙니다.", "양파를 넣고 볶습니다.", "간장과 설탕을 조금 넣어 골고루 볶아 마무리합니다."]
    },
    {
        "name": "고추장 삼겹살 볶음",
        "ingredients": ["삼겹살"],
        "extra": ["고추장", "간장", "설탕", "마늘(선택)", "양파(선택)"],
        "time": 18, "difficulty": "보통",
        "steps": ["삼겹살을 한입 크기로 썹니다.", "고추장, 간장, 설탕을 섞어 양념을 만듭니다.", "팬에서 삼겹살을 익히다가 기름을 적당히 제거합니다.", "양념을 넣고 타지 않게 볶아 속까지 익힙니다."]
    },
    {
        "name": "삼겹살 숙주볶음",
        "ingredients": ["삼겹살", "숙주"],
        "extra": ["간장", "후추", "대파(선택)"],
        "time": 12, "difficulty": "쉬움",
        "steps": ["삼겹살을 먹기 좋게 썹니다.", "팬에서 삼겹살을 충분히 익힙니다.", "숙주를 넣고 센 불에서 빠르게 볶습니다.", "간장과 후추로 간을 맞춥니다."]
    },
    {
        "name": "돼지고기 김치찌개",
        "ingredients": ["삼겹살", "김치"],
        "extra": ["물", "두부(선택)", "대파(선택)"],
        "time": 25, "difficulty": "보통",
        "steps": ["삼겹살과 김치를 썹니다.", "냄비에서 삼겹살을 볶아 기름을 냅니다.", "김치를 넣고 함께 볶은 뒤 물을 붓습니다.", "끓으면 불을 줄여 충분히 끓이고 두부나 대파를 넣습니다."]
    },
    {
        "name": "삼겹살 덮밥",
        "ingredients": ["삼겹살"],
        "extra": ["밥", "양파(선택)", "간장", "설탕"],
        "time": 15, "difficulty": "쉬움",
        "steps": ["삼겹살을 잘게 썹니다.", "팬에서 삼겹살을 충분히 익힙니다.", "간장과 설탕을 조금 넣고 볶습니다.", "밥 위에 올리고 양파가 있으면 곁들입니다."]
    },
    {
        "name": "돼지고기 채소볶음",
        "ingredients": ["삼겹살", "양파", "대파"],
        "extra": ["간장", "후추", "식용유(필요시)"],
        "time": 15, "difficulty": "쉬움",
        "steps": ["삼겹살과 채소를 먹기 좋은 크기로 썹니다.", "삼겹살을 팬에서 충분히 익힙니다.", "양파와 대파를 넣어 볶습니다.", "간장과 후추로 간을 맞춥니다."]
    },
    {
        "name": "감자채 삼겹살볶음",
        "ingredients": ["삼겹살", "감자"],
        "extra": ["소금", "후추", "양파(선택)"],
        "time": 18, "difficulty": "보통",
        "steps": ["감자는 가늘게 채 썰어 물에 잠깐 담갔다가 물기를 뺍니다.", "삼겹살을 잘게 썰어 팬에서 충분히 익힙니다.", "감자를 넣고 익을 때까지 볶습니다.", "소금과 후추로 간을 맞춥니다."]
    },
    {
        "name": "계란밥",
        "ingredients": ["계란"],
        "extra": ["밥", "간장", "참기름"],
        "time": 5, "difficulty": "쉬움",
        "steps": ["계란을 프라이로 익힙니다.", "따뜻한 밥 위에 계란을 올립니다.", "간장과 참기름을 기호에 맞게 넣어 비빕니다."]
    },
    {
        "name": "감자전",
        "ingredients": ["감자"],
        "extra": ["소금", "식용유"],
        "time": 15, "difficulty": "보통",
        "steps": ["감자를 강판에 갈거나 곱게 채 썹니다.", "물기를 적당히 빼고 소금을 넣습니다.", "팬에 기름을 두르고 얇게 펴서 앞뒤로 노릇하게 부칩니다."]
    },
    {
        "name": "참치 양파볶음",
        "ingredients": ["참치", "양파"],
        "extra": ["간장", "후추", "식용유(필요시)"],
        "time": 8, "difficulty": "쉬움",
        "steps": ["양파를 얇게 썹니다.", "팬에 양파를 볶다가 참치를 넣습니다.", "간장과 후추로 간을 맞춰 볶습니다."]
    },
    {
        "name": "토마토 계란볶음",
        "ingredients": ["토마토", "계란"],
        "extra": ["소금", "식용유", "설탕(선택)"],
        "time": 10, "difficulty": "쉬움",
        "steps": ["토마토를 한입 크기로 썰고 계란을 풉니다.", "팬에서 계란을 반쯤 익혀 덜어 둡니다.", "토마토를 볶다가 계란을 다시 넣습니다.", "소금으로 간을 맞춰 마무리합니다."]
    },
    {
        "name": "닭고기 양파볶음",
        "ingredients": ["닭고기", "양파"],
        "extra": ["간장", "마늘", "후추"],
        "time": 18, "difficulty": "보통",
        "steps": ["닭고기를 한입 크기로 썹니다.", "팬에서 닭고기를 속까지 완전히 익힙니다.", "양파를 넣고 볶습니다.", "간장과 마늘, 후추로 간을 맞춥니다."]
    },

    {
        "name": "닭가슴살 크림 파스타",
        "ingredients": ["닭가슴살", "파스타면"],
        "extra": ["우유", "마늘", "소금", "후추", "치즈(선택)"],
        "time": 20, "difficulty": "보통",
        "steps": ["파스타면을 소금물에 삶고 면수는 조금 남깁니다.", "닭가슴살을 한입 크기로 썰어 팬에서 속까지 익힙니다.", "마늘을 넣어 볶고 우유와 치즈를 넣어 약불로 끓입니다.", "삶은 면을 넣고 면수로 농도를 맞춰 마무리합니다."]
    },
    {
        "name": "닭가슴살 토마토 파스타",
        "ingredients": ["닭가슴살", "파스타면", "토마토"],
        "extra": ["토마토소스", "마늘", "양파(선택)"],
        "time": 20, "difficulty": "쉬움",
        "steps": ["파스타면을 삶아 둡니다.", "닭가슴살을 잘게 썰어 팬에서 완전히 익힙니다.", "마늘과 토마토 또는 토마토소스를 넣고 끓입니다.", "삶은 면을 넣고 소스와 잘 섞습니다."]
    },
    {
        "name": "간장 닭가슴살 덮밥",
        "ingredients": ["닭가슴살", "밥"],
        "extra": ["간장", "설탕 또는 올리고당", "마늘(선택)", "계란(선택)"],
        "time": 12, "difficulty": "쉬움",
        "steps": ["닭가슴살을 얇게 썹니다.", "팬에서 닭가슴살을 속까지 완전히 익힙니다.", "간장과 설탕, 물 약간을 넣고 졸입니다.", "밥 위에 올리고 계란이 있으면 곁들입니다."]
    },
    {
        "name": "닭가슴살 볶음밥",
        "ingredients": ["닭가슴살", "밥"],
        "extra": ["계란", "대파", "간장", "냉동 채소(선택)"],
        "time": 12, "difficulty": "쉬움",
        "steps": ["닭가슴살을 잘게 썰어 팬에서 완전히 익힙니다.", "대파와 냉동 채소가 있으면 넣어 볶습니다.", "밥을 넣고 간장으로 간을 합니다.", "계란을 넣어 함께 볶아 마무리합니다."]
    },
    {
        "name": "닭가슴살 샐러드 덮밥",
        "ingredients": ["닭가슴살", "밥"],
        "extra": ["양상추 또는 샐러드 채소", "마요네즈(선택)", "간장(선택)"],
        "time": 12, "difficulty": "쉬움",
        "steps": ["닭가슴살을 팬이나 전자레인지로 속까지 익힙니다.", "밥을 그릇에 담습니다.", "먹기 좋게 찢은 닭가슴살과 채소를 올립니다.", "기호에 따라 소스나 마요네즈를 조금 곁들입니다."]
    },
    {
        "name": "알리오 올리오",
        "ingredients": ["파스타면", "마늘"],
        "extra": ["식용유 또는 올리브유", "소금", "후추", "페페론치노(선택)"],
        "time": 15, "difficulty": "쉬움",
        "steps": ["파스타면을 삶고 면수를 한 컵 남깁니다.", "팬에 기름과 편마늘을 넣고 약불에서 향을 냅니다.", "삶은 면과 면수를 넣고 빠르게 섞습니다.", "소금과 후추로 간을 맞춥니다."]
    },
    {
        "name": "참치 오일 파스타",
        "ingredients": ["파스타면", "참치"],
        "extra": ["마늘", "식용유 또는 올리브유", "후추", "고추(선택)"],
        "time": 15, "difficulty": "쉬움",
        "steps": ["파스타면을 삶습니다.", "팬에 기름과 마늘을 볶아 향을 냅니다.", "기름을 뺀 참치를 넣어 가볍게 볶습니다.", "면과 면수를 넣고 섞은 뒤 후추로 마무리합니다."]
    },
    {
        "name": "원팬 토마토 파스타",
        "ingredients": ["파스타면", "토마토"],
        "extra": ["토마토소스", "물", "마늘", "소금"],
        "time": 18, "difficulty": "쉬움",
        "steps": ["팬에 파스타면과 토마토소스, 물을 넣습니다.", "중불에서 저어가며 면을 익힙니다.", "토마토와 마늘을 넣고 소스가 졸아들 때까지 끓입니다.", "면이 익었는지 확인하고 소금으로 간을 맞춥니다."]
    },
    {
        "name": "참치마요 덮밥",
        "ingredients": ["참치", "밥"],
        "extra": ["마요네즈", "간장", "김가루(선택)", "계란(선택)"],
        "time": 5, "difficulty": "쉬움",
        "steps": ["참치의 기름을 적당히 뺍니다.", "밥 위에 참치를 올립니다.", "마요네즈와 간장을 조금 뿌립니다.", "김가루나 계란을 곁들입니다."]
    },
    {
        "name": "두부 계란 덮밥",
        "ingredients": ["두부", "계란", "밥"],
        "extra": ["간장", "참기름", "대파(선택)"],
        "time": 10, "difficulty": "쉬움",
        "steps": ["두부를 으깨거나 작게 썹니다.", "팬에서 두부의 수분을 날리며 볶습니다.", "계란을 넣고 익힌 뒤 간장으로 간을 합니다.", "밥 위에 올리고 참기름을 조금 둘러 마무리합니다."]
    },
    {
        "name": "두부 참치 볶음",
        "ingredients": ["두부", "참치"],
        "extra": ["고추장 또는 간장", "양파(선택)", "대파(선택)"],
        "time": 12, "difficulty": "쉬움",
        "steps": ["두부를 한입 크기로 썹니다.", "팬에 참치와 양파를 넣고 볶습니다.", "두부를 넣고 부서지지 않게 섞습니다.", "고추장이나 간장으로 간을 맞춰 졸입니다."]
    },
    {
        "name": "햄 계란 볶음밥",
        "ingredients": ["햄", "계란", "밥"],
        "extra": ["대파(선택)", "간장", "식용유"],
        "time": 10, "difficulty": "쉬움",
        "steps": ["햄과 대파를 잘게 썹니다.", "팬에 햄을 볶고 한쪽으로 밀어 계란을 익힙니다.", "밥을 넣고 고루 볶습니다.", "간장으로 간을 맞춰 마무리합니다."]
    },
    {
        "name": "소시지 야채볶음",
        "ingredients": ["소시지", "양파"],
        "extra": ["케첩", "간장", "식용유", "파프리카(선택)"],
        "time": 12, "difficulty": "쉬움",
        "steps": ["소시지와 양파를 썹니다.", "팬에 소시지를 먼저 볶습니다.", "양파를 넣고 익을 때까지 볶습니다.", "케첩과 간장을 조금 넣어 버무립니다."]
    },
    {
        "name": "만두 계란국",
        "ingredients": ["만두", "계란"],
        "extra": ["물", "국간장", "대파(선택)"],
        "time": 10, "difficulty": "쉬움",
        "steps": ["냄비에 물을 끓이고 국간장으로 간을 합니다.", "냉동만두를 넣고 제품 안내에 맞게 충분히 익힙니다.", "풀어 둔 계란을 둘러 넣습니다.", "계란이 익으면 대파를 넣어 마무리합니다."]
    },
    {
        "name": "김치 참치 볶음밥",
        "ingredients": ["김치", "참치", "밥"],
        "extra": ["식용유", "김가루(선택)", "계란(선택)"],
        "time": 10, "difficulty": "쉬움",
        "steps": ["김치를 잘게 썹니다.", "팬에서 김치와 참치를 볶습니다.", "밥을 넣고 골고루 볶습니다.", "김가루나 계란프라이를 곁들입니다."]
    },
    {
        "name": "감자 베이컨 볶음",
        "ingredients": ["감자", "베이컨"],
        "extra": ["소금", "후추", "양파(선택)"],
        "time": 15, "difficulty": "쉬움",
        "steps": ["감자를 얇게 채 썰어 전자레인지에 2분 정도 익힙니다.", "베이컨을 팬에서 볶습니다.", "감자와 양파를 넣어 충분히 익을 때까지 볶습니다.", "소금과 후추로 간을 합니다."]
    },
    {
        "name": "카레 닭가슴살 덮밥",
        "ingredients": ["닭가슴살", "밥"],
        "extra": ["카레가루 또는 카레 블록", "양파", "물"],
        "time": 18, "difficulty": "쉬움",
        "steps": ["닭가슴살과 양파를 작게 썹니다.", "냄비에서 닭가슴살을 속까지 익히고 양파를 볶습니다.", "물을 붓고 카레가루나 카레 블록을 넣습니다.", "걸쭉해질 때까지 끓여 밥 위에 올립니다."]
    },
    {
        "name": "콩나물 비빔밥",
        "ingredients": ["콩나물", "밥"],
        "extra": ["간장", "참기름", "고춧가루(선택)", "계란(선택)"],
        "time": 10, "difficulty": "쉬움",
        "steps": ["콩나물을 깨끗이 씻어 충분히 익도록 데칩니다.", "밥 위에 콩나물을 올립니다.", "간장과 참기름을 섞어 양념장을 만듭니다.", "양념장을 넣어 비벼 먹습니다."]
    },
    {
        "name": "양배추 참치 덮밥",
        "ingredients": ["양배추", "참치", "밥"],
        "extra": ["간장", "마요네즈(선택)", "후추"],
        "time": 10, "difficulty": "쉬움",
        "steps": ["양배추를 가늘게 썹니다.", "팬에서 양배추를 숨이 죽을 때까지 볶습니다.", "참치를 넣고 간장과 후추로 간을 합니다.", "밥 위에 올리고 기호에 따라 마요네즈를 곁들입니다."]
    },
    {
        "name": "라면 계란죽",
        "ingredients": ["라면", "계란"],
        "extra": ["밥", "물"],
        "time": 8, "difficulty": "쉬움",
        "steps": ["냄비에 물을 평소보다 넉넉히 끓입니다.", "라면 면과 스프를 넣고 잘게 부숩니다.", "밥을 넣고 부드러워질 때까지 끓입니다.", "계란을 풀어 넣고 완전히 익혀 마무리합니다."]
    },

    # 자주 남는 소량 식재료를 활용하는 간단 메뉴 (양념은 매칭 재료에서 제외)
    {"name":"양배추 계란볶음", "ingredients":["양배추","계란"], "extra":["식용유","소금"], "time":8,"difficulty":"쉬움", "steps":["양배추를 가늘게 썹니다.","팬에 양배추를 볶아 숨을 죽입니다.","계란을 넣고 함께 익혀 마무리합니다."]},
    {"name":"양배추전", "ingredients":["양배추","계란"], "extra":["밀가루","물","식용유"], "time":12,"difficulty":"쉬움", "steps":["양배추를 얇게 채 썹니다.","계란과 밀가루, 물을 섞어 반죽합니다.","팬에 얇게 펴서 앞뒤로 익힙니다."]},
    {"name":"오이 계란 샐러드", "ingredients":["오이","계란"], "extra":["마요네즈(선택)"], "time":10,"difficulty":"쉬움", "steps":["계란을 완숙으로 삶습니다.","오이를 잘게 썰고 삶은 계란을 으깹니다.","기호에 따라 마요네즈를 조금 섞습니다."]},
    {"name":"오이 토마토 샐러드", "ingredients":["오이","토마토"], "extra":["치즈(선택)"], "time":5,"difficulty":"쉬움", "steps":["오이와 토마토를 씻어 한입 크기로 썹니다.","그릇에 담고 치즈가 있으면 곁들입니다."]},
    {"name":"버섯 계란볶음", "ingredients":["버섯","계란"], "extra":["식용유","소금"], "time":8,"difficulty":"쉬움", "steps":["버섯을 먹기 좋게 썹니다.","팬에 버섯을 볶습니다.","계란을 넣고 익혀 마무리합니다."]},
    {"name":"버섯 두부볶음", "ingredients":["버섯","두부"], "extra":["식용유","간장"], "time":12,"difficulty":"쉬움", "steps":["버섯과 두부를 한입 크기로 썹니다.","두부를 먼저 노릇하게 굽습니다.","버섯을 넣어 익히고 간장으로 간합니다."]},
    {"name":"애호박 계란볶음", "ingredients":["애호박","계란"], "extra":["식용유","소금"], "time":10,"difficulty":"쉬움", "steps":["애호박을 반달 모양으로 썹니다.","팬에 애호박을 볶아 익힙니다.","계란을 넣고 함께 볶습니다."]},
    {"name":"당근 계란볶음밥", "ingredients":["당근","계란","밥"], "extra":["식용유","간장"], "time":10,"difficulty":"쉬움", "steps":["당근을 잘게 다집니다.","팬에 당근과 계란을 볶습니다.","밥을 넣고 함께 볶아 간장으로 간합니다."]},
    {"name":"브로콜리 계란볶음", "ingredients":["브로콜리","계란"], "extra":["식용유","소금"], "time":10,"difficulty":"쉬움", "steps":["브로콜리를 작게 나누어 살짝 데칩니다.","팬에 브로콜리를 볶습니다.","계란을 넣고 익혀 마무리합니다."]},
    {"name":"콘치즈", "ingredients":["옥수수","치즈"], "extra":["마요네즈(선택)"], "time":8,"difficulty":"쉬움", "steps":["옥수수의 물기를 뺍니다.","그릇에 옥수수와 치즈를 담습니다.","전자레인지나 팬에서 치즈가 녹을 때까지 익힙니다."]},
    {"name":"식빵 계란 토스트", "ingredients":["식빵","계란"], "extra":["치즈(선택)","버터(선택)"], "time":8,"difficulty":"쉬움", "steps":["계란을 풀어 팬에서 익힙니다.","식빵을 굽고 계란을 올립니다.","치즈가 있으면 함께 올려 마무리합니다."]},
    {"name":"치즈 감자구이", "ingredients":["감자","치즈"], "extra":["버터(선택)"], "time":15,"difficulty":"쉬움", "steps":["감자를 얇게 썰어 전자레인지로 먼저 익힙니다.","팬이나 오븐용 그릇에 감자를 담습니다.","치즈를 올려 녹을 때까지 익힙니다."]},
    {"name":"우유 계란죽", "ingredients":["우유","계란","밥"], "extra":["소금"], "time":10,"difficulty":"쉬움", "steps":["냄비에 밥과 우유를 넣고 약불로 끓입니다.","밥알이 부드러워지면 계란을 풀어 넣습니다.","계란이 익을 때까지 저어 마무리합니다."]},
    {"name":"햄 치즈 토스트", "ingredients":["식빵","햄","치즈"], "extra":["버터(선택)"], "time":7,"difficulty":"쉬움", "steps":["식빵 위에 햄과 치즈를 올립니다.","다른 식빵으로 덮습니다.","팬이나 토스터에서 치즈가 녹고 빵이 노릇해질 때까지 굽습니다."]},
    {"name":"어묵 볶음", "ingredients":["어묵","양파"], "extra":["간장","식용유"], "time":10,"difficulty":"쉬움", "steps":["어묵과 양파를 썹니다.","팬에 양파를 볶다가 어묵을 넣습니다.","간장으로 간해 충분히 볶습니다."]},
    {"name":"떡 계란볶이", "ingredients":["떡","계란"], "extra":["고추장","물"], "time":12,"difficulty":"쉬움", "steps":["계란을 삶아 둡니다.","팬에 떡과 물, 고추장을 넣고 끓입니다.","떡이 말랑해지면 삶은 계란을 넣어 조금 더 끓입니다."]},
    {"name":"만두 구이", "ingredients":["만두"], "extra":["식용유","물"], "time":10,"difficulty":"쉬움", "steps":["팬에 기름을 두르고 냉동만두를 올립니다.","바닥이 노릇해지면 물을 조금 넣고 뚜껑을 덮습니다.","속까지 충분히 익히고 수분을 날려 마무리합니다."]},
    {"name":"콩나물 계란볶음", "ingredients":["콩나물","계란"], "extra":["식용유","소금"], "time":8,"difficulty":"쉬움", "steps":["콩나물을 깨끗이 씻어 익힙니다.","팬에 콩나물을 볶습니다.","계란을 넣어 함께 익힙니다."]},
    {"name":"시금치 계란볶음", "ingredients":["시금치","계란"], "extra":["식용유","소금"], "time":8,"difficulty":"쉬움", "steps":["시금치를 씻어 먹기 좋게 자릅니다.","팬에 시금치를 볶아 숨을 죽입니다.","계란을 넣고 익혀 마무리합니다."]},
    {"name":"파프리카 계란볶음", "ingredients":["파프리카","계란"], "extra":["식용유","소금"], "time":8,"difficulty":"쉬움", "steps":["파프리카를 잘게 썹니다.","팬에 파프리카를 볶습니다.","계란을 넣고 함께 익힙니다."]},
]

def load_data():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []
    return []

def save_data(items):
    DATA_FILE.write_text(
        json.dumps(items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def normalize_name(name):
    value = name.strip().replace(" ", "")
    aliases = {
        "돼지고기삼겹살": "삼겹살",
        "삼겹살용돼지고기": "삼겹살",
        "대파": "파",
        "쪽파": "파",
        "달걀": "계란",
        "닭가슴살큐브": "닭가슴살",
        "훈제닭가슴살": "닭가슴살",
        "닭안심": "닭고기",
        "스파게티면": "파스타면",
        "파스타": "파스타면",
        "토마토소스": "토마토",
        "참치캔": "참치",
        "런천미트": "햄",
        "스팸": "햄",
        "비엔나소시지": "소시지",
        "냉동만두": "만두",
        "양배추": "양배추",
        "새송이버섯": "버섯", "표고버섯": "버섯", "팽이버섯": "버섯", "느타리버섯": "버섯",
        "애호박": "애호박", "주키니": "애호박", "파프리카": "파프리카",
        "브로콜리": "브로콜리", "시금치": "시금치", "오이": "오이",
        "옥수수캔": "옥수수", "스위트콘": "옥수수", "모짜렐라치즈": "치즈",
        "슬라이스치즈": "치즈", "체다치즈": "치즈", "식빵": "식빵",
        "어묵": "어묵", "부산어묵": "어묵", "떡볶이떡": "떡", "가래떡": "떡",
    }
    return aliases.get(value, value)

def ingredient_names(items):
    return [item["name"] for item in items]

def recipe_score(recipe, available):
    # 띄어쓰기 차이를 무시하고 현재 냉장고 재료와 비교합니다.
    available_map = {normalize_name(x): x for x in available}
    required = recipe["ingredients"]
    matched = [x for x in required if normalize_name(x) in available_map]
    missing = [x for x in required if normalize_name(x) not in available_map]
    score = len(matched) / len(required) if required else 0
    return score, matched, missing




def ingredient_amount(name, recipe_name=""):
    """1~2인분 기준의 초보자용 대략 계량. 냉장고 보유량과 무관한 조리 기준량입니다."""
    n = normalize_name(name)
    recipe = recipe_name
    # 국물 요리는 메뉴에 따라 물의 양을 다르게 안내합니다.
    if n == "물":
        if "찌개" in recipe:
            return "500ml"
        if "국" in recipe:
            return "500ml"
        if "죽" in recipe:
            return "450~500ml"
        if "파스타" in recipe:
            return "면이 잠길 정도(약 1L, 삶는 물) 또는 레시피 단계 참고"
        if "조림" in recipe:
            return "100ml"
        if "만두" in recipe:
            return "450ml"
        if "카레" in recipe:
            return "250ml"
        return "2~3큰술(30~45ml), 농도에 따라 조절"
    amounts = {
        "계란":"2개", "두부":"150g", "양파":"1/4개(약 50g)", "파":"1/3대(약 20g)",
        "김치":"150~200g", "삼겹살":"150g", "돼지고기":"150g", "닭가슴살":"150g",
        "닭고기":"150g", "참치":"작은 캔 1/2개(약 75g)", "파스타면":"100g",
        "밥":"1공기(약 200g)", "감자":"1개(약 150g)", "토마토":"1개(약 150g)",
        "마늘":"2쪽", "숙주":"100g", "햄":"50g", "소시지":"5~6개(약 80g)",
        "만두":"5~6개", "베이컨":"2줄(약 40g)", "콩나물":"100g", "양배추":"100g",
        "오이":"1/2개", "버섯":"80g", "애호박":"1/3개", "당근":"1/4개",
        "브로콜리":"80g", "옥수수":"80g", "치즈":"1~2장(약 20~40g)",
        "식빵":"2장", "우유":"150ml", "어묵":"1장(약 50g)", "떡":"150g",
        "시금치":"80g", "파프리카":"1/2개", "라면":"1봉지",
    }
    return amounts.get(n, "약 1/2컵 또는 1~2큰술(재료 상태에 맞게 조절)")


def extra_amount(name, recipe_name=""):
    n = name.replace("(선택)", "").strip()
    if "간장" in n: return "1큰술(15ml)"
    if "국간장" in n: return "1/2~1큰술(7.5~15ml)"
    if "고춧가루" in n: return "1큰술(약 6g)"
    if "고추장" in n: return "1큰술(약 20g)"
    if "다진 마늘" in n or n == "마늘": return "1/2큰술(약 5g)"
    if "설탕" in n or "올리고당" in n: return "1작은술(약 5g)"
    if "식용유" in n or "올리브유" in n: return "1큰술(15ml)"
    if "참기름" in n: return "1작은술(5ml)"
    if "마요네즈" in n: return "1큰술(15g)"
    if "토마토소스" in n: return "150g"
    if "우유" in n: return "150ml"
    if "밀가루" in n: return "1/2컵(약 60g)"
    if "소금" in n: return "두 꼬집(약 1g), 마지막에 간 조절"
    if "후추" in n: return "약간"
    if "물" in n: return ingredient_amount("물", recipe_name)
    if "밥" in n: return "1공기(약 200g)"
    return "약간(선택 재료)"


def recipe_water_note(recipe):
    name = recipe["name"]
    if "찌개" in name:
        return "국물은 물 500ml부터 넣으세요. 끓인 뒤 짜면 물 50ml를 추가하고, 싱거우면 국간장 1작은술씩 보충하세요."
    if "국" in name:
        return "국물은 물 500ml 기준입니다. 재료가 잠기지 않으면 50ml씩 추가하세요."
    if "파스타" in name:
        return "면 삶는 물은 약 1L에 소금 1작은술을 사용하고, 면수는 50~100ml 남겨 소스 농도 조절에 사용하세요."
    if "조림" in name:
        return "조림 물은 100ml부터 넣고, 바닥이 마르면 2큰술씩 추가하세요."
    if "카레" in name:
        return "물 250ml부터 넣고 카레가루를 풀어 농도를 확인하세요. 너무 되직하면 50ml씩 추가하세요."
    if "죽" in name:
        return "물 450~500ml 기준입니다. 끓이는 동안 되직해지면 50ml씩 추가하세요."
    return None


def cooking_guide(recipe, step, index):
    """각 조리 단계에 초보자용 불 세기와 대략적인 시간을 붙입니다."""
    name = recipe["name"]
    # 사용자가 예로 든 참치 양파볶음은 단계별 안내를 구체적으로 지정합니다.
    if name == "참치 양파볶음":
        guides = [
            ("불 사용 없음", "약 2분", "양파를 3~5mm 두께로 얇게 썰면 고르게 익습니다."),
            ("약불 2분 → 중불", "약 2~3분", "팬에 기름을 조금 두르고 양파가 투명해질 때까지 볶습니다."),
            ("중불", "약 1~2분", "기름을 뺀 참치를 넣고 양파와 골고루 섞어 따뜻하게 볶습니다."),
            ("약불", "약 30초~1분", "간장은 조금씩 넣고 후추로 마무리합니다. 간이 강해지지 않게 맛을 보세요."),
        ]
        return guides[min(index, len(guides)-1)]

    t = step.replace(" ", "")
    if any(k in t for k in ["썹니다", "다집니다", "손질", "씻", "물기를", "준비합니다", "자릅니다", "갈거나"]):
        return ("불 사용 없음", "약 1~3분", "재료를 비슷한 크기로 손질하면 익는 시간이 일정해집니다.")
    if any(k in t for k in ["끓", "데칩", "삶"]):
        return ("중불로 끓인 뒤 약불", "약 3~8분", "끓어오르면 넘치지 않도록 불을 낮추고 재료가 익었는지 확인합니다.")
    if any(k in t for k in ["굽", "부칩", "전", "프라이"]):
        return ("중불로 시작해 약불 조절", "앞뒤 각 2~4분", "한쪽 면이 노릇해지면 뒤집고, 두꺼운 재료는 약불로 속까지 익힙니다.")
    if any(k in t for k in ["볶", "팬에", "익힙니다", "익힙"]):
        return ("중불", "약 2~4분", "재료가 타지 않도록 자주 저어 주고, 수분이 부족하면 불을 조금 낮춥니다.")
    if any(k in t for k in ["넣", "섞", "비빕", "담", "올립", "마무리"]):
        return ("약불 또는 불 끄기", "약 30초~1분", "재료가 골고루 섞이도록 가볍게 저어 마무리합니다.")
    return ("중약불", "약 1~3분", "재료 상태를 확인하면서 타지 않게 조리합니다.")

st.set_page_config(page_title="오늘의 냉장고", page_icon="🥬", layout="wide", initial_sidebar_state="expanded")

# 앱처럼 보이도록 전체 UI 스타일 적용
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }
.stApp { background: #f6f8f3; }
.block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] { background: #eef3e9; border-right: 1px solid #e0e8d9; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #53634e; }
.hero { background: linear-gradient(120deg,#244b35 0%,#477653 100%); padding: 30px 34px; border-radius: 24px; color: white; margin-bottom: 24px; box-shadow: 0 10px 28px rgba(38,75,52,.13); }
.hero-kicker { color:#dcebd8; font-size: .88rem; font-weight:600; letter-spacing:.08em; }
.hero h1 { color:white; font-size:2.05rem; margin:.35rem 0 .4rem 0; font-weight:800; }
.hero p { color:#e8f1e4; margin:0; font-size:1rem; }
.section-title { color:#243c2b; font-size:1.35rem; font-weight:800; margin: 1.1rem 0 .25rem 0; }
div[data-testid="stTabs"] button { border-radius: 12px; padding: 12px 18px; font-weight:700; }
div[data-testid="stTabs"] button[aria-selected="true"] { background:#e5efdf; color:#285238; }
.stButton>button, .stFormSubmitButton>button { border-radius:12px; border:0; background:#356b45; color:white; font-weight:700; padding:.55rem 1rem; }
.stButton>button:hover, .stFormSubmitButton>button:hover { background:#244b35; color:white; border:0; }
.stTextInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] { border-radius:10px; }
[data-testid="stMetric"] { background:white; border:1px solid #e5ebdf; padding:16px 18px; border-radius:16px; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius:16px; border-color:#e3eadf; background:white; }
[data-testid="stFileUploader"] { background:white; border:1px dashed #b9cbb3; border-radius:16px; padding:12px; }
small, .stCaption { color:#75816f; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='font-size:2rem'>🥬</div><div style='font-size:1.2rem;font-weight:800;color:#244b35'>오늘의 냉장고</div><div style='font-size:.85rem;color:#71806b;margin-top:4px'>냉장고 속 재료로 만드는 한 끼</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("**MY KITCHEN**")
    st.caption("재료를 관리하고, 남김없이 맛있게!")
    st.divider()

st.markdown("""
<div class="hero">
  <div class="hero-kicker">SMART KITCHEN · FOOD WASTE LESS</div>
  <h1>오늘은 냉장고에 뭐가 있을까?</h1>
  <p>식재료와 유통기한을 관리하고, 남김없이 활용할 메뉴를 찾아보세요.</p>
</div>
""", unsafe_allow_html=True)

def get_gemini_api_key():
    """Streamlit secrets 또는 환경변수에서 Gemini API 키를 안전하게 읽습니다."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.getenv("GEMINI_API_KEY", "")


def generate_custom_recipe(menu_name):
    """Gemini를 이용해 입력한 메뉴의 구조화된 레시피를 생성합니다."""
    api_key = get_gemini_api_key()
    if not api_key:
        raise RuntimeError("Gemini API 키가 설정되지 않았습니다. Streamlit Secrets에 GEMINI_API_KEY를 등록해 주세요.")

    from google import genai
    client = genai.Client(api_key=api_key)
    prompt = f"""
너는 한국 가정식과 자취 요리에 익숙한 요리 안내자야.
사용자가 요청한 메뉴: {menu_name}

초보자가 이 설명만 보고 요리할 수 있도록 한국어로 1~2인분 레시피를 작성해.
식재료와 양념은 가능한 한 g, ml, 개, 큰술(15ml), 작은술(5ml) 단위로 계량해.
물이나 육수는 반드시 정확한 시작 용량(ml)을 제시하고, 농도 조절 방법도 설명해.
각 조리 단계마다 불 세기(약불/중불/강불/불 끔), 예상 시간(분), 완료 상태를 구체적으로 적어.
고기·생선·달걀 등은 안전하게 완전히 익히는 방법을 안내해.
필요한 양념은 준비 재료와 별도로 숨기지 말고 모두 적어.
메뉴와 무관한 설명은 하지 말고 JSON 객체만 반환해.

반드시 다음 키를 포함해:
{{
  "name": "메뉴 이름",
  "servings": "1~2인분",
  "time": 25,
  "difficulty": "쉬움/보통/어려움 중 하나",
  "ingredients": [{{"name":"재료명","amount":"150g"}}],
  "steps": [{{"instruction":"구체적인 조리 설명","heat":"중불","minutes":"3~4분","done":"완료 상태 또는 확인 방법"}}],
  "tips": ["조리 팁"],
  "water_note": "물 또는 육수의 양과 조절 방법. 물이 필요 없는 메뉴면 해당 없음이라고 작성"
}}
"""
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={"response_mime_type": "application/json", "temperature": 0.4},
    )
    import json as _json
    result = _json.loads(response.text)
    required = ["name", "servings", "time", "difficulty", "ingredients", "steps"]
    if not all(k in result for k in required) or not result["ingredients"] or not result["steps"]:
        raise ValueError("레시피 응답 형식이 올바르지 않습니다. 메뉴 이름을 조금 바꿔 다시 시도해 주세요.")
    return result


def show_custom_recipe(recipe):
    st.markdown(f"## 🍽️ {recipe['name']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("기준 인분", recipe.get("servings", "1~2인분"))
    c2.metric("예상 조리 시간", f"약 {recipe.get('time', 20)}분")
    c3.metric("난이도", recipe.get("difficulty", "보통"))

    st.markdown("### 🥕 준비 재료와 정확한 계량")
    for item in recipe.get("ingredients", []):
        if isinstance(item, dict):
            st.write(f"• **{item.get('name', '재료')}**: {item.get('amount', '양 조절')}")
        else:
            st.write(f"• {item}")

    water_note = recipe.get("water_note", "")
    if water_note:
        st.info("💧 물·육수 안내: " + str(water_note))

    st.markdown("### 👩‍🍳 단계별 조리 순서")
    for i, step in enumerate(recipe.get("steps", []), 1):
        if isinstance(step, dict):
            st.markdown(f"**{i}단계. {step.get('instruction', '')}**")
            a, b = st.columns(2)
            a.caption(f"🔥 불 세기: {step.get('heat', '중불')}")
            b.caption(f"⏱️ 예상 시간: {step.get('minutes', '상태 확인')}")
            if step.get("done"):
                st.caption("✔ 완료 기준: " + str(step["done"]))
        else:
            st.markdown(f"**{i}단계. {step}**")

    if recipe.get("tips"):
        st.markdown("### 💡 요리 팁")
        for tip in recipe["tips"]:
            st.write("• " + str(tip))
    st.warning("AI가 생성한 레시피는 참고용입니다. 재료의 신선도와 제품별 염도, 화력에 따라 간과 조리 시간을 조절하고 고기·생선·달걀은 속까지 충분히 익혀 주세요.")


# 첫 화면과 두 가지 기능을 세션 상태로 전환합니다.
if "app_page" not in st.session_state:
    st.session_state.app_page = "home"

if st.session_state.app_page == "home":
    st.markdown("<div class='section-title'>원하는 서비스를 선택해 주세요</div>", unsafe_allow_html=True)
    st.caption("이용할 기능을 선택해 주세요.")
    st.write("")

    # HTML 줄바꿈 태그를 사용해 카드 안의 아이콘/제목/설명을 세로로 배치합니다.
    left, right = st.columns(2, gap="large")
    with left:
        fridge_card_label = "🥬<br><br>**재료 관리 / 메뉴 추천**<br><br>냉장고 재료와 유통기한을 관리하고<br>보유한 재료로 만들 수 있는 메뉴 찾기"
        if st.button(
            fridge_card_label,
            key="home_fridge_card",
            use_container_width=True,
            type="secondary",
        ):
            st.session_state.app_page = "fridge"
            st.rerun()

    with right:
        recipe_card_label = "🍳<br><br>**원하는 메뉴 레시피**<br><br>먹고 싶은 메뉴 이름을 입력하고<br>AI가 만드는 상세 레시피 확인하기"
        if st.button(
            recipe_card_label,
            key="home_custom_recipe_card",
            use_container_width=True,
            type="secondary",
        ):
            st.session_state.app_page = "custom_recipe"
            st.rerun()

    st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            width: 100%;
            min-height: 245px;
            white-space: normal;
            text-align: center;
            justify-content: center;
            align-items: center;
            display: flex;
            border: 1px solid #d9e2d8;
            border-radius: 24px;
            background: #f7faf5;
            color: #244b35;
            padding: 30px 24px;
            font-size: 17px;
            font-weight: 400;
            line-height: 1.8;
            box-shadow: none;
            transition: background 0.15s ease, border-color 0.15s ease;
        }
        div[data-testid="stButton"] > button p {
            margin: 0;
            text-align: center;
            width: 100%;
        }
        div[data-testid="stButton"] > button strong {
            font-size: 21px;
            font-weight: 700;
        }
        div[data-testid="stButton"] > button:hover {
            border-color: #39734f;
            background: #edf5ec;
            color: #183d29;
        }
        div[data-testid="stButton"] > button:focus:not(:active) {
            border-color: #39734f;
            color: #183d29;
            box-shadow: 0 0 0 1px #39734f;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

elif st.session_state.app_page == "custom_recipe":
    if st.button("← 첫 화면으로", key="back_from_recipe"):
        st.session_state.app_page = "home"
        st.rerun()
    st.markdown("<div class='section-title'>원하는 메뉴 레시피</div>", unsafe_allow_html=True)
    st.caption("먹고 싶은 메뉴를 입력하면 1~2인분 기준의 상세 레시피를 만들어 드립니다.")
    with st.form("custom_recipe_form"):
        menu_name = st.text_input("만들고 싶은 메뉴", placeholder="예: 제육볶음, 크림파스타, 김치찌개")
        submitted_recipe = st.form_submit_button("레시피 만들기", type="primary", use_container_width=True)
    if submitted_recipe:
        if not menu_name.strip():
            st.warning("메뉴 이름을 먼저 입력해 주세요.")
        else:
            with st.spinner(f"'{menu_name.strip()}' 레시피를 만들고 있어요..."):
                try:
                    st.session_state.generated_recipe = generate_custom_recipe(menu_name.strip())
                    st.session_state.generated_recipe_query = menu_name.strip()
                except Exception as exc:
                    error_text = str(exc)
                    if "API 키가 설정" in error_text:
                        st.error(error_text)
                    else:
                        st.error("레시피를 생성하지 못했어요. API 키, 인터넷 연결 또는 Gemini 사용량을 확인한 뒤 다시 시도해 주세요.")
                        st.error(f"상세 오류: {error_text[:800]}")
    if st.session_state.get("generated_recipe"):
        st.divider()
        show_custom_recipe(st.session_state.generated_recipe)

elif st.session_state.app_page == "fridge":
    if st.button("← 첫 화면으로", key="back_from_fridge"):
        st.session_state.app_page = "home"
        st.rerun()

    items = load_data()
    tab1, tab2 = st.tabs(["식재료 관리", "메뉴 추천"])

    with tab1:
        st.markdown("<div class='section-title'>식재료 관리</div>", unsafe_allow_html=True)
        st.caption("보유한 재료와 유통기한을 한눈에 관리해요.")
        with st.form("add_ingredient", clear_on_submit=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                new_name = st.text_input("식재료 이름", placeholder="예: 계란")
            with c2:
                quantity = st.text_input("수량", placeholder="예: 3개")
            with c3:
                expiry = st.date_input("유통기한", value=date.today() + timedelta(days=7))
            submitted = st.form_submit_button("재료 추가")
            if submitted:
                if not new_name.strip():
                    st.warning("식재료 이름을 입력해 주세요.")
                elif any(normalize_name(x["name"]) == normalize_name(new_name) for x in items):
                    st.warning("이미 등록된 재료입니다. 기존 항목을 삭제한 뒤 다시 등록해 주세요.")
                else:
                    items.append({"name": new_name.strip(), "quantity": quantity.strip() or "미입력", "expiry": expiry.isoformat()})
                    save_data(items)
                    st.success(f"{new_name.strip()} 등록 완료!")
                    st.rerun()

        st.markdown("<div class='section-title'>내 냉장고 목록</div>", unsafe_allow_html=True)
        if not items:
            st.info("아직 등록된 재료가 없습니다. 위에서 재료를 추가해 보세요.")
        else:
            today = date.today()
            for idx, item in enumerate(items):
                try:
                    exp = date.fromisoformat(item.get("expiry", (today + timedelta(days=7)).isoformat()))
                except (ValueError, TypeError):
                    exp = today + timedelta(days=7)
                days_left = (exp - today).days
                col1, col2, col3, col4 = st.columns([2, 1, 1.5, 1])
                col1.write(f"**{item['name']}**")
                col2.write(item.get("quantity", "미입력"))
                col3.write(f"유통기한: {exp.isoformat()}")
                if days_left < 0:
                    col3.error(f"{abs(days_left)}일 지남")
                elif days_left <= 3:
                    col3.warning(f"{days_left}일 남음")
                else:
                    col3.caption(f"{days_left}일 남음")
                if col4.button("삭제", key=f"delete_{idx}"):
                    items.pop(idx)
                    save_data(items)
                    st.rerun()
            st.caption("※ 유통기한은 사용자가 입력한 날짜를 기준으로 표시합니다. 실제 섭취 전에는 보관 상태와 식품 상태도 확인하세요.")

    with tab2:
        st.markdown("<div class='section-title'>보유 재료로 메뉴 추천</div>", unsafe_allow_html=True)
        st.caption("등록한 재료를 기준으로 만들 수 있는 메뉴를 자동으로 추천합니다. 재료를 추가하거나 삭제하면 추천도 함께 바뀝니다.")
        available_items = ingredient_names(items)
        if not available_items:
            st.info("먼저 '재료 관리' 탭에서 식재료를 등록해 주세요.")
        else:
            scored_recipes = []
            today = date.today()
            expiring_names = set()
            for item in items:
                try:
                    days_left = (date.fromisoformat(item.get("expiry", "")) - today).days
                    if days_left <= 3:
                        expiring_names.add(normalize_name(item["name"]))
                except (ValueError, TypeError):
                    pass
            for recipe in RECIPES:
                score, matched, missing = recipe_score(recipe, available_items)
                if matched:
                    urgent_matches = sum(1 for name in matched if normalize_name(name) in expiring_names)
                    scored_recipes.append((urgent_matches, score, len(matched), recipe, matched, missing))
            scored_recipes.sort(key=lambda row: (row[0], row[1], row[2]), reverse=True)
            if not scored_recipes:
                st.warning("등록한 재료를 활용하는 레시피가 아직 없습니다. 닭가슴살, 파스타면, 참치, 계란, 두부, 김치, 햄, 만두 등 자취생 기본 재료를 등록해 보세요.")
            else:
                st.success(f"현재 보유 재료 {len(available_items)}개를 확인했어요. 보유 재료를 많이 활용하는 메뉴부터 보여드릴게요.")
                for urgent_matches, score, matched_count, recipe, matched, missing in scored_recipes[:15]:
                    with st.container(border=True):
                        left, right = st.columns([4, 1])
                        with left:
                            st.markdown(f"### 🍽️ {recipe['name']}")
                            st.write(f"재료 일치율 **{round(score * 100)}%** · 조리 시간 약 {recipe['time']}분 · 난이도 {recipe['difficulty']}")
                            st.write("**보유 재료 중 사용 가능:** " + ", ".join(matched))
                            urgent_used = [name for name in matched if normalize_name(name) in expiring_names]
                            if urgent_used:
                                st.warning("유통기한이 임박한 재료 포함: " + ", ".join(urgent_used))
                            extras = missing + recipe.get("extra", [])
                            st.write("**추가로 필요한 재료:** " + (", ".join(extras) if extras else "없음"))
                        with right:
                            st.metric("재료 일치율", f"{round(score * 100)}%")
                        with st.expander("상세 레시피 보기", expanded=False):
                            st.markdown("**준비 재료 (1~2인분 기준)**")
                            for ingredient in recipe["ingredients"]:
                                st.write(f"• {ingredient}: **{ingredient_amount(ingredient, recipe['name'])}**")
                            if recipe.get("extra"):
                                st.markdown("**추가 재료·양념**")
                                for extra in recipe["extra"]:
                                    st.write(f"• {extra}: **{extra_amount(extra, recipe['name'])}**")
                            water_note = recipe_water_note(recipe)
                            if water_note:
                                st.info("💧 물 조절 팁: " + water_note)
                            st.markdown("**조리 순서**")
                            for step_no, step in enumerate(recipe["steps"], 1):
                                heat, duration, tip = cooking_guide(recipe, step, step_no - 1)
                                st.markdown(f"**{step_no}단계. {step}**")
                                info1, info2 = st.columns(2)
                                info1.caption(f"🔥 불 세기: {heat}")
                                info2.caption(f"⏱️ 예상 시간: {duration}")
                                st.caption(f"조리 팁: {tip}")
                            st.info("계량은 1~2인분 기준의 가정용 조리 예시입니다. 재료 크기·제품 염도·화력에 따라 달라질 수 있으니 간은 조금씩 조절하세요. 고기와 닭고기는 속까지 완전히 익혀 드세요.")

st.divider()
st.caption("오늘의 냉장고 · 식재료를 알뜰하게 활용하는 나만의 주방 도우미")
