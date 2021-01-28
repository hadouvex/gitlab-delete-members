# gitlab-tools

Handy scripts for automating typical operations in Gitlab.
Built on top of GitLab Python API: https://python-gitlab.readthedocs.io/


## gitlab-delete-members.py

### Usage:

```
gitlab-delete-members.py [-h] --query QUERY --token TOKEN [--url URL]
                         [--visibility VISIBILITY] [--dry]

Delete member from all accessible gitlab projects.

optional arguments:
  -h, --help            show this help message and exit
  --query QUERY         Gitlab query string that defines users to be deleted
                        (username is recommended)
  --token TOKEN         Gitlab token of your user
  --url URL             Gitlab URL
  --visibility VISIBILITY
                        Gitlab projects visibility
  --dry                 dry run
```


### Example

You gitlab token is `Abcdefg123`. You want to delete user with username `johndoe123` from all accessible private projects:

```
$ gitlab-delete-members.py --query johndoe123 --token Abcdefg123
Auth at https://gitlab.com
Project "MyGroupSpam / my-project-foo" (id=11111111) : no users to delete
Project "MyGroupSpam / my-project-bar" (id=11111112) : delete johndoe123 (id=3333333)
Project "MyGroupEggs / my-project-baz" (id=11111113) : delete johndoe123 (id=3333333)
2 members deleted in 2 repositories
```

### Dry run

If you are worried about which projects will be affected, you can use `--dry` option. This option enables "dry run". I.e. no actual delete action will be performed.
