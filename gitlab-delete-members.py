#!/usr/bin/env python3

"""Handy script for searching and deleting members from Gitlab projects.
Built on top of GitLab Python API: https://python-gitlab.readthedocs.io/
"""

import argparse
import gitlab


def parse_args():
    parser = argparse.ArgumentParser(
        description='Delete member from all accessible gitlab projects.')
    parser.add_argument('--query', required=True,
                        help='Gitlab query string that defines users '
                        'to be deleted (username is recommended)')
    parser.add_argument('--token', required=True,
                        help='Gitlab token of your user')
    parser.add_argument('--url', default='https://gitlab.com',
                        help='Gitlab URL')
    parser.add_argument('--visibility', default='private',
                        help='Gitlab projects visibility')
    parser.add_argument('--dry', action='store_true',
                        help='dry run')
    return parser.parse_args()


def main():
    # Greeting and args parsing.
    args = parse_args()

    # Initialize Gitlab API.
    print(f'Auth at {args.url}')
    gl = gitlab.Gitlab(args.url, private_token=args.token)
    gl.auth()

    # Iterate over projects.
    projects = gl.projects.list(all=True, visibility=args.visibility)
    groups = gl.groups.list(all=True, visibility=args.visibility)

    del_members_projects_count = 0
    del_members_groups_count = 0
    del_projects_count = 0
    del_groups_count = 0

    for p in projects:
        print(f'Project "{p.name_with_namespace}" (id={p.id}) :',
              end='')

        # Query members.
        members = p.members.list(query=args.query)

        # Delete members.
        if len(members) == 0:
            print(' no users to delete', end='')
        else:
            del_projects_count += 1
            for m in members:
                print(f' delete {m.username} (id={m.id})', end='')
                del_members_projects_count += 1
                if not args.dry:
                    try:
                        m.delete()
                        pass
                    except:
                        print(" / ! Error occured but probably nothing to worry about...")
        print()

    for g in groups:
        print(f'Group "{g.name}" (id={g.id}) :',
              end='')

        # Query members.
        members = g.members.all(query=args.query, all=True)

        # Delete members.
        if len(members) == 0:
            print(' no users to delete', end='')
        else:
            del_groups_count += 1
            for m in members:
                print(f' delete {m.username} (id={m.id})', end='')
                del_members_groups_count += 1
                if not args.dry:
                    try:
                        m.delete()
                        pass
                    except:
                        print(" / ! Error occured but probably nothing to worry about...")
        print()

    # Statistics.
    print(f'{del_members_projects_count} members deleted '
          f'in {del_projects_count} repositories')
          
    print(f'{del_members_groups_count} members deleted '
          f'in {del_groups_count} groups')


if __name__ == '__main__':
    main()
