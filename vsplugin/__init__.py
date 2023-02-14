from fman import ( 
	DirectoryPaneCommand, show_alert, show_prompt, show_status_message
)
from fman.fs import makedirs, touch
from fman.url import normalize, relpath, join
from os.path import basename, pardir

class AddFolder(DirectoryPaneCommand):
	aliases = (
		'Add folder', 'New folder', 'Create folder', 'Add directory', 'New directory', 'Create directory'
	)
	def __call__(self):
		name, ok = show_prompt("New folder (directory)", "")
		if ok and name:
			# Support recursive creation of directories:
			base_url = self.pane.get_path()
			dir_url = join(base_url, name)
			try:
				makedirs(dir_url)
				show_status_message(f'Added new folder "{name}".', 2)
			except NotImplementedError :
				show_alert("A file with this name already exists!")
			# Use normalize(...) instead of resolve(...) to avoid the following
			# problem: Say c/ is a symlink to a/b/. We're inside c/ and create
			# d. Then # resolve(c/d) would give a/b/d and the relative path
			# further down # would be ../a/b/d. We could not place the cursor at
			# that. If on # the other hand, we use normalize(...), then we
			# compute the relpath from c -> c/d, which does work.
			effective_url = normalize(dir_url)
			select = relpath(effective_url, base_url).split('/')[0]
			if select != '..':
				try:
					self.pane.place_cursor_at(join(base_url, select))
				except ValueError as dir_disappeared:
					pass
class AddFile(DirectoryPaneCommand):
	aliases = (
		'Add folder', 'New folder', 'Create folder', 'Add directory', 'New directory', 'Create directory'
	)
	def __call__(self):
		name, ok = show_prompt("New file", "")
		if ok and name:
			# Support recursive creation of directories:
			base_url = self.pane.get_path()
			file_url = join(base_url, name)
			try:
				touch(file_url)
				show_status_message(f'Added new file "{name}".', 2)
			except FileExistsError:
				show_alert("A file with this name already exists!")
			# Use normalize(...) instead of resolve(...) to avoid the following
			# problem: Say c/ is a symlink to a/b/. We're inside c/ and create
			# d. Then # resolve(c/d) would give a/b/d and the relative path
			# further down # would be ../a/b/d. We could not place the cursor at
			# that. If on # the other hand, we use normalize(...), then we
			# compute the relpath from c -> c/d, which does work.
			effective_url = normalize(file_url)
			select = relpath(effective_url, base_url).split('/')[0]
			if select != '..':
				try:
					self.pane.place_cursor_at(join(base_url, select))
				except ValueError as dir_disappeared:
					pass