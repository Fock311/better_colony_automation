import io
import os

files = [
    ("localisation/simp_chinese/bt_main_3_l_simp_chinese.yml",
     "localisation/english/bt_main_3_l_english.yml",
     "localisation/japanese/bt_main_3_l_japanese.yml"),
    ("localisation/simp_chinese/bca_intro_l_simp_chinese.yml",
     "localisation/english/bca_intro_l_english.yml",
     "localisation/japanese/bca_intro_l_japanese.yml"),
    ("localisation/simp_chinese/bca_gui_l_simp_chinese.yml",
        "localisation/english/bca_gui_l_english.yml",
        "localisation/japanese/bca_gui_l_japanese.yml"),
]

root = os.path.dirname(os.path.dirname(__file__))


def read_keys(path):
    p = os.path.join(root, path.replace('/', os.sep))
    if not os.path.exists(p):
        return None, f"MISSING_FILE: {path}"
    with io.open(p, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    keys = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s.startswith('#') or s.startswith('//'):
            continue
        # ignore header like l_simp_chinese:
        if s.endswith(':') and s.split(':')[0].startswith('l_') and len(s.split())==1:
            continue
        # find first colon
        if ':' in s:
            # but avoid lines where colon is inside value? key is before first colon
            key = s.split(':', 1)[0].strip()
            # skip if key seems to be a single quote or value continuation
            if key:
                keys.append(key)
    return set(keys), None


total_cn = 0
missing_report = {}
for cn, en, jp in files:
    cn_keys, err = read_keys(cn)
    if cn_keys is None:
        print(err)
        continue
    en_keys, err_en = read_keys(en)
    jp_keys, err_jp = read_keys(jp)
    missing_en = sorted(list(cn_keys - (en_keys or set())))
    missing_jp = sorted(list(cn_keys - (jp_keys or set())))
    missing_report[cn] = {
        'english_missing_count': len(missing_en),
        'japanese_missing_count': len(missing_jp),
        'english_missing': missing_en,
        'japanese_missing': missing_jp,
        'english_file_missing': en_keys is None,
        'japanese_file_missing': jp_keys is None,
    }
    total_cn += len(cn_keys)

# print human readable
for cn_path, data in missing_report.items():
    print('FILE:', cn_path)
    if data['english_file_missing']:
        print('  English file missing entirely')
    else:
        print('  Missing in English:', data['english_missing_count'])
        for k in data['english_missing']:
            print('    ', k)
    if data['japanese_file_missing']:
        print('  Japanese file missing entirely')
    else:
        print('  Missing in Japanese:', data['japanese_missing_count'])
        for k in data['japanese_missing']:
            print('    ', k)
    print()

# summary
total_missing_en = sum(d['english_missing_count'] for d in missing_report.values())
total_missing_jp = sum(d['japanese_missing_count'] for d in missing_report.values())
print('SUMMARY: total chinese keys scanned (approx):', total_cn)
print('SUMMARY: total missing in English:', total_missing_en)
print('SUMMARY: total missing in Japanese:', total_missing_jp)

