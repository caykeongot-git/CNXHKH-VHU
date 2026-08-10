import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def normalize(text):
    text = text.lower()
    text = re.sub(r'[\.\:\,\;\-\?\!\(\)\"\'\“\”\s]+', ' ', text).strip()
    return text

def get_keywords(text):
    words = normalize(text).split()
    stop_words = {'là', 'của', 'trong', 'về', 'có', 'được', 'cho', 'và', 'nào', 'gì', 'thế', 'này', 'đó', 'các', 'những', 'một', 'để', 'ở', 'khi', 'với', 'như', 'bởi', 'do', 'theo', 'hãy', 'cho', 'biết'}
    return set(w for w in words if w not in stop_words and len(w) > 1)

def main():
    json_path = 'data/cnxhkh_vhu.json'
    # Reload from original docx if build_data.py can be run or parse current json
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    raw_questions = data.get('questions', [])
    print(f"Original total questions: {len(raw_questions)}")

    clean_questions = []
    removed_count = 0

    for q in raw_questions:
        q_text = q['question']
        q_keys = get_keywords(q_text)
        
        is_dup = False
        for u in clean_questions:
            u_text = u['question']
            u_keys = get_keywords(u_text)
            
            if not q_keys or not u_keys:
                continue
                
            intersection = len(q_keys & u_keys)
            union = len(q_keys | u_keys)
            jaccard = intersection / float(union)
            
            norm_q = normalize(q_text)
            norm_u = normalize(u_text)
            
            # High similarity or substring match
            if jaccard >= 0.62 or (norm_q in norm_u or norm_u in norm_q) and intersection >= min(len(q_keys), len(u_keys)) * 0.75:
                is_dup = True
                print(f"Removing duplicate Q{q['id']}: '{q_text[:60]}...' (Matches Q{u['id']})")
                break
                    
        if not is_dup:
            clean_questions.append(q)

    # Re-index IDs 1..N
    for idx, item in enumerate(clean_questions):
        item['id'] = idx + 1

    print(f"Clean unique questions: {len(clean_questions)} (Removed {len(raw_questions) - len(clean_questions)} duplicates)")

    data['total_questions'] = len(clean_questions)
    data['subject_name'] = f"CNXHKH - VHU ({len(clean_questions)} Câu)"
    data['chapter_title'] = f"Bộ {len(clean_questions)} câu trắc nghiệm tổng hợp VHU (Đã làm sạch câu trùng)"
    data['questions'] = clean_questions

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {json_path} with {len(clean_questions)} deduplicated questions.")

    manifest_json = {
        "subjects": [
            {
                "id": "cnxhkh_vhu",
                "name": f"Chủ nghĩa xã hội khoa học - VHU ({len(clean_questions)} Câu)",
                "chapters": [
                    { "id": "c_all", "title": f"Bộ {len(clean_questions)} câu tổng hợp chuẩn", "file": "data/cnxhkh_vhu.json" }
                ]
            }
        ]
    }

    with open('data/manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest_json, f, ensure_ascii=False, indent=2)

    print("Updated data/manifest.json successfully.")

if __name__ == '__main__':
    main()
