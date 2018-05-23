from bulkeditor import BulkEditor

bulkEditor = BulkEditor()

print("The following repos are not private:")
# select repo
for repo in bulkEditor.get_repos():
   if (not repo.private):
      print(repo.full_name)

      # set repo settings
      # repo.edit(private=True)
