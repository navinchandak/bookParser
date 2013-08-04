Group Number - 5
Group Member Names -
	1.Hardik Kothari 110050029
	2.Navin Chandak 110050047
	3.Putha Preetham Sai Sreenivas 110050073

I hereby declare that we have not plagiarized the lab work from any source. All the content present here is the 
product of the hours of discussion and work of our team. 

Brief description of the algorithms for:
1. finding the Author and Title of the novel:
- When traversing the text file from the start, the first line that starts with "Author" gives the name of the author and the first line 		starting with "Title" gives the title of the novel.

2. finding the characters of the story along with their number of occurances: 
- Only a word with its first letter as capital can be a character.
- We identify such consecutive words with their first letters as capital and call them a capital block.
- Only a capital block can be a character.
- The following arguments are for the condition that the capital block doesn't come at the the start of a line.
	-- If the first word of a capital block is Mr., Mrs., Ms., Dr., Prof. etc., then definitely it is a character.
	-- If the last word of the capital block is Jr. or Sr., then definitely it is a character.
	-- If any of the two words before the capital block is a, an, the, at, these etc., then definitely it is not a character.
	-- If any capital block is followed by the words either 'himself' or 'herself', then definitely it is a character.
- The following arguments are for the condition that the capital block comes at the the start of a line. 
	-- If the capital block contains just one word, then we just search if that word is stored as a character which also appeared in the 			earlier part of text. Here we are assuming that as all the words that start the sentence begin with a capital letter, it is a rare 			chance that the first word is a character or even if it is a character then it would have appeared atleast once earlier. Or, in other 			words, if the capital block at the start of a sentence is of size 1, then it not a first occurance of a character. In some very rare 			cases if its a character, then unfortunately our algorithm will ignore it.
	-- Other points are similar to the one where the capital block comes in between except the point which checks the words before the capital 			block.
- If some consecutive words with their first letters as capital are separated by commas followed by an 'and' or an 'or', then we assume that 	they are of same type i.e. suppose certain words appear with commas between them and if we are able to find any of these words which had 	appeared earlier as a character, then we can infer that all of these words separated by commas are characters and vice versa.
- Some general highlights:
	-- We are separating the given novel into sentences which are identified by full stops(.) and double quotes("") .
	-- We are storing all the capital blocks in a list with their number of occurances and a string representing their status like "confirm" 			(if it is confirmed as a character), "maybe" and "no".

3. finding the gender of characters:
- After finding the chracters from the above method use following arguments:
	-- If words like Mr., Ms., Mrs., Miss, Master, Lady etc. words appear before a character then we can identify its gender.
	-- If the character name is followed by words like 'himself' or 'herself', then we can identify the gender of the character.
	-- Let the set of all pronouns which can distinguish between gender like him, his, her etc. be 'S'. If in a particular sentence, only a 		character name appears and no word from the set S appears and then whenever in subsequent sentences the first instance of a word 			belonging to set S comes, then we can identify the gender of the character.

4. finding heros, heroines and villians:
- The male character with highest number of occurances is the hero.
- The female character with highest number of occurances is the heroin.
- The one with the highest number of occurances apart from the hero and the heroine is the villian. 

