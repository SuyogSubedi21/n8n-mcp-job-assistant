import re
from difflib import SequenceMatcher


def normalise(text):
    return re.sub(r"[^a-z0-9+#/ ]", " ", text.lower())


def skill_in_cv(skill, cv_text, threshold=0.85):
    skill = normalise(skill).strip()
    cv = normalise(cv_text)
    if not skill:
        return False
    if skill in cv:
        return True
    words = cv.split()
    size = len(skill.split())
    for i in range(len(words) - size + 1):
        chunk = " ".join(words[i:i + size])
        if SequenceMatcher(None, skill, chunk).ratio() >= threshold:
            return True
    return False


def check_fit(cv_text, required_skills, required_years=0, candidate_years=0):
    skills = [s.strip() for s in required_skills if s.strip()]
    if not skills:
        return {"score": 0, "matched": [], "missing": [], "note": "No skills given"}

    matched = [s for s in skills if skill_in_cv(s, cv_text)]
    missing = [s for s in skills if s not in matched]
    skill_score = round(len(matched) / len(skills) * 100)

    if required_years <= 0:
        exp_score = 100
        exp_note = "No experience requirement found"
    else:
        exp_score = round(min(candidate_years / required_years, 1) * 100)
        gap = max(required_years - candidate_years, 0)
        exp_note = "Meets the requirement" if gap == 0 else f"Short by {gap} year(s)"

    score = round(skill_score * 0.7 + exp_score * 0.3)
    return {
        "score": score,
        "skill_score": skill_score,
        "experience_score": exp_score,
        "experience_note": exp_note,
        "matched": matched,
        "missing": missing,
    }