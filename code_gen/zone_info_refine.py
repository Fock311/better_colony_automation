#!/usr/bin/env python3
"""
按 icon 分组 zones_info.yaml 中的条目，输出 icons_info 格式的 YAML。
用法：
  python group_zones_by_icon.py            # 读取 zones_info.yaml，写入 zones_by_icon.yaml
  python group_zones_by_icon.py -i in.yaml -o out.yaml
"""
import argparse
import sys
import os
import yaml


def group_zones(zones_list):
    order = []
    groups = {}
    for item in zones_list:
        zid = item.get('id') or item.get('zone') or ''
        icon = (item.get('icon') or '').strip()
        if icon not in groups:
            groups[icon] = []
            order.append(icon)
        if zid and zid not in groups[icon]:
            groups[icon].append(zid)
    #using first zone as type:e.g. first zone is 'zone_urban' then type is 'urban'

    return [{'icon': ic,
             'zones': groups[ic],
             'type': str(ic).replace('GFX_district_specialization_', '')
             }
            for ic in order]

def main():
    input_default = 'zone_icon_list.yaml'
    merge = 'manual_config/zone_type_fitness.yaml'
    output_default = '../gui_generate/config/zone_config.yaml'

    with open(input_default, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}

    with open(merge, 'r', encoding='utf-8') as f:
        zone_type_fitness_data = yaml.safe_load(f) or {}

    zone_type_fitness = zone_type_fitness_data.get('zone_type_fitness')
    zone_type_fitness_map = {item['type']: item for item in zone_type_fitness}

    zones = data.get('zone_icon_list')
    grouped = {'icons_info': group_zones(zones)}
    group_to_remove = []
    # adding fitness_trigger(optional) and fitness(optional) to each group if no key raise error
    for group in grouped['icons_info']:
        type_ = group['type']
        fitness_info = zone_type_fitness_map.get(type_)
        if fitness_info:
            if fitness_info.get('fitness_trigger'):
                group['fitness_trigger'] = fitness_info.get('fitness_trigger')
            if fitness_info.get('fitness'):
                group['fitness'] = fitness_info.get('fitness')
        else:
            print(f"Warning: No fitness info found for type '{type_}'")
            #remove group if no fitness info
            group_to_remove.append(group)
    for group in group_to_remove:
        grouped['icons_info'].remove(group)

    # reorder grouped['icons_info'] according to zone_type_fitness type order
    type_order = [item['type'] for item in zone_type_fitness]
    grouped['icons_info'].sort(key=lambda x: type_order.index(x['type']) if x['type'] in type_order else len(type_order))

    # rename icons_info as zones_info
    grouped['zones_info'] = grouped.pop('icons_info')

    with open(output_default, 'w', encoding='utf-8') as f:
        yaml.safe_dump(grouped, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

    print(f"Wrote {len(grouped['zones_info'])} groups to {output_default}")

if __name__ == '__main__':
    main()