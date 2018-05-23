from bulkeditor import BulkEditor
from config import testMode, testRepoName

# Main code
bulkEditor = BulkEditor()

# select repo
for repo in bulkEditor.get_repos():
   if (testMode):
       if (not repo.full_name == testRepoName):
           continue
   print(repo.full_name)

   # turn off branch protection if already enabled to commit our templates
   bulkEditor.disable_branch_protection(repo)

   # check if files exist
   #  add file if not
   #  commit to master
   bulkEditor.upload_templates(repo)

   # turn on branch protection
   bulkEditor.enable_branch_protection(repo)

   # set repo settings
   repo.edit(has_issues=False)
   repo.edit(has_wiki=False)
   repo.edit(has_projects=False)
   repo.edit(allow_squash_merge=True)
   repo.edit(allow_merge_commit=False)
   repo.edit(allow_rebase_merge=False)
