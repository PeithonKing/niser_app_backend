// this function is called when the page is loaded. It listens to
// the change event of the category select element and adds a new
// input element if the selected value is "Other". Thus the user
// can put the other value if the category is not in the list. If
// the user selects a value other than "Other" the input element
// is removed.

function main(e) {
	let selectCategory = document.querySelector('#id_category');
	selectCategory.onchange = function(e) {
		if (selectCategory.value === "Other") { // if the selected value is "Other" add a new input element
			selectCategory.setAttribute("name", "");

			let inputCategory = document.createElement("input");
			inputCategory.id = "id_category_other";
			inputCategory.setAttribute("type", "text");
			inputCategory.setAttribute("name", "category");
			inputCategory.setAttribute("required", "");

			selectCategory.parentNode.appendChild(inputCategory);
		} else {  // if the selected value is not "Other" remove the input element if present
			let inputCategory = document.querySelector("#id_category_other");
			if (inputCategory) {
				inputCategory.parentNode.removeChild(inputCategory);
				selectCategory.setAttribute("name", "category");
			}
		}
	};
}

window.onload = main;
