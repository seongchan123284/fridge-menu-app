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
                items.append({
                    "name": new_name.strip(),
                    "quantity": quantity.strip() or "미입력",
                    "expiry": expiry.isoformat(),
                })
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

    if items:
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
                        st.markdown(f"**준비 재료:** {', '.join(recipe['ingredients'])}")
                        if recipe.get("extra"):
                            st.markdown(f"**추가 재료·선택 양념:** {', '.join(recipe['extra'])}")
                        st.markdown("**조리 순서**")
                        for step_no, step in enumerate(recipe["steps"], 1):
                            heat, duration, tip = cooking_guide(recipe, step, step_no - 1)
                            st.markdown(f"**{step_no}단계. {step}**")
                            info1, info2 = st.columns(2)
                            info1.caption(f"🔥 불 세기: {heat}")
                            info2.caption(f"⏱️ 예상 시간: {duration}")
                            st.caption(f"조리 팁: {tip}")
                        st.info("조리 시간과 불 세기는 가정용 화력과 재료의 양·두께에 따라 달라질 수 있습니다. 특히 고기와 닭고기는 속까지 완전히 익었는지 확인하세요.")


st.divider()
st.caption("오늘의 냉장고 · 식재료를 알뜰하게 활용하는 나만의 주방 도우미")
