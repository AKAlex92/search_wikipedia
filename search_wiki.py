import sys, os
import wikipedia
import urllib.request
from urllib.parse import urlparse

def draw_input(text, options):
	while True:
		choice = input(text)
		# if str.upper(choice) in map(str.upper, options):  # Case insensitive check (slower)
		if choice.upper() in (o.upper() for o in options): # Case insensitive check (faster???)
			break

	return choice

def draw_menu(options):
	while True:
		error = False
		print("***\t***\t***\t***\t***\t***\t***\t***\t***\t")
		i = 0
		mm = len(options)
		for opt in options:
			print("%d)\t%s" % (i, opt))
			i+=1
		print("***\t***\t***\t***\t***\t***\t***\t***\t***\t")
		choice = input("Select the option [0 - " + str(mm - 1) + ", q = quit]:\t")
		if choice == "q":
			sys.exit(1)

		try:
			intchoice = int(choice)
		except ValueError as e:
			error = True
			print("Characters are not a valid input")
		if error is False:
			if 0 <= intchoice <= mm - 1:
				break
			else:
				error = True
				print("Not a valid input, please select an option between 0 and %s" % str(mm - 1))
	return intchoice

def get_summary(searched_text):
	try:
		out = wikipedia.summary(searched_text)
	except wikipedia.exceptions.PageError as e:
		print(e)
		main() # Restart the script
	except wikipedia.exceptions.DisambiguationError as e:
		which_one = draw_menu(e.options)
		print(e.options[which_one])
		out = get_summary(e.options[which_one])
	return out

def get_page_info(searched_text, out_type = "fullpage"):
	out = ""
	info = wikipedia.page(searched_text)
	if out_type == "fullpage":
		out = info.content
	elif out_type == "fullpagehtml":
		out = info.html()
	elif out_type == "getimageslink":
		out = info.images
	elif out_type == "getpageurl":
		out = info.url
	elif out_type == "getpagetitle":
		out = info.title

	return out
"""
def get_fullpage(page_obj):
	out = page_obj.content
	return out
"""
def download_from_links(arr_files, path = "."):
	if os.path.isdir(path) is False:
		print("Creating directory %s" % path)
		# define the access rights
		access_rights = 0o755
		try:
			os.mkdir(path, access_rights)
		except OSError:
			raise Exception ("Creation of the directory %s failed" % path)
		else:
			print ("Successfully created the directory %s" % path)

	for link in arr_files:
		url_obj = urlparse(link)
		filename = os.path.basename(url_obj.path) # get filename from path of the remote file
		urllib.request.urlretrieve(link, path + "/" + filename)


def main():
	wikipedia.set_lang("it")
	max_search_results = 3
	search_choices = list(["Summary", "Full Page", "Full Page in HTML", "Get Images Link", "Get Page Url"])
	# to_search = "fabi fiba"
	to_search = input("What are you looking for?\n")
	if wikipedia.suggest(to_search) is not None:
		to_search = wikipedia.suggest(to_search)
	print("I'm looking for %s" % to_search)
	search_results = wikipedia.search(to_search, results = max_search_results)
	print(search_results)
	which_one = draw_menu(search_results)
	term = search_results[which_one]
	which_one = draw_menu(search_choices)
	if which_one == 0:
		output = get_summary(term)
		print(output)
	elif which_one == 1:
		output = get_page_info(term, "fullpage")
		print(output)
	elif which_one == 2:
		output = get_page_info(term, "fullpagehtml")
		print(output)
	elif which_one == 3:
		output = get_page_info(term, "getimageslink")
		response = draw_input("Do you want to download all of them? [Y/N]: \t", list(["Y", "N"]))
		if response.upper() == "Y":
			title = get_page_info(term, "getpagetitle")
			# Download all images
			download_from_links(output, title)
	elif which_one == 4:
		output = get_page_info(term, "getpageurl")
		print(output)
	else:
		print("Hello!")
	





if __name__ == "__main__":
	main()