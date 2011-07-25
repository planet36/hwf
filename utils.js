
/*
Copyright (C) 2011 Steve Ward

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

//------------------------------------------------------------------------------


// Get the datum by its id.  This is a utility for "getElementById".
function id(x)
{
	if (typeof x == "string")
	{
		try
		{
			return document.getElementById(x)
		}
		catch (e)
		{
			alert(e.name + ": " + e.message)

			return x
		}
	}
	else
	{
		return x
	}
}


// Get the daturm by its name.  This is a utility for "getElementsByName".
function name(x)
{
	if (typeof x == "string")
	{
		try
		{
			return document.getElementsByName(x)
		}
		catch (e)
		{
			alert(e.name + ": " + e.message)

			return x
		}
	}
	else
	{
		return x
	}
}


//------------------------------------------------------------------------------

/*
Source:
http://mxr.mozilla.org/mozilla-central/source/layout/style/html.css
*/

var default_display_value_map = {}

default_display_value_map["area"]     = "none"
default_display_value_map["base"]     = "none"
default_display_value_map["basefont"] = "none"
default_display_value_map["datalist"] = "none"
default_display_value_map["head"]     = "none"
default_display_value_map["meta"]     = "none"
default_display_value_map["noembed"]  = "none"
default_display_value_map["noframes"] = "none"
default_display_value_map["param"]    = "none"
default_display_value_map["script"]   = "none"
default_display_value_map["style"]    = "none"
default_display_value_map["title"]    = "none"

default_display_value_map["address"]    = "block"
default_display_value_map["article"]    = "block"
default_display_value_map["aside"]      = "block"
default_display_value_map["blockquote"] = "block"
default_display_value_map["body"]       = "block"
default_display_value_map["center"]     = "block"
default_display_value_map["dd"]         = "block"
default_display_value_map["dir"]        = "block"
default_display_value_map["div"]        = "block"
default_display_value_map["dl"]         = "block"
default_display_value_map["dt"]         = "block"
default_display_value_map["figcaption"] = "block"
default_display_value_map["figure"]     = "block"
default_display_value_map["footer"]     = "block"
default_display_value_map["form"]       = "block"
default_display_value_map["frameset"]   = "block"
default_display_value_map["h1"]         = "block"
default_display_value_map["h2"]         = "block"
default_display_value_map["h3"]         = "block"
default_display_value_map["h4"]         = "block"
default_display_value_map["h5"]         = "block"
default_display_value_map["h6"]         = "block"
default_display_value_map["header"]     = "block"
default_display_value_map["hgroup"]     = "block"
default_display_value_map["hr"]         = "block"
default_display_value_map["html"]       = "block"
default_display_value_map["listing"]    = "block"
default_display_value_map["map"]        = "block"
default_display_value_map["menu"]       = "block"
default_display_value_map["nav"]        = "block"
default_display_value_map["ol"]         = "block"
default_display_value_map["p"]          = "block"
default_display_value_map["plaintext"]  = "block"
default_display_value_map["pre"]        = "block"
default_display_value_map["section"]    = "block"
default_display_value_map["ul"]         = "block"
default_display_value_map["xmp"]        = "block"

default_display_value_map["table"] = "table"

default_display_value_map["caption"] = "table-caption"

default_display_value_map["tr"] = "table-row"

default_display_value_map["col"] = "table-column"

default_display_value_map["colgroup"] = "table-column-group"

default_display_value_map["tbody"] = "table-row-group"

default_display_value_map["thead"] = "table-header-group"

default_display_value_map["tfoot"] = "table-footer-group"

default_display_value_map["td"] = "table-cell"
default_display_value_map["th"] = "table-cell"

default_display_value_map["li"] = "list-item"

default_display_value_map["marquee"] = "inline-block"


function get_default_display_value(element)
{
	var tag_name = id(element).tagName.toLowerCase()

	var default_display_value = default_display_value_map[tag_name]

	if (default_display_value == null)
	{
		default_display_value = "inline"
	}

	return default_display_value
}


//------------------------------------------------------------------------------


function get_element_property(element, property)
{
	try
	{
		return id(element)[property]
	}
	catch (e)
	{
		alert(e.name + ": " + e.message)
	}
}


