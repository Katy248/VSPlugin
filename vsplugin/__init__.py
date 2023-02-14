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
			# select created folder
			effective_url = normalize(dir_url)
			select = relpath(effective_url, base_url).split('/')[0]
			if select != '..':
				try:
					self.pane.place_cursor_at(join(base_url, select))
				except ValueError as dir_disappeared:
					pass
class AddFile(DirectoryPaneCommand):
	aliases = (
		'Add file', 'New file', 'Create file', 'Touch file', 'Touch'
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
			# select created file
			effective_url = normalize(file_url)
			select = relpath(effective_url, base_url).split('/')[0]
			if select != '..':
				try:
					self.pane.place_cursor_at(join(base_url, select))
				except ValueError as dir_disappeared:
					pass