
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


// Get the unique values in the array.
function uniq(array)
{
	return array.filter(function(x,i,a){return a.indexOf(x) === i;})
}


// Create a Counter object that maps the array values to the number of occurrences.
function counter_create(array)
{
	var result = {}

	//##### find a better way to do this
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

	//##### find a better way to do this
	for (var i = 0; i < least_common_keys.length; ++i)
	{
		delete object[least_common_keys[i]]
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

	//##### find a better way to do this
	for (var i = 0; i < most_common_keys.length; ++i)
	{
		delete object[most_common_keys[i]]
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
	for each (var regex in regexes)
	{
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
	for each (var regex in regexes)
	{
		if (!regex.test(string))
		{
			return false
		}
	}

	return true
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

	//##### find a better way to do this
	for (var i = 0; i < array.length; ++i)
	{
		if (array[i].length < min)
		{
			min = array[i].length
		}
	}

	return min
}


function get_max_string_length(array)
{
	var max = Number.MIN_VALUE

	//##### find a better way to do this
	for (var i = 0; i < array.length; ++i)
	{
		if (array[i].length > max)
		{
			max = array[i].length
		}
	}

	return max
}


function string_repeat(string, num)
{
	return Array(num+1).join(string)
}


//------------------------------------------------------------------------------


function validate_letters(letters)
{
	// Convert the string to lowercase.
	letters = letters.toLowerCase()

	// Remove all non-lowercase characters.
	letters = letters.replace(/[^a-z]/g, "")

	return letters
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