function set_element_property(element, property, value)
{
	try
	{
		id(element)[property] = value
	}
	catch (e)
	{
		alert(e.name + ": " + e.message)
	}
}


function reset_element_property(element, property)
{
	set_element_property(element, property, null)
}


//------------------------------------------------------------------------------


function get_element_disabled(element)
{
	return get_element_property(element, "disabled")
}


function set_element_disabled(element, value)
{
	set_element_property(element, "disabled", value)
}


function reset_element_disabled(element)
{
	reset_element_property(element, "disabled")
}


//------------------------------------------------------------------------------


function set_element_disabled_false(element)
{
	set_element_disabled(element, false)
}


function set_element_disabled_true(element)
{
	set_element_disabled(element, true)
}


//------------------------------------------------------------------------------


function get_element_style_property(element, property)
{
	try
	{
		return id(element).style[property]
	}
	catch (e)
	{
		alert(e.name + ": " + e.message)
	}
}


function set_element_style_property(element, property, value)
{
	try
	{
		id(element).style[property] = value
	}
	catch (e)
	{
		alert(e.name + ": " + e.message)
	}
}


function reset_element_style_property(element, property)
{
	set_element_style_property(element, property, "")
}


//------------------------------------------------------------------------------


function get_element_style_display(element)
{
	return get_element_style_property(element, "display")
}


function set_element_style_display(element, value)
{
/*
http://www.w3.org/TR/CSS1/#display
'display'
Value: block | inline | list-item | none
Initial: block

http://www.w3.org/TR/CSS21/visuren.html#propdef-display
'display'
Value: inline | block | list-item | run-in | inline-block | table | inline-table | table-row-group | table-header-group | table-footer-group | table-row | table-column-group | table-column | table-cell | table-caption | none | inherit
Initial: inline
*/
	set_element_style_property(element, "display", value)
}


function reset_element_style_display(element)
{
	reset_element_style_property(element, "display")
}


//------------------------------------------------------------------------------


function set_element_style_display_block(element)
{
	set_element_style_display(element, "block")
}


function set_element_style_display_inline(element)
{
	set_element_style_display(element, "inline")
}


function set_element_style_display_list_item(element)
{
	set_element_style_display(element, "list-item")
}


function set_element_style_display_none(element)
{
	set_element_style_display(element, "none")
}


//------------------------------------------------------------------------------


function toggle_element_style_display(element)
{
	var element_display_value = get_element_style_display(element)

	var default_display_value = get_default_display_value(element)

	if (element_display_value == default_display_value || element_display_value == "")
	{
		set_element_style_display_none(element)
	}
	else
	{
		set_element_style_display(element, default_display_value)
	}
}


//------------------------------------------------------------------------------


function get_element_style_visibility(element)
{
	return get_element_style_property(element, "visibility")
}


function set_element_style_visibility(element, value)
{
/*
http://www.w3.org/TR/CSS21/visufx.html#visibility
'visibility'
Value: visible | hidden | collapse | inherit
Initial: visible
*/
	set_element_style_property(element, "visibility", value)
}


function reset_element_style_visibility(element)
{
	reset_element_style_property(element, "visibility")
}


//------------------------------------------------------------------------------


function set_element_style_visibility_visible(element)
{
	set_element_style_visibility(element, "visible")
}


function set_element_style_visibility_hidden(element)
{
	set_element_style_visibility(element, "hidden")
}


function set_element_style_visibility_collapse(element)
{
	set_element_style_visibility(element, "collapse")
}


function set_element_style_visibility_inherit(element)
{
	set_element_style_visibility(element, "inherit")
}


//------------------------------------------------------------------------------


function toggle_element_style_visibility(element)
{
	var element_visibility_value = get_element_style_visibility(element)

	var default_visibility_value = "visible"

	if (element_visibility_value == default_visibility_value || element_visibility_value == "")
	{
		set_element_style_visibility_hidden(element)
	}
	else
	{
		set_element_style_visibility_visible(element)
	}
}


//------------------------------------------------------------------------------


// Get the unique values in the array.
function uniq(array)
{
	return array.filter(function(x,i,a){return a.indexOf(x) === i;})
}


