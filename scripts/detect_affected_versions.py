#!/usr/bin/env python3

import oyaml as yaml

import argparse
import os
import subprocess
import sys

VERSION_KEY = "hive.openshift.io/version-major-minor"
CONFIG_FILENAME = "config.yaml"
DEPLOY_DIR = "deploy"

SUPPORTED_VERSIONS = ["4.16", "4.18", "4.19", "4.20", "4.21"]


def parse_version(version_str):
    parts = version_str.split(".")
    return tuple(int(p) for p in parts)


def get_changed_files(base_ref):
    result = subprocess.run(
        ["git", "diff", "--name-only", base_ref],
        capture_output=True,
        text=True,
        check=True,
    )
    return [f for f in result.stdout.strip().splitlines() if f]


def find_config_dir(filepath, repo_root):
    dirpath = os.path.dirname(filepath)
    while dirpath and dirpath.startswith(DEPLOY_DIR):
        config_path = os.path.join(repo_root, dirpath, CONFIG_FILENAME)
        if os.path.exists(config_path):
            return dirpath
        parent = os.path.dirname(dirpath)
        if parent == dirpath:
            break
        dirpath = parent
    return None


def get_changed_deploy_dirs(changed_files, repo_root):
    deploy_dirs = set()
    for filepath in changed_files:
        if not filepath.startswith(DEPLOY_DIR + "/"):
            continue
        config_dir = find_config_dir(filepath, repo_root)
        if config_dir:
            deploy_dirs.add(config_dir)
    return sorted(deploy_dirs)


def extract_versions_from_config(config_path, all_versions):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    if not config:
        return set()

    if config.get("deploymentMode") == "Policy":
        return set()

    sss = config.get("selectorSyncSet")
    if not sss:
        return set()

    for expr in sss.get("matchExpressions", []):
        if expr.get("key") != VERSION_KEY:
            continue

        operator = expr.get("operator", "")
        values = [str(v) for v in expr.get("values", [])]

        if operator == "In":
            return set(values)
        elif operator == "NotIn":
            return set(all_versions) - set(values)

    return set(all_versions)


def main():
    parser = argparse.ArgumentParser(
        description="Detect the latest OpenShift version affected by changes in a managed-cluster-config PR"
    )
    parser.add_argument(
        "--base-ref",
        "-b",
        default=os.environ.get("PULL_BASE_SHA", "master"),
        help="Base git ref to diff against (default: PULL_BASE_SHA env var or master)",
    )
    parser.add_argument(
        "--repo-root",
        "-r",
        default=".",
        help="Root of the managed-cluster-config repo (default: .)",
    )
    args = parser.parse_args()

    all_versions = sorted(SUPPORTED_VERSIONS, key=parse_version)
    changed_files = get_changed_files(args.base_ref)
    changed_deploy_dirs = get_changed_deploy_dirs(changed_files, args.repo_root)

    affected = set()
    for d in changed_deploy_dirs:
        config_path = os.path.join(args.repo_root, d, CONFIG_FILENAME)
        versions = extract_versions_from_config(config_path, all_versions) & set(all_versions)
        affected.update(versions)

    if affected:
        print(sorted(affected, key=parse_version)[-1])
    else:
        print("nil")


if __name__ == "__main__":
    main()
