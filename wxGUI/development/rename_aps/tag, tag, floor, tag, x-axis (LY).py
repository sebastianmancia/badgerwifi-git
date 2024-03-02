# tag, tag, floor, tag, x-axis (LY).py

from pathlib import Path

from common import load_json
from common import create_floor_plans_dict

from common import save_and_move_json
from common import re_bundle_project


def create_tag_keys_dict(tag_keys_json):
    """Create a dictionary of tag keys."""
    tag_keys_dict = {}
    for tagKey in tag_keys_json['tagKeys']:
        tag_keys_dict[tagKey['key']] = tagKey['id']
    return tag_keys_dict


def sort_tag_value_getter(tags_list, sort_tag_key, tag_keys_dict):
    """Retrieve the value of a specific tag for sorting purposes."""
    undefined_tag_value = '-   ***   TagValue is empty   ***   -'
    missing_tag_key = 'Z'
    sort_tag_unique_id = tag_keys_dict.get(sort_tag_key)
    if sort_tag_unique_id is None:
        return missing_tag_key
    for value in tags_list:
        if value.get('tagKeyId') == sort_tag_unique_id:
            tag_value = value.get('value')
            if tag_value is None:
                return undefined_tag_value
            return tag_value
    return missing_tag_key


def sort_access_points(access_points, tag_keys_dict, floor_plans_dict):
    """Sort access points based on various criteria."""
    return sorted(access_points,
                  key=lambda ap: (
                      sort_tag_value_getter(ap.get('tags', []), 'UNIT', tag_keys_dict),
                      sort_tag_value_getter(ap.get('tags', []), 'building-group', tag_keys_dict),
                      floor_plans_dict.get(ap['location'].get('floorPlanId', 'missing_floorPlanId')),
                      sort_tag_value_getter(ap.get('tags', []), 'sequence-override', tag_keys_dict),
                      ap['location']['coord']['x']
                  ))


def rename_access_points(access_points, tag_keys_dict, floor_plans_dict, message_callback):
    """Rename access points based on sorting and specific naming conventions."""
    ap_sequence_number = 1
    for ap in access_points:
        new_ap_name = f"{sort_tag_value_getter(ap['tags'], 'UNIT', tag_keys_dict)}-AP{ap_sequence_number:03}"

        message_callback(
            f"{ap['name']} {ap['model']} from: {floor_plans_dict.get(ap['location']['floorPlanId'])} renamed to {new_ap_name}")

        ap['name'] = new_ap_name
        ap_sequence_number += 1


def run(working_directory, project_name, message_callback):
    project_dir = Path(working_directory) / project_name

    # Load JSON data
    floor_plans_json = load_json(project_dir, 'floorPlans.json', message_callback)
    access_points_json = load_json(project_dir, 'accessPoints.json', message_callback)
    tag_keys_json = load_json(project_dir, 'tagKeys.json', message_callback)

    # Process data
    floor_plans_dict = create_floor_plans_dict(floor_plans_json)
    tag_keys_dict = create_tag_keys_dict(tag_keys_json)

    # Sort Access Points
    sorted_access_points = sort_access_points(access_points_json['accessPoints'], tag_keys_dict, floor_plans_dict)

    # Rename Access Points
    rename_access_points(sorted_access_points, tag_keys_dict, floor_plans_dict, message_callback)

    # Save and Move the Updated JSON
    updated_access_points_json = {'accessPoints': sorted_access_points}
    save_and_move_json(updated_access_points_json, project_dir / 'accessPoints.json')

    # Re-bundle into .esx File
    re_bundle_project(project_dir, f"{project_name}_re-zip")

    message_callback(f"\nProcess complete\n{project_name}_re-zip re-bundled into .esx file")