// Create a Counter object that maps the array values to the number of occurrences.
function counter_create(array)
{
	var result = {}

	for (var i = 0; i < array.length; ++i)
	{
		var elem = array[i]

		if (! result.hasOwnProperty(elem))
		{
			result[elem] = 0
		}

		result[elem]++
	}

	return result
}


// Count the number of properties in the object.
function count_properties(object)
{
	var count = 0

	for (var property in object)
	{
		++count
	}

	return count
}


//------------------------------------------------------------------------------


// Get the least common value in the Counter object.
function get_least_common_value(object)
{
	var min = Number.MAX_VALUE

	for (var property in object)
	{
		if (object[property] < min)
		{
			min = object[property]
		}
	}

	return min
}


// Get the keys of the least common elements from the Counter object.
function get_least_common_keys(object)
{
	var min = get_least_common_value(object)

	var least_common_keys = []

	for (var property in object)
	{
		if (object[property] == min)
		{
			least_common_keys.push(property)
		}
	}

	return least_common_keys
}


// Remove the keys of the least common elements from the Counter object.
function remove_least_common_keys(object)
{
	var least_common_keys = get_least_common_keys(object)

	for (var i = 0; i < least_common_keys.length; ++i)
	{
		var least_common_key = least_common_keys[i]

		delete object[least_common_key]
	}
}


//------------------------------------------------------------------------------


// Get the most common value in the Counter object.
function get_most_common_value(object)
{
	var max = Number.MIN_VALUE

	for (var property in object)
	{
		if (object[property] > max)
		{
			max = object[property]
		}
	}

	return max
}


// Get the keys of the most common elements from the Counter object.
function get_most_common_keys(object)
{
	var max = get_most_common_value(object)

	var most_common_keys = []

	for (var property in object)
	{
		if (object[property] == max)
		{
			most_common_keys.push(property)
		}
	}

	return most_common_keys
}


// Remove the keys of the most common elements from the Counter object.
function remove_most_common_keys(object)
{
	var most_common_keys = get_most_common_keys(object)

	for (var i = 0; i < most_common_keys.length; ++i)
	{
		var most_common_key = most_common_keys[i]

		delete object[most_common_key]
	}
}


//------------------------------------------------------------------------------


// Add the occurrences of the array values to the Counter object.
function add_counters(object1, object2)
{
	for (var property in object2)
	{
		if (! object1.hasOwnProperty(property))
		{
			object1[property] = 0
		}

		object1[property]++
	}
}


// Convert the Counter object to an array.
function counter_to_array(object)
{
	var array = []

	for (var property in object)
	{
		var value = object[property]

		if (array[value] == null)
		{
			array[value] = []
		}

		array[value] = array[value].concat(property).sort()
	}

	return array
}


//------------------------------------------------------------------------------


// Determine if the string matches any of the regular expressions.
function matches_any(string, regexes)
{
	for (var i = 0; i < regexes.length; ++i)
	{
		var regex = regexes[i]

		if (regex.test(string))
		{
			return true
		}
	}

	return false
}


// Determine if the string matches none of the regular expressions.
function matches_none(string, regexes)
{
	return !matches_any(string, regexes)
}


// Determine if the string matches all of the regular expressions.
function matches_all(string, regexes)
{
	for (var i = 0; i < regexes.length; ++i)
	{
		var regex = regexes[i]

		if (!regex.test(string))
		{
			return false
		}
	}

	return true
}


//------------------------------------------------------------------------------


//##### are these stable?

function sort_ascend(x)
{
	return x.sort(function(a, b){return b < a})
}


function sort_descend(x)
{
	return x.sort(function(a, b){return a < b})
}


//------------------------------------------------------------------------------


function number_to_string(number, width)
{
	var number_str = number.toString()

	if (width > number_str.length)
	{
		number_str = Array(width - number_str.length + 1).join(" ") + number_str
	}

	return number_str
}


function get_min_string_length(array)
{
	var min = Number.MAX_VALUE

	for (var i = 0; i < array.length; ++i)
	{
		var x = array[i]

		if (x.length < min)
		{
			min = x.length
		}
	}

	return min
}


