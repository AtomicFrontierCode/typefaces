I-beam analysis code for the "Which typeface's capital "I" makes the best I-beam?" video.

Hacked together in Python because I've become lazy and unfulfilled. 

== To play around with data ==

Download the <<4.Results and Graphs>> folder. The 'showGraphs.py' file will plot the data storred in 'normalisedData.txt'.
If you also download font images (really large set of files, sorry) then it might also plot a preview assuming it actually works.

== To test your own fonts ==

This is a little harder as you'll need an Abaqus license. There might be information about getting a trial / university copy at https://www.3ds.com/products/simulia/abaqus/cae. I don't know, I just used my university lab computer (sorry people who actually have important research).

You'll then want to run through the following folders in order...

<1. Raw font profiles>
This is a collection of the origional beam profiles. The included 'generateFonts.py' should generate a bunch based on what fonts you have installed. It's a little broken though so you can also just insert your own 1000px x 1000px jpg.

<2. Vectorised graphics>
This is a collection of the beam profiles simplified as vectors. The 'generateVectors.py' should be able to take the raw fonts from the previous stage and convert them into vectors. 

<3. Abaqus simulation>
This is the step that needs Abaqus. If somone wants to substitute it for an open source python version that would be awesome... I just found Abaqus' record feature really useful and was able to hack together a vector-to-beam conversion.
The 'fontsToTest.txt' file contains the list of fonts you want to test. Modify as needed.
Run the 'abaqusBending.py', 'abaqusBuckling.py', 'abaqusTorsion.py', 'abaqusTension.py' of your choice.
The function saves an output image and the stress data. It doesn't save the full results because that produces far too much data.
The 'cleanData.py' function should combine and clean your raw data outputs. 

<4. Results and graphs>
Finally you should be able to run the 'showGraphs.py' file.

== Modifying and updating ==

If you have an interrest please feel free to modify an update as you see fit. I'm bad at maintaining code and never want to see an I-beam again. I wish you the best!
- James
