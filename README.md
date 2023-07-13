# WinGPT
### An OpenAI command-line interface. 

## Some notes until I write the actual README file.

Currently there is a cli and a gui available through `init.py`. Inside ***init.py*** there is a variable called `USE_GUI` which you can switch from true to false or vice versa depending on your preference: **gui** or  **cli**.

The **cli** currently holds most of the funcionality like being able to control everything such as the ***response token limit***, the ***engine*** etc. Originally I didn't plan on building a gui and was solely focused on the cli. Because of this the gui currently only supports chatting but not changing any settings.

Since I created the gui later I didn't wrap it fully around the cli yet but instead only what it needs to function so far which is making requests and getting responses. ***Soon I will be rebuilding the gui around the cli*** I would just like to finish the cli and clean it up before doing so. 