function get_max_string_length(array)
{
	var max = Number.MIN_VALUE

	for (var i = 0; i < array.length; ++i)
	{
		var x = array[i]

		if (x.length > max)
		{
			max = x.length
		}
	}

	return max
}


// Repeat a string a number of times.
function string_repeat(string, num)
{
	return Array(num + 1).join(string)
}


//------------------------------------------------------------------------------


// These are the values of the letters in some Zynga word games.
zynga_letter_values = {
	"A" : 1,
	"B" : 4,
	"C" : 4,
	"D" : 2,
	"E" : 1,
	"F" : 4,
	"G" : 3,
	"H" : 3,
	"I" : 1,
	"J" : 10,
	"K" : 5,
	"L" : 2,
	"M" : 4,
	"N" : 2,
	"O" : 1,
	"P" : 4,
	"Q" : 10,
	"R" : 1,
	"S" : 1,
	"T" : 1,
	"U" : 2,
	"V" : 5,
	"W" : 4,
	"X" : 8,
	"Y" : 3,
	"Z" : 10,
}


// Get the letter values of the letters.
function letters_to_letter_values(letters)
{
	return letters.toUpperCase().split("").map(function(letter){return zynga_letter_values[letter]})
}


// Split the bonus string into an array of bonuses.
function split_bonus_string(bonus_string)
{
	return bonus_string.replace(/(DL|TL|DW|TW|.)/g, "$1 ").trim().split(" ")
}


// Apply the bonuses to the letter values.
function apply_bonuses(letter_values, bonuses)
{
	if (bonuses == null)
	{
		return
	}

	var bonuses_len = bonuses.length

	var word_multiplier = 1

	for (var i = 0; i < letter_values.length; ++i)
	{
		if (i == bonuses_len)
		{
			// There are no more bonuses to apply.
			break;
		}

		if (bonuses[i] == "DL")
		{
			letter_values[i] *= 2
		}
		else if (bonuses[i] == "TL")
		{
			letter_values[i] *= 3
		}
		else if (bonuses[i] == "DW")
		{
			word_multiplier *= 2
		}
		else if (bonuses[i] == "TW")
		{
			word_multiplier *= 3
		}
	}

	if (word_multiplier != 1)
	{
		// Apply a word multiplier.
		for (var i = 0; i < letter_values.length; ++i)
		{
			letter_values[i] *= word_multiplier
		}
	}
}


function get_word_value(word, bonuses)
{
	var letter_values = letters_to_letter_values(word)

	apply_bonuses(letter_values, bonuses)

	// Get the array sum.
	return letter_values.reduce(function(a, b){return a + b})
}


//------------------------------------------------------------------------------


// Validate the letters.
function validate_letters(letters)
{
	// Convert the string to lowercase.
	letters = letters.toLowerCase()

	// Remove all non-lowercase characters.
	letters = letters.replace(/[^a-z]/g, "")

	return letters
}


// Validate the bonus string.
function validate_bonus_string(bonus_string)
{
	// Convert the string to uppercase.
	bonus_string = bonus_string.toUpperCase()

	// Trim leading and trailing whitespace.
	bonus_string = bonus_string.trim()

	return bonus_string
}


// Validate the word pattern.
function validate_word_pattern(word_pattern)
{
	// Convert the string to lowercase.
	word_pattern = word_pattern.toLowerCase()

	// Remove characters not matching lowercase letters and unknown letters.
	word_pattern = word_pattern.replace(/[^a-z.?]/g, "")

	return word_pattern
}


// Validate the excluded letters.
function validate_excluded_letters(excluded_letters, word_pattern)
{
	// Convert the string to lowercase.
	excluded_letters = excluded_letters.toLowerCase()

	// Remove characters not matching lowercase letters.
	excluded_letters = excluded_letters.replace(/[^a-z]/g, "")

	// Add letters in the word pattern to the excluded letters.
	excluded_letters += word_pattern.replace(/[^a-z]/g, "")

	// Remove duplicate letters and sort the letters.
	excluded_letters = uniq(excluded_letters.split("").sort()).join("")

	return excluded_letters
}


//------------------------------------------------------------------------------
