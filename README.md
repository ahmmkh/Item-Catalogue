# Item Catalog Project:

Item Catalog Project is a course related project in Udacity's nanodegree. This is a complete RESTful web application made using Flask framework. It utilizes different features including Authentication & Authorization using OAuth2.0, JSON endpoints, local permission system, and finally allows registered users to perform Create, Read, Update, and Delete operations on all categories.

Some of the technologies used to build this application include Flask, Bootsrap, Jinja2

# Installation:

The project.py file will work from any environment with Python,flask and SQLalchemy installed. Setting up a VM will help ensure that all users have the same environment, as long as you have the correct versions of Python, flask, SQLalchemy installed, feel free to skip this part.

The VM is a Linux server system that runs on top of your own computer. You can share files easily between your computer and the VM and it requires installing both VirtualBox, and Vagrant.

### Install VirtualBox:
VirtualBox is the software that actually runs the virtual machine. You can download it from [virtualbox.org](Virtualbox.org). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

### Install Vagrant:
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from [vagrantup.com](vagrantup.com). Install the version for your operating system.

Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.


### Download the VM configuration:
Use Github to fork and clone this Vagrantfile [https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile)


### Start the virtual machine
From your terminal, inside the vagrant subdirectory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM!


# Logged in!

If you are now looking at a shell prompt that starts with the word vagrant (as in the above screenshot), congratulations — you've gotten logged into your Linux VM.


### Logging out and in
If you type exit (or Ctrl-D) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type vagrant ssh again.

If you reboot your computer, you will need to run vagrant up to restart the VM.

You can power off the virtual machine by typing `vagrant halt` from the host computer's shell.


## Running using the command line
Windows:
Create a folder on your computer to use for your Python programs, such as C:\pythonpractice, and save your .py files in that folder.
In the Start menu, select "Run...", and type in cmd. This will cause the Windows terminal to open.
Type cd \directory to change directory to your program folder, and hit Enter.
Type project.py to run your program!

Mac:
Create a folder on your computer to use for your Python programs. A good suggestion would be to name it pythonpractice and place it in your Home folder (the one that contains folders for Documents, Movies, Music, Pictures, etc). Save your .py files into this folder.
Open the Applications folder, go into the Utilities folder, and open the Terminal program.
Type cd your-directory to change directory to your program folder, and hit Enter.
Type python ./project.py to run your program!

Linux:
Create a folder on your computer to use for your Python programs, such as ~/pythonpractice, and save your .py files in that folder.
Open up the terminal program. In KDE, open the main menu and select "Run Command..." to open Konsole. In GNOME, open the main menu, open the Applications folder, open the Accessories folder, and select Terminal.
Type cd ~/pythonpractice to change directory to your pythonpractice folder, and hit Enter.
Type python ./project.py to run your program!

## Important Note
When adding an item or a category, please provide an image in the form, if you updated a category or an item with no image, the code will not work.

## Things to improve
- Making adding images optional.
- Deleting actual images from the server after the user deletes them.

## JSON EndPoints
`/categories/JSON` JSON endpoint to view all info about all categories
![alt text](https://github.com/AhmedElkashef02/Item-Catalogue/blob/master/assets/categoriesJSON.png)


`/categories/<category>/<int:item_id>/JSON` JSON endpoint to view all info for a single item
![alt text](https://github.com/AhmedElkashef02/Item-Catalogue/blob/master/assets/singleItemJSON.png)


`/categories/<category>/JSON`JSON endpoint to view all items within a category
![alt text](https://github.com/AhmedElkashef02/Item-Catalogue/blob/master/assets/SingleCategoryJSON.png)
